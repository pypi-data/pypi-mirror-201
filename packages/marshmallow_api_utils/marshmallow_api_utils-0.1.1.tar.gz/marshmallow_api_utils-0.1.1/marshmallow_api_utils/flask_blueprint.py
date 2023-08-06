# Can only be used if flask and flask-smorest are installed
import logging
from typing import Union

from .package_finder import PackageFinder

try:
    from flask import Blueprint as FlaskBlueprint
    from flask import Flask
    from flask.views import MethodViewType
except ImportError:
    raise Exception("flask must be installed to use FlaskBlueprint") from None


try:
    from flask_smorest import Api
    from flask_smorest import Blueprint as SmorestBlueprint
except ImportError:
    raise Exception("flask_smorest must be installed to use FlaskBlueprint") from None


logger = logging.getLogger(__name__)


# https://github.com/marshmallow-code/flask-smorest/issues/110
class Blueprint(SmorestBlueprint):
    '''
        Allows us to have undocumented APIs.
        To ensure an api is undocumented, simply set `document=False`
    '''
    def route(self, rule, *, parameters=None, document=True, **options):
        if document:
            return super().route(rule, parameters=parameters, **options)
        # Copy else case from Flask Blueprint
        else:
            def decorator(func):
                endpoint = options.pop("endpoint", func.__name__)
                if isinstance(func, MethodViewType):
                    view_func = func.as_view(endpoint)
                else:
                    view_func = func

                self.add_url_rule(rule, endpoint, view_func, **options)
                return view_func
            return decorator


def dynamically_register_routes(
    flask_app: Flask,
    smorest_api: Api,
    package_name=None,
    routes_package_name='routes',
):
    '''
        Dynamically registers all blueprints.

        It does this by searching for the 'routes' package in the caller's parent tree.
        Then finding all modules that have a Blueprint attribute, and registering said attribute.
    '''
    if package_name is None:
        package_name = PackageFinder.get_parent_package()

    for blueprint in PackageFinder.find_attributes_iter(
        package_name=routes_package_name,
        root_package_name=package_name,
        attr_types=(FlaskBlueprint, SmorestBlueprint),
    ):
        register_blueprint(
            blueprint,
            flask_app,
            smorest_api,
        )


def register_blueprint(
    blueprint: Union[FlaskBlueprint, SmorestBlueprint],
    flask_app: Flask,
    smorest_api: Api,
):
    '''
        Registers Blueprint
    '''
    logger.info(
        f"Registering blueprint '{blueprint.name}' with prefix '{blueprint.url_prefix}'",
        extra={
            'blueprint.name': blueprint.name,
            'blueprint.import_name': blueprint.import_name,
            'blueprint.url_prefix': blueprint.url_prefix,
        },
    )

    if isinstance(blueprint, SmorestBlueprint):
        smorest_api.register_blueprint(blueprint)
    elif isinstance(blueprint, FlaskBlueprint):
        flask_app.register_blueprint(blueprint)
