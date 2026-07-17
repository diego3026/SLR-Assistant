class ConsoleService:

    def __init__(self):
        self.console = None

    def bind(self, console):
        self.console = console

    def info(self, text):
        if self.console:
            self.console.append(text, "info")

    def success(self, text):
        if self.console:
            self.console.append(text, "success")

    def warning(self, text):
        if self.console:
            self.console.append(text, "warning")

    def error(self, text):
        if self.console:
            self.console.append(text, "error")

console = ConsoleService()