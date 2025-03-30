
from app import App
from imgui_bundle import hello_imgui

def main():
    app = App()
    runner_params = app.initialize()
    hello_imgui.run(runner_params)

if __name__ == "__main__":
    main()
