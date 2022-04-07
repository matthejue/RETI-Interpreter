from colorama import Style, Fore


class _ColorManager:
    _instance = None

    def color_off(self):
        self.BLACK = (
            self.RED
        ) = (
            self.GREEN
        ) = (
            self.YELLOW
        ) = self.BLUE = self.MAGENTA = self.CYAN = self.WHITE = self.RESET = ""
        self.BRIGHT = self.RESET_ALL = ""

    def color_on(self):
        self.BLACK = Fore.BLACK
        self.RED = Fore.RED
        self.GREEN = Fore.GREEN
        self.YELLOW = Fore.YELLOW
        self.BLUE = Fore.BLUE
        self.MAGENTA = Fore.MAGENTA
        self.CYAN = Fore.CYAN
        self.WHITE = Fore.WHITE
        self.RESET = Fore.RESET
        self.BRIGHT = Style.BRIGHT
        self.NORMAL = Style.NORMAL
        self.RESET_ALL = Style.RESET_ALL


def ColorManager():
    if _ColorManager._instance is None:
        _ColorManager._instance = _ColorManager()
    return _ColorManager._instance
