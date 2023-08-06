import pathlib
import platform
import subprocess


class Clipboard:

    def __init__(self, ):
        self.os = platform.system()
        if self.os == "Windows":
            self._copy = self.copy_windows
        elif self.os == "Darwin":
            self._copy = self.copy_darwin
        elif self.os == "Linux":
            self._copy = self.copy_linux
        else:
            raise OSError(f"Unsupported platform {self.os}")

    def copy(self, file: pathlib.Path):
        self._copy(file)

    def copy_windows(self, file: pathlib.Path):
        raise NotImplementedError("Copy for Windows is not implemented")

    def copy_darwin(self, file: pathlib.Path):
        cmd = f"""osascript -e 'set the clipboard to (read (POSIX file "{file.absolute()}") as""" + "{«class PNGf»})'"
        subprocess.run(cmd, shell=True)

    def copy_linux(self, file: pathlib.Path):
        cmd = f"""xclip -selection clipboard -t image/png -i {file.absolute()}"""
        subprocess.run(cmd, shell=True)
