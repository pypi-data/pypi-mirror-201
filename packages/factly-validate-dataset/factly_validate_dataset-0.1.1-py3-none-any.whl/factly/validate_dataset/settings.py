from typing import List

DEFAULT_LOG_FILE: str = "virus.log"
DEFAULT_VALIDATION_RULES: str = "src/validations/rules.py"
DEFAULT_DATASET_RULES: str = "src/validations/config.json"
DEFAULT_VALIDATION_COLUMNS: List[str] = [
    "schema_context",
    "column",
    "check",
    "check_number",
    "failure_case",
    "index",
]
