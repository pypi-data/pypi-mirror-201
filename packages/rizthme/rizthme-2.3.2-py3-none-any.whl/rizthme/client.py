import os
import discord
import logging
import importlib.util
from glob import glob
from typing import Iterable
dir_name, name_file = os.path.split(__file__)


def import_module_from_file(full_path_to_module):
    # Get module name and path from full path
    module_dir, module_file = os.path.split(full_path_to_module)
    module_name, module_ext = os.path.splitext(module_file)

    # Get module "spec" from filename
    spec = importlib.util.spec_from_file_location(module_name, full_path_to_module)

    return spec.loader.load_module()


class Client(discord.Client):

    def __init__(self, prefix="!"):
        self.commands = {}
        self.PREFIX = prefix
        self.logger = logging.getLogger("discord.rizthme")
        discord.Client.__init__(self, intents=discord.Intents.all())

    def load(self):
        """
        Initialise all commands and events
        """
        self._init_directory("events")
        self._init_directory("commands")

    def _init_directory(self, directory: str):
        """
        Initialise all events
        """
        path = os.path.join(dir_name, directory)
        list_module = [
            import_module_from_file(path) for path in glob(os.path.abspath(path) + '/*.py')
            if not "__" in path
        ]
        for module in list_module:
            init = getattr(module, 'init')
            init(self)

    def command(self, alias: Iterable[str]):
        """
        add a function to all aliases.

        This function is call when a message started with the alias is sent on a discord textual channel
        :param alias: List[str], list of command, callable with a discord.Message (Without PREFIX)
        """
        def decorator(f):
            """
            :param f: Callable, function to call when the alias is sent in a message.
            """
            for name in alias:
                if name in self.commands:
                    raise ValueError(f"Command {name} already exists")
                self.commands[name] = f
            return f
        return decorator
