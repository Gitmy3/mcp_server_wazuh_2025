# naive mapping: if field is in FIELD_TYPES and type is keyword/text decide .keyword
from .validators import FIELD_TYPES

def field_to_term_field(field: str) -> str:
    ftype = FIELD_TYPES.get(field)
    if ftype == "keyword":
        return field  # already keyword
    if ftype == "text":
        return f"{field}.keyword"
    return field


