# Imports
from flask import Flask, Blueprint, current_app
from flask_sqlalchemy import SQLAlchemy
from flaskez import config as c
import typing as t
import importlib
import datetime
import warnings
import secrets


def create_app(
        app_name: t.Optional[str] = "flaskez_application",
        *args: t.Optional[t.Any],
        run: t.Optional[bool] = False,
        run_kwargs: t.Optional[dict] = None,
        config: t.Optional[dict] = None,
        secret_key: t.Optional[str] = None,
        generate_secret_key: t.Optional[bool] = True,
        routes: t.Optional[list] = None,
        error_pages: t.Optional[list] = None,
        permanent_session_lifetime: t.Optional[dict] = None,
        create_db: t.Optional[bool] = False,
        flask_kwargs: t.Optional[dict] = None,
        db_kwargs: t.Optional[dict] = None,
        **kwargs: t.Optional[t.Any]
) -> t.Union[t.Tuple[Flask, SQLAlchemy], Flask]:  # Function for creating a flask.Flask object
    """
    create_app() is a function for generating a flask.Flask object.
    :param app_name: Name of the Flask application. Defaults to "flaskez_application" if no value is entered.
    :param args: Optional positional arguments. Passed to the flask.Flask().register_blueprint() function.
    :param run: Optional bool if you want the function to run the application directly.
    :param run_kwargs: Optional dict if you want extra keyword arguments passed to the flask.Flask().run() function.
    :param config: Dictionary. Configuration for the flask.Flask object.
    :param secret_key: String. Variable if you want to define a custom secret key for the application.
    :param generate_secret_key: Bool. Variable if you want to generate a secret key. Uses python's random and secrets modules.
    :param routes: List. A list with dictionaries of all blueprints for the application.
    Format: routes=[{'path': 'routes.routes', 'blueprint': 'routes'}] or routes=[{'blueprint': flask.Blueprint(*args, **kwargs)}]
    Path can also be the imported file.
    An optional key 'prefix' can be added to specify a prefix for the url (an extra / (route) before the unique route of the web page).
    It is easier to use the create_blueprint() function (see its docs for more info).
    :param error_pages: List. A list with dictionaries of all error pages for the application.
    Format: error_pages=[{'path': 'routes.routes', 'code': '404', 'function': 'not_found'}]
    :param permanent_session_lifetime: Dictionary. Permanent session lifetime variable for flask.sessions.
    :param create_db: Bool. Optionally create a database (using flask-sqlalchemy). Used for login, etc.
    :param flask_kwargs: A dictionary for arguments passed to the creation of the flask.Flask object (kwargs and args are already used for blueprints)
    :param db_kwargs: A dictionary for arguments passed to the creation of the flask_sqlalchemy.SQLAlchemy object
    (kwargs and args are already used for blueprints)
    :param kwargs: Optional keyword arguments. Passed to the register_blueprint() function.
    :return: Returns a flask.Flask object.
    """
    if permanent_session_lifetime is None:  # Checks if the user has entered custom times for the permanent_session lifetime variable
        permanent_session_lifetime = {
            'days': 0,
            'seconds': 0,
            'microseconds': 0,
            'milliseconds': 0,
            'minutes': 0,
            'hours': 0,
            'weeks': 0
        }  # Sets the value to the default value

    if flask_kwargs is None:  # Checks if the user has entered any keyword arguments for the flask application
        flask_kwargs = {}  # Sets the flask_kwargs variable to the default value of {}, emtpy dict

    if db_kwargs is None:  # Checks if the user has entered any keyword arguments for the database
        db_kwargs = {}  # Sets the db_kwargs variable to the default value of {}, empty dict

    if run_kwargs is None:  # Checks if the user has entered any keyword arguments for the run function
        run_kwargs = {}  # Sets the run_kwargs variable to the default value of {}, empty dict

    app = Flask(app_name, **flask_kwargs)  # Creating the application

    if generate_secret_key:  # Checks if the user wants to generate a secret key
        app.secret_key = secrets.token_urlsafe(256)  # Sets secret key

    elif not generate_secret_key and secret_key is None:  # If the user does not want to generate a secret key but has not entered a custom one
        app.secret_key = "DefaultKey"  # Sets secret key

    else:  # If none of the above is true
        app.secret_key = secret_key  # Sets secret key

    if config:  # Checks if the user has entered any custom configuration for the application
        for key, value in config.items():  # Loops through the configuration
            app.config[key] = value  # Gives the configuration to the application

    app.permanent_session_lifetime = datetime.timedelta(
        **permanent_session_lifetime)  # Sets the permanent session lifetime

    if routes is not None:  # Checks if there are any custom blueprint routes
        try:  # Tries to create a blueprint
            for info in routes:  # Loops through the routes list
                if 'path' in info:
                    route = importlib.import_module(info['path']) if isinstance(info['path'], str) else info[
                        'path']  # Imports the file with the blueprint
                    app.register_blueprint(getattr(route, info['blueprint']),
                                           url_prefix=info['prefix'] if 'prefix' in info else None, *args,
                                           **kwargs)  # Registers the blueprint
                    del route
                else:
                    app.register_blueprint(info['blueprint'],
                                           url_prefix=info['prefix'] if 'prefix' in info else None, *args,
                                           **kwargs)  # Registers the blueprint
        except ImportError as e:  # Error if the file didn't exist
            if not c.SUPPRESS_WARNINGS:  # Checks if the user want warnings
                warnings.warn(
                    "One of the specified routes for create_app() was not found. "
                    "\nFull python error: " + str(e),
                    ImportWarning
                )  # Warning
        except AttributeError as e:  # Error if the blueprint is broken
            if not c.SUPPRESS_WARNINGS:  # Checks if the user want warnings
                warnings.warn(
                    "Something went wrong trying to find the blueprint, "
                    "either there is no function, you haven't entered a function, or something is spelled incorrectly." +
                    "\nFull python error: " + str(e),
                    ImportWarning
                )
    else:  # No custom blueprints
        if not c.SUPPRESS_WARNINGS:  # Checks if the user want warnings
            warnings.warn(
                "There are no custom blueprints. "
                "Make sure to either create a blueprint using the create_blueprint() function "
                "or have all pages come from the flask.Flask object itself.",
                UserWarning
            )  # Warning

    if error_pages is not None:  # Checks if the user has specified any error pages
        try:
            for info in error_pages:  # Loops through the error pages list
                if 'path' in info:
                    route = importlib.import_module(info['path']) if isinstance(info['path'], str) else info[
                        'path']  # Imports the file with the error page
                    app.register_error_handler(info['code'],
                                               getattr(route, info['function']))  # Registers the error page
                    del route
                else:
                    app.register_error_handler(info['code'],
                                               info['function'])
        except ImportError as e:  # Error if the file didn't exist
            if not c.SUPPRESS_WARNINGS:  # Checks if the user want warnings
                warnings.warn(
                    "One of the specified routes for an error page was not found."
                    "\nFull python error: " + str(e),
                    ImportWarning
                )  # Warning
        except AttributeError as e:  # Error if the error page function is broken
            if not c.SUPPRESS_WARNINGS:  # Checks if the user want warnings
                warnings.warn(
                    "Something went wrong trying to find the error page function, "
                    "either there is no function, you haven't entered a function, or something is spelled incorrectly."
                    "\nFull python error: " + str(e),
                    ImportWarning
                )  # Warning

    if create_db:  # Checks if the user wants to create a database
        db = SQLAlchemy(app, **db_kwargs)  # Creates a database and assigns the flask.Flask object to the database
        with app.app_context():  # Listens to the app_context()
            db.create_all()  # Creates all tables that don't already exist in the database
        if run:  # Checks if the user wants to run the application
            app.run(**run_kwargs)  # Runs the application
        return app, db  # Returns the flask.Flask object and the database object

    if run:  # Checks if the user wants to run the application
        app.run(**run_kwargs)  # Run the application
    return app  # Returns the flask.Flask object


