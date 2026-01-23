import asyncio

from src.v2.domain.entities.tenant import Tenant
from src.v2.edge_agent.farm_runner import FarmRunner


class TenantRuntime:

    def __init__(self, farm_runner: FarmRunner):
        self.farm_runner = farm_runner

    async def run(self, tenant:Tenant):
        tasks = [
            asyncio.create_task(self.farm_runner.run(farm))
            for farm in tenant.farms.values()
        ]
        await asyncio.gather(*tasks)
