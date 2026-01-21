1. Edge Agent (customer-side) — MUST HAVE

This is the product customers run.

Core

MQTT broker (Mosquitto or EMQX)

TLS support

Device authentication (username/password or cert)

Topic enforcement via your TopicBuilder grammar

ACL file generation from policies

Hot-reload config without restart

Control

Outbound HTTPS connection to your SaaS

Periodic policy sync

Health reporting

Packaging

Docker image

Simple env-based config:

TENANT_ID
AGENT_TOKEN
CONTROL_PLANE_URL

2. SaaS Control Plane — MUST HAVE

This is what you sell access to.

Tenant management

Create company / farms / devices

Assign device credentials

API tokens for agents

Configuration

Upload YAML provisioning

Validate schema

Generate topic structure

Generate ACL rules

Policy engine

Per-MessageType rules:

allowed QoS

retained allowed

publish / subscribe permissions

API

REST endpoints:

POST /tenants
POST /agents/register
POST /configs/upload
GET  /agents/{id}/policy

3. Topic System (your core advantage)
Features

Formal topic grammar

Hierarchical validation

Wildcard scoping

Contract-based message types

Topic preview generator

Output

MQTT topic lists

Subscription patterns

ACL rules

4. Security (non-negotiable)

Per-device credentials

Per-agent token

Tenant isolation

No wildcard publish to cmd

QoS enforcement

5. CLI Tool (optional but powerful)
iotctl push config.yml
iotctl list topics
iotctl validate config.yml


Saves you UI work early.

6. Basic UI (minimal)

Just enough to sell.

Pages

Tenants

Farms

Devices

Agents

Topics preview

API tokens

No dashboards. No graphs. No real-time charts.

7. What NOT to build in MVP

❌ Billing automation
❌ Device OTA
❌ Data storage
❌ Visualization
❌ AI
❌ Rules engine
❌ Alerting
❌ Kafka integration
❌ Multi-region HA

All later.

MVP Architecture Diagram
Customer network
┌────────────┐
│ Sensors    │
└─────┬──────┘
      │ MQTT
┌─────▼───────────┐
│ Edge Agent      │
│ - broker        │
│ - ACL engine    │
│ - policy sync   │
└─────┬───────────┘
      │ HTTPS
┌─────▼─────────────────┐
│ SaaS Control Plane    │
│ - tenants             │
│ - YAML config         │
│ - topic engine        │
│ - API                 │
└───────────────────────┘

MVP Success Criteria (real world)

You can:

onboard a customer in < 30 minutes

deploy agent with Docker

see topics generated correctly

block invalid publishes

isolate tenants

rotate credentials

If yes → you can charge money.

Expected build effort (solo dev)
Component	Time
Topic engine (you have)	✔
Domain model	✔
YAML loader	2 days
ACL generator	3 days
Agent container	1 week
SaaS API	1 week
Minimal UI	1 week
Docs	3 days

≈ 4–5 weeks

Pricing for MVP

Start with:

€49 / agent / month

€0.10 / device / month

Even 20 customers = real income.

Brutal truth

If you ship just this MVP:

You are already ahead of:

90% of IoT startups

95% of MQTT tool vendors

Because your topic grammar + policy model is the hard part.

If you want next

I can provide:

API contract spec

edge agent component design

Mosquitto ACL generator logic

SaaS DB schema

onboarding flow

or pitch deck outline

You’re not building a toy.

You’re building a platform.