def create_blueprint(
        app: t.Optional[t.Union[Flask, str]] = current_app,
        *args: t.Optional[t.Any],
        app_name: t.Optional[str] = None,
        blueprint_name: t.Optional[str] = None,
        blueprint_import_name: t.Optional[str] = None,
        settings: t.Optional[dict] = None,
        blueprint_kwargs: t.Optional[dict] = None,
        **kwargs: t.Optional[t.Any]
) -> t.Union[Blueprint, None]:  # Function for creating and registering a new blueprint
    """
    create_blueprint() is a function for creating and registering blueprints for your application.
    You need to use the create_app() function or make your own flask application before you can use this function.
    NOTICE: CURRENTLY DOES NOT (easily) WORK TO CREATE A BLUEPRINT INSIDE THE FUNCTION
    UNLESS YOU FOR SOME REASON CREATE A BLUEPRINT INSIDE YOUR MAIN FILE!
    :param app: Parameter for the application object.
    Either flask.Flask or type str with the path to import the file with the app
    (app_name is required to be filled in for this one to work).
    If you use "with app.app_context():", you can skip app.
    :param args: Optional positional arguments. Passed to the register_blueprint() function.
    :param app_name: String.
    Used in case you want to import your flask.Flask object rather than passing it through the function (see param: app).
    :param blueprint_name: Name of the blueprint in case you want to not pass any settings, etc.
    :param blueprint_import_name: Import name for the blueprint. Only used if you create a blueprint inside this function without using settings.
    :param settings: List with settings in case you don't want to look up the parameters for the register_blueprint() function.
    Format: settings=[{'path': 'routes.routes', 'blueprint': 'routes'}] or settings=[{'blueprint': flask.Blueprint(*args, **kwargs)}]
    Path can also be the imported file.
    An optional key 'prefix' can be added to specify a prefix for the url (an extra / (route) before the unique route of the web page).
    :param blueprint_kwargs: Keyword arguments for creating the blueprint.
    :param kwargs: Optional keyword arguments. Passed to the register_blueprint() function.
    :return: If you choose to create the blueprint in the function, it returns a flask.Blueprint object, otherwise None.
    """
    if isinstance(app, str):  # Checks if the app is a string or not
        if app_name is not None:  # Checks if the user has entered an app name or not (required if the app is a string)
            app = getattr(importlib.import_module(app),
                          app_name)  # If the app is a string, import it together with the app name
        else:  # If the app name does not exist
            raise AttributeError(
                "You need to enter the app_name parameter if you enter the app parameter as a string")  # Raise error

    if blueprint_kwargs is None:  # Checks if the user has entered any keyword arguments for the blueprint
        blueprint_kwargs = {}  # Sets the blueprint_kwargs variable to the default value of {}, empty dict

    if settings is not None:  # Checks if the user has entered settings
        if isinstance(settings['Blueprint'], str):  # Checks if the blueprint is a string or not
            try:
                route = importlib.import_module(settings['path']) if isinstance(settings['path'], str) else settings[
                    'path']  # Imports the file with the blueprint
                app.register_blueprint(getattr(route, settings['blueprint']),
                                       url_prefix=settings['prefix'] if 'prefix' in settings else None, *args,
                                       **kwargs)  # Registers the blueprint
                del route  # Deletes the imported route
            except ImportError as e:  # Error if the file didn't exist
                if not c.SUPPRESS_WARNINGS:  # Checks if the user want warnings
                    warnings.warn(
                        "An error occurred while trying to import the blueprint."
                        "\nFull python error: " + str(e),
                        ImportWarning
                    )  # Warning
            except AttributeError as e:  # Error if the blueprint is broken
                if not c.SUPPRESS_WARNINGS:  # Checks if the user want warnings
                    warnings.warn(
                        "Something went wrong trying to find the blueprint, "
                        "either there is no blueprint, or something is spelled incorrectly."
                        "\nFull python error: " + str(e),
                        ImportWarning
                    )  # Warning
        else:  # If the blueprint isn't of type str
            try:  # Try to register a blueprint
                app.register_blueprint(settings['blueprint'],
                                       settings['prefix'] if 'prefix' in settings else None, *args,
                                       **kwargs)  # Registers the blueprint
            except AttributeError as e:  # Error if the blueprint is broken
                if not c.SUPPRESS_WARNINGS:  # Checks if the user want warnings
                    warnings.warn(
                        "Something went wrong trying to find the blueprint, "
                        "either there is no blueprint, or something is spelled incorrectly." +
                        "\nFull python error: " + str(e),
                        ImportWarning
                    )  # Warning

    else:  # If there are no settings
        if blueprint_name is not None and blueprint_import_name is not None:  # If there is a blueprint_name and blueprint_import_name
            blueprint = Blueprint(blueprint_name, blueprint_import_name, **blueprint_kwargs)  # Create a blueprint
            app.register_blueprint(blueprint, *args, **kwargs)  # Registers the blueprint
            return blueprint  # Returns the blueprint to the user
        else:  # If there isn't blueprint_name or blueprint_import_name
            app.register_blueprint(*args, **kwargs)  # Register blueprint
