# mcp_data_protect

### Enterprise-grade Model Context Protocol (MCP) server for secure, local-first LLM integration with proprietary SQL and CSV data.

Data privacy focused.

### Architecture

**Security:** Asymmetric context injection; Pydantic-enforced schema validation prevents sensitive leakage.

**Data Integrity:** Transactional audit logging and strict type-hinting for robust tool execution.

**Interface:** Decoupled data-layer supporting SQLAlchemy and pandas-backed CSV sources.

**Integration:** Built using the official MCP Python SDK and SQLAlchemy for database-agnostic performance (SQL, PostgreSQL, CSV).

**Zero-Cloud Footprint:** No data is sent to third-party vectors unless explicitly configured.

**MCP Resource Templates:** Exposes database schemas as readable resources for LLM context.

**Dynamic Tooling:** Allows LLMs to execute secure, read-only SQL queries via natural language.

**Audit Logging:** Every query and data access event is logged for compliance.


