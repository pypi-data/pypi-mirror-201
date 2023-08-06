import dearpygui.dearpygui as dpg

from trainerbase.gui import add_script_to_gui, add_gameobject_to_gui, add_codeinjection_to_gui, simple_trainerbase_menu
from scripts import *
from objects import *
from injections import *


@simple_trainerbase_menu("Trainer Base", 800, 600)
def run_menu():
    with dpg.tab_bar():
        # (!) Example:
        #
        # with dpg.tab(label="Scripts", tag="scripts"):
        #     add_script_to_gui(script, "Readable Name")
        #
        # with dpg.tab(label="Objects", tag="objects"):
        #     add_gameobject_to_gui(game_object, "Readable Name")
        #
        # with dpg.tab(label="Code Injections", tag="code_injections"):
        #     add_codeinjection_to_gui(injection, "Injection Name")

        ...
