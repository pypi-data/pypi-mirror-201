class SchemaVersionMismatchError(Exception):
    def __init__(self, expected_version: int, actual_version: int) -> None:
        super().__init__(
            f"schema version mismatch; expected: {expected_version}, got: {actual_version}"
        )
