"""
Private subpackage containing HTML code.
"""
import typing

base: str = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Flaskez Base Page</title>
    </head>
    <body>
        <div class="base">
            <h1>Flaskez Base Page</h1>
        </div>
    </body>
</html>
"""

t: typing.Dict[str, str] = {"base": base}
