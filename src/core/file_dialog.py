from imgui_bundle import imgui, portable_file_dialogs as pfd

class FileDialogController:
    def __init__(self):
        self.open_file_handle = None
        self.result_callback = lambda path: print(f"Result: {path}")  # Default callback
        

    def open_files(self, title="Select File", multiselect=True):
        options = pfd.opt.multiselect if multiselect else pfd.opt.none
        self.open_file_handle = pfd.open_file(title, options=options)
    def open_folder(self, title="Select Folder"):
        self.open_file_handle = pfd.select_folder(title)
    def save_file(self, title="Save File", default_path="", filters=None):
        if filters is None:
            filters = ["*.*"]
        self.open_file_handle = pfd.save_file(title, default_path, filters=filters)
        
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