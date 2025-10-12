from typing import Dict, Any, List
from .schemas import WazuhSearchPlan, FilterItem
from .utils import field_to_term_field
from .config import settings

def filter_to_clause(f: FilterItem):
    # convert FilterItem to ES clause
    field = field_to_term_field(f.field)  # e.g., agent.name -> agent.name.keyword if needed
    op = f.op
    val = f.value
    if op == "eq":
        return {"term": {field: val}}
    if op == "in":
        return {"terms": {field: val}}
    if op == "contains":
        return {"match": {f.field: val}}
    if op in ("gt","gte","lt","lte"):
        range_op = {"gt":"gt","gte":"gte","lt":"lt","lte":"lte"}[op]
        return {"range": {f.field: {range_op: val}}}
    if op == "neq":
        return {"bool": {"must_not": {"term": {field: val}}}}
    raise ValueError("unsupported op")

def build_dsl(plan: WazuhSearchPlan) -> Dict[str, Any]:
    bool_filter = []
    must_not_clauses = []
    # time range
    time_clause = {
        "range": {
            "@timestamp": {"gte": plan.time.from_, "lte": plan.time.to}
        }
    }
    bool_filter.append(time_clause)
    # structured filters
    for f in (plan.filters or []):
        clause = filter_to_clause(f)
        # `neq` returns bool/must_not - handle simple case:
        if "bool" in clause and "must_not" in clause["bool"]:
            must_not_clauses.append(clause["bool"]["must_not"])
        else:
            bool_filter.append(clause)
    for f in (plan.must_not or []):
        clause = filter_to_clause(f)
        must_not_clauses.append(clause)
    query = {"bool": {}}
    if bool_filter:
        query["bool"]["filter"] = bool_filter
    if must_not_clauses:
        query["bool"]["must_not"] = must_not_clauses

    body = {"query": query}
    # aggregation
    if plan.aggregation:
        agg = plan.aggregation
        if agg.get("type") == "terms":
            body["aggs"] = {
                "top_terms": {"terms": {"field": agg["field"], "size": agg.get("size",10)}}
            }
            body["size"] = 0
        elif agg.get("type") == "count":
            body["size"] = 0
    else:
        body["size"] = min(plan.limit or settings.MAX_LIMIT, settings.MAX_LIMIT)

    # Safety defaults
    body.update({"track_total_hits": False})
    return body


