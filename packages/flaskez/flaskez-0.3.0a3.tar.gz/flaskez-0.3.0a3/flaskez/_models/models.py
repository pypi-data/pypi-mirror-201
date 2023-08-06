def _false() -> None:
    raise ValueError("'value' has to be a bool.")


class Configuration:
    """
    Configuration object for flaskez.

    Properties:
    SUPPRESS_WARNINGS - False to show all warnings in the console, True to hide all warnings.
    """
    def __init__(self) -> None:
        self.__SUPPRESS = False

    @property
    def SUPPRESS_WARNINGS(self) -> bool:
        return self.__SUPPRESS

    @SUPPRESS_WARNINGS.setter
    def SUPPRESS_WARNINGS(self, value: bool) -> None:
        self.__SUPPRESS = value if isinstance(value, bool) else _false()


config = Configuration()
