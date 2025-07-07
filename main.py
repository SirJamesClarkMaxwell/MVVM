import sys
from app import App
from imgui_bundle import hello_imgui,imgui


def main(*args):
    print(*args)
    with App(*args) as app:
        app.run()
    # app = App()
    # app.run()
    # app.shutdown()

if __name__ == "__main__":
    # main(*sys.argv[1:])
    main("--path","R27.json")
