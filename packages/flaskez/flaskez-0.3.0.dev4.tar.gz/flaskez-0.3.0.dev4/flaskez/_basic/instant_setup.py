from flaskez.Public.Models import Page
import flask


def instant_setup(pages: list[Page], run: bool = True, static: str = 'static', templates: str = 'templates') -> flask.Flask:
    app = flask.Flask('flaskez_application', static_folder=static, template_folder=templates)

    for page in pages:
        exec(
             f'app.add_url_rule("{page.route}", "{page.route}", lambda **kwargs: flask.render_template("""{page.source}""", **kwargs) if """{page.source}""".endswith(".html") else """{page.source}""")')

    if run:
        app.run()

    return app
