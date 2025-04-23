import subprocess


class TerminalModel:
    def __init__(self):
        self.shell_prefix = ["wsl"]  # You can also use ["wsl.exe"] if needed

    def execute_command(self, command: str) -> str:
        try:
            result = subprocess.check_output(
                self.shell_prefix + [command],
                shell=False,  # keep False for list style
                stderr=subprocess.STDOUT,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            result = e.output
        return result
