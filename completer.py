from typing import List

import readline


class Completer:
    def __init__(self, commands: List[str], sites: List[str]) -> None:
        self.commands = commands
        self.sites = sites

        self.all_options = self.commands + self.sites

        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.completer)


    def completer(self, text, state):
        options = [i for i in self.all_options if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None
