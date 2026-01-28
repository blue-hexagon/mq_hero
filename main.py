from __future__ import annotations
import logging
import os
import signal
import sys
from pathlib import Path

from src.v2.application.runtime.context import RuntimeContext
from src.v2.application.services.tenant_assembler import TenantAssembler
from src.v2.application.services.tenant_config_service import TenantConfigService
from src.v2.edge_agent.bootstrap import BootstrapClient
from src.v2.infrastructure.filesystem.vfs import VirtualFS
from src.v2.infrastructure.loaders.schema_validator import SchemaValidator
from src.v2.infrastructure.loaders.yaml_loader import YamlLoader
from src.v2.domain.entities.registry import DomainRegistry
from src.v2.infrastructure.logging.logger import setup_logging
from dotenv import load_dotenv
from src.v2.application.services.topic_generation_service import TopicGenerationService
import asyncio

def shutdown_handler(signum, frame):
    print(f"Received signal {signum}, shutting down cleanly")
    # close sockets, flush buffers, stop threads, etc.
    sys.exit(0)

if __name__ == '__main__':
    load_dotenv(".env")
    rt = RuntimeContext()
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    if rt.is_client():
        setup_logging(
            level=logging.DEBUG,
            enable_debug_modules=[
                "src.v2.domain.policies",
                "src.v2.infrastructure.mqtt",
                "src.v2.domain.entities.tenant",
                "src.v2.application.runtime.context",
            ],
            show_empty_context=True,
        )
        bsc = BootstrapClient()
        try:
            asyncio.run(bsc.bootstrap(tenant_id=os.environ.get("TENANT_ID")))
        except KeyboardInterrupt:
            logging.getLogger(__name__).info("Client: Terminated successfully.")
    elif rt.is_server():
        setup_logging(
            level=logging.INFO,
            enable_debug_modules=[],
            show_empty_context=False,
        )
        vfs = VirtualFS(
            root=Path(".")
        )
        tcs = TenantConfigService(
            fs=vfs,
            tenant_assembler=TenantAssembler(
                registry=DomainRegistry()
            ),
            yaml_loader=YamlLoader(),
            schema_validator=SchemaValidator(),
        )
        tcs.load()
        registry = tcs.tenant_assembler.registry

        for tenant in registry.iter_tenants():
            topics = TopicGenerationService(tenant=tenant)

            acl_path = vfs.root / f"{tenant.id}.acl"

            with open(acl_path, "w", encoding="utf-8") as f:
                for topic in topics.generate_topics(with_trx_rules=True):
                    f.write(f"{topic}\n")
            # pprint(list(registry.iter_devices(tenant_id=tenant.id)))
        # logging.getLogger(__name__).info("Server: Terminated successfully.")

