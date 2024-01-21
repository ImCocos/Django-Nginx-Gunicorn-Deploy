class Painter:
    END = '\33[0m'
    GREY = '\33[90m'
    RED = '\33[91m'
    GREEN = '\33[92m'
    YELLOW = '\33[93m'
    BLUE = '\33[94m'

    def __call__(self, text: str, color) -> str:
        return color + text + self.END
