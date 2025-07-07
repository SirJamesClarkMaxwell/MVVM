
from app import App
from imgui_bundle import hello_imgui,imgui


def main():

    with App() as app:
        app.run()
    # app = App()
    # app.run()
    # app.shutdown()

if __name__ == "__main__":
    main()
