from imgui_bundle import imgui
from views import Panel


class CalculatorPanel(Panel):
    def render(self):
        changed_a, self.view_model.data.a = imgui.input_float("A", self.view_model.data.a)
        changed_b, self.view_model.data.b = imgui.input_float("B", self.view_model.data.b)
        changed_op, op_index = imgui.combo(
            "Operator",
            ["+", "-", "*", "/", "^"].index(self.view_model.data.operation),
            ["+", "-", "*", "/", "^"],
        )
        if changed_op:
            self.view_model.data.operation = ["+", "-", "*", "/", "^"][op_index]

        if imgui.button("Compute"):
            self.view_model.compute()

        if self.view_model.data.result is not None:  
            imgui.text(f"Result: {self.view_model.data.result}")
