import os
import importlib
from .base import SocialMedia

# Dynamically import all social media plugins in this directory
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith('.py') and file != '__init__.py':
        module_name = file[:-3]
        module = importlib.import_module('.' + module_name, package=__name__)
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, SocialMedia) and obj != SocialMedia:
                SocialMedia.register_platform(obj.PLATFORM_NAME, obj)
