from imgui_bundle import imgui, portable_file_dialogs as pfd

class FileDialogController:
    def __init__(self):
        self.open_file_handle = None
        self.result_callback = lambda x: print(f"Result: {x}")  # Default callback

    def open(self, title="Select File", multiselect=True):
        options = pfd.opt.multiselect if multiselect else pfd.opt.none
        self.open_file_handle = pfd.open_file(title, options=options)

    def render(self):
        if self.open_file_handle and self.open_file_handle.ready():
            results = self.open_file_handle.result()
            if isinstance(results, list):
                for path in results:
                    if self.result_callback:
                        self.result_callback(path)
            else:
                if self.result_callback:
                    if callable(self.result_callback):
                        self.result_callback(results)
            self.open_file_handle = None