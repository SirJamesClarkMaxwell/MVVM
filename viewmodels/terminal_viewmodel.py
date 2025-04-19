from data.terminal_data import TerminalData
from models.terminal_model import TerminalModel

class TerminalViewModel:
    def __init__(self,app,*args,**kwargs):
        self.model = TerminalModel()
        self.data = TerminalData()
    def run_command(self):
        cmd = self.data.terminal_input.strip()
        if not cmd:
            return

        self.data.terminal_history.append(cmd)
        output = self.model.execute_command(cmd)
        self.data.terminal_output += f"> {cmd}\n{output}\n"
        self.data.terminal_input = ""

