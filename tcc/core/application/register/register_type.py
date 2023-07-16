from enum import Enum


class RegisterType(str, Enum):
    TABLE_REPOSITORY = "table_repository"
    TRANSFORMER_RUNNER = "transformer_runner"
    VARIATION_REPOSITORY = "variation_repository"
