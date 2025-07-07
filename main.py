import sys
from app import App
from imgui_bundle import hello_imgui,imgui


def main(*args):
    with App(*args) as app:
        app.run()


if __name__ == "__main__":
    main(*sys.argv[1:])
    # main("--path","R27.json")
