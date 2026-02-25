### Enterprise-grade Model Context Protocol (MCP) server for secure, local-first LLM integration with proprietary SQL and CSV data.

[![CI Build](https://github.com/stefanionascu0/mcp_data_protect/actions/workflows/ci.yml/badge.svg)](https://github.com/stefanionascu0/mcp_data_protect/actions)
[![Vulnerabilities](https://snyk.io/test/github/stefanionascu0/mcp_data_protect/badge.svg)](https://snyk.io/test/github/stefanionascu0/mcp_data_protect)
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/stefanionascu0/mcp_data_protect?utm_source=oss&utm_medium=github&utm_campaign=stefanionascu0%2Fmcp_data_protect&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=stefanionascu0_mcp_data_protect&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=stefanionascu0_mcp_data_protect)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=stefanionascu0_mcp_data_protect&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=stefanionascu0_mcp_data_protect)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=stefanionascu0_mcp_data_protect&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=stefanionascu0_mcp_data_protect)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=stefanionascu0_mcp_data_protect&metric=coverage)](https://sonarcloud.io/summary/new_code?id=stefanionascu0_mcp_data_protect)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=stefanionascu0_mcp_data_protect&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=stefanionascu0_mcp_data_protect)
[![Duplicated Lines](https://sonarcloud.io/api/project_badges/measure?project=stefanionascu0_mcp_data_protect&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=stefanionascu0_mcp_data_protect)

### RUN SERVER
`uv run mcp dev src/mcp_data_protect/server.py`
### Architecture

**Security:** Asymmetric context injection; Pydantic-enforced schema validation prevents sensitive leakage.

**Data Integrity:** Transactional audit logging and strict type-hinting for robust tool execution.

**Interface:** Decoupled data-layer supporting SQLAlchemy and pandas-backed CSV sources.

**Integration:** Built using the official MCP Python SDK and SQLAlchemy for database-agnostic performance (SQL, PostgreSQL, CSV).

**Zero-Cloud Footprint:** No data is sent to third-party vectors unless explicitly configured.

**MCP Resource Templates:** Exposes database schemas as readable resources for LLM context.

**Dynamic Tooling:** Allows LLMs to execute secure, read-only SQL queries via natural language.

**Audit Logging:** Every interaction is captured via a non-intrusive `@audit_log` decorator, providing ISO-8601 timestamped telemetry for all data access events.

**Automated Governance**: Integrated with GitHub CodeQL for static analysis and Dependabot for supply chain security, maintaining a permanent "Green CI" state.


