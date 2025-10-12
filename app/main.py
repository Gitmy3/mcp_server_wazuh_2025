# FastAPI Server
# Full endpoint for wazuh.search 

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from .schemas import WazuhSearchPlan
from .validators import is_index_allowed, validate_filters, enforce_time_window
from .dsl_builder import build_dsl
from .es_client import validate_query, execute_query
from .config import settings
import logging

app = FastAPI(title="MCP Wazuh (Python)")

@app.post("/mcp/wazuh.search")
async def wazuh_search(plan: WazuhSearchPlan):
    # Step 1: index allowlist
    if not is_index_allowed(plan.indices):
        raise HTTPException(400, "index not allowed")
    # Step 2: validate time window
    if not enforce_time_window(plan.time.from_, plan.time.to):
        raise HTTPException(400, "time window too large or invalid")
    # Step 3: validate filters semantics
    try:
        validate_filters(plan.filters or [])
        validate_filters(plan.must_not or [])
    except Exception as e:
        raise HTTPException(400, str(e))
    # Step 4: build DSL server-side
    dsl = build_dsl(plan)
    # Step 5: preflight validate
    if plan.dry_run:
        try:
            v = validate_query(plan.indices, dsl)
            return {"validation": v}
        except Exception as e:
            logging.exception("validate failed")
            raise HTTPException(500, f"validate failed: {e}")
    # Step 6: execute with safe defaults / try-catch
    try:
        res = execute_query(plan.indices, dsl)
        # optionally post-process mask fields etc.
        return {"result": res}
    except Exception as e:
        logging.exception("search failed")
        raise HTTPException(500, f"search failed: {e}")
    

    
