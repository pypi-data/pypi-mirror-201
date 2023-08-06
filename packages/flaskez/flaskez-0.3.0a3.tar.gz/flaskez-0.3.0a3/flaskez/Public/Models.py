from flaskez._basic.html import t as templates
import typing
import os


class Page:
    """
    Class for representing pages in the instant_setup() function.
    """

    def __init__(self, template_or_code: typing.Union[str, typing.TextIO] = "base", route: str = "/") -> None:
        if isinstance(template_or_code, typing.TextIO):
            self.source = template_or_code.read()
        elif isinstance(template_or_code, str):
            self.source = template_or_code
        else:
            raise TypeError('Invalid type for parameter "template_or_code"')

        self._route = route if route.startswith("/") else "/" + route

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, value: str) -> None:
        if value in templates:
            self._source = templates[value]
        else:
            if os.path.isfile(value):
                with open(value) as f:
                    self._source = f.read()
            else:
                self._source = value

    @property
    def route(self) -> str:
        return self._route

    @route.setter
    def route(self, value: str) -> None:
        self._route = value if value.startswith("/") else "/" + value
