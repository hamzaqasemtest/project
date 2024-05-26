import importlib
import os
import pkgutil
from fastapi import APIRouter


class RoutesIncluder:

    @staticmethod
    def get_routes():

        router = APIRouter()

        package_dir = os.path.dirname(__file__)
        for _, module_name, _ in pkgutil.iter_modules([package_dir]):
            if module_name != "__init__":
                module = importlib.import_module(f"{__name__}.{module_name}")
                if hasattr(module, "router"):
                    router.include_router(module.router, prefix='/api')

        return router
