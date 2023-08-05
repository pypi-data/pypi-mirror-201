from typing import Callable

import dearpygui.dearpygui as dpg
import keyboard

from trainerbase import scriptengine
from trainerbase import gameobject
from trainerbase import codeinjection
from trainerbase.common import Teleport


def simple_trainerbase_menu(window_title: str, width, height):
    def menu_decorator(initializer: Callable):
        def run_menu_wrapper(on_initialized: Callable):
            dpg.create_context()
            dpg.create_viewport(
                title=window_title,
                min_width=width,
                min_height=height,
                width=width,
                height=height,
            )
            dpg.setup_dearpygui()

            with dpg.window(
                label=window_title,
                tag="menu",
                min_size=[width, height],
                no_close=True,
                no_move=True,
                no_title_bar=True,
                horizontal_scrollbar=True,
            ):
                initializer()

            dpg.show_viewport()

            on_initialized()

            dpg.start_dearpygui()
            dpg.destroy_context()

        return run_menu_wrapper

    return menu_decorator


def add_script_to_gui(
    script: scriptengine.Script,
    label: str,
    hotkey: str = None,
):
    def on_script_state_change():
        script.enabled = dpg.get_value(script.dpg_tag)

    if hotkey is not None:

        def on_hotkey_press():
            dpg.set_value(script.dpg_tag, not dpg.get_value(script.dpg_tag))
            on_script_state_change()

        keyboard.add_hotkey(hotkey, on_hotkey_press)

        label = f"[{hotkey}] {label}"

    dpg.add_checkbox(label=label, tag=script.dpg_tag, callback=on_script_state_change, default_value=script.enabled)


def add_gameobject_to_gui(
    gameobject: gameobject.GameObject,
    label: str,
    hotkey: str = None,
    before_set: Callable = int,
):
    def on_frozen_state_change():
        gameobject.frozen = gameobject.value if dpg.get_value(gameobject.dpg_tag_frozen) else None

    def on_value_set():
        raw_new_value = dpg.get_value(gameobject.dpg_tag_setter)
        if not raw_new_value:
            return

        new_value = before_set(raw_new_value)

        if gameobject.frozen is None:
            gameobject.value = new_value
        else:
            gameobject.frozen = new_value

    if hotkey is not None:

        def on_hotkey_press():
            dpg.set_value(gameobject.dpg_tag_frozen, not dpg.get_value(gameobject.dpg_tag_frozen))
            on_frozen_state_change()

        keyboard.add_hotkey(hotkey, on_hotkey_press)

        label = f"[{hotkey}] {label}"

    with dpg.group(horizontal=True):
        dpg.add_checkbox(tag=gameobject.dpg_tag_frozen, callback=on_frozen_state_change)
        dpg.add_text(label)
        dpg.add_input_text(width=220, tag=gameobject.dpg_tag_getter, readonly=True)
        dpg.add_input_text(width=220, tag=gameobject.dpg_tag_setter, hint="Set value here")
        dpg.add_button(label="Set", callback=on_value_set)


def add_codeinjection_to_gui(
    injection: codeinjection.CodeInjection,
    label: str,
    hotkey: str = None,
):
    def on_codeinjection_state_change():
        if dpg.get_value(injection.dpg_tag):
            injection.inject()
        else:
            injection.eject()

    if hotkey is not None:

        def on_hotkey_press():
            dpg.set_value(injection.dpg_tag, not dpg.get_value(injection.dpg_tag))
            on_codeinjection_state_change()

        keyboard.add_hotkey(hotkey, on_hotkey_press)

        label = f"[{hotkey}] {label}"

    dpg.add_checkbox(label=label, tag=injection.dpg_tag, callback=on_codeinjection_state_change)


def add_teleport_to_gui(tp: Teleport, hotkey_save_position: str = None, hotkey_set_saved_position: str = None):
    tag_teleport_labels = "teleport_labels"
    should_add_save_set_position_hotkeys = hotkey_save_position is not None and hotkey_set_saved_position is not None

    def on_goto_label():
        tp.goto(dpg.get_value(tag_teleport_labels))

    def on_clip_coords():
        dpg.set_clipboard_text(repr(tp.get_coords()))

    if should_add_save_set_position_hotkeys:
        saved_position = None

        def on_hotkey_save_position_press():
            nonlocal saved_position
            saved_position = tp.get_coords()

        def on_hotkey_set_saved_position_press():
            if saved_position is not None:
                tp.set_coords(*saved_position)

        keyboard.add_hotkey(hotkey_save_position, on_hotkey_save_position_press)
        keyboard.add_hotkey(hotkey_set_saved_position, on_hotkey_set_saved_position_press)

    with dpg.tab(label="Teleport", tag="tab_teleport"):
        if should_add_save_set_position_hotkeys:
            dpg.add_text(f"[{hotkey_save_position}] Save Position")
            dpg.add_text(f"[{hotkey_set_saved_position}] Set Saved Position")

        add_gameobject_to_gui(tp.player_x, "X", before_set=float)
        add_gameobject_to_gui(tp.player_y, "Y", before_set=float)
        add_gameobject_to_gui(tp.player_z, "Z", before_set=float)

        labels = sorted(tp.labels.keys())
        with dpg.group(horizontal=True):
            dpg.add_button(label="Go To", callback=on_goto_label)
            dpg.add_combo(label="Labels", tag=tag_teleport_labels, items=labels, default_value=labels[0])

        dpg.add_button(label="Clip Coords", callback=on_clip_coords)
