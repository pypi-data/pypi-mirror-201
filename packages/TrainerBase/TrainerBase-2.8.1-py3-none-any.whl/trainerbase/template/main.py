import os


from scripts import script_engine, system_script_engine
from gui import run_menu


def start_script_engines():
    system_script_engine.start()
    script_engine.start()


def main():
    run_menu(on_initialized=start_script_engines)
    os._exit(0)


if __name__ == "__main__":
    main()
