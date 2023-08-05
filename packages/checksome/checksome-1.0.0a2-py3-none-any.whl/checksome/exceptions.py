class UnexpectedEndOfBuffer(Exception):
    def __init__(self, offset: int, length: int) -> None:
        super().__init__(
            f"Buffer does not have {length} byte{'s' if length > 1 else ''} "
            f"after offset {offset}"
        )
