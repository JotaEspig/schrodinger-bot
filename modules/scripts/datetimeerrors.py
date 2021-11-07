class InvalidDate(Exception):
    def __init__(self, *args) -> None:
        super().__init__("Invalid date format", *args)


class InvalidTime(Exception):
    def __init__(self, *args) -> None:
        super().__init__("Invalid time format", *args)