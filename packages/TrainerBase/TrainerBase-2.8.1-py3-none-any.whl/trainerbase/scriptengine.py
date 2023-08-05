import typing
import threading
import time
import uuid

import pymem
import dearpygui.dearpygui as dpg
from trainerbase.gameobject import GameObject


class Script:
    DPG_TAG_PREFIX = "script__"

    def __init__(self, callback: typing.Callable, enabled: bool = False):
        self.callback = callback
        self.enabled = enabled
        self.dpg_tag = f"{Script.DPG_TAG_PREFIX}{uuid.uuid4()}"

    def __repr__(self):
        return (
            f"<Script {getattr(self.callback, '__name__', 'Anon')}:"
            f" enabled={self.enabled},"
            f" dpg_tag={repr(self.dpg_tag)}"
            f">"
        )

    def __call__(self):
        return self.callback()


class ScriptEngine:
    def __init__(self, delay: float = 0.05):
        self.delay = delay
        self.should_run = False
        self.thread = threading.Thread(target=self.script_loop)
        self.scripts = []

    def __repr__(self):
        return (
            "<ScriptEngine" f" delay={self.delay}" f" should_run={self.should_run}" f" scripts={len(self.scripts)}" ">"
        )

    def start(self):
        self.should_run = True
        self.thread.start()

    def stop(self):
        self.should_run = False
        self.thread.join()

    def script_loop(self):
        while self.should_run:
            try:
                for script in self.scripts:
                    if script.enabled:
                        script()
            except (pymem.exception.MemoryReadError, pymem.exception.MemoryWriteError):
                continue
            except Exception as e:
                print(e)
                self.stop()
            time.sleep(self.delay)

    def register_script(self, script: Script) -> Script:
        self.scripts.append(script)
        return script

    def simple_script(self, executor: typing.Callable) -> Script:
        script = Script(executor)
        self.register_script(script)
        return script


system_script_engine = ScriptEngine()


@system_script_engine.simple_script
def update_frozen_objects():
    for game_object in GameObject.updated_objects:
        if game_object.frozen is not None:
            game_object.value = game_object.frozen


@system_script_engine.simple_script
def update_displayed_objects():
    for game_object in GameObject.updated_objects:
        if dpg.does_alias_exist(game_object.dpg_tag_getter):
            dpg.set_value(game_object.dpg_tag_getter, game_object.value)


update_frozen_objects.enabled = True
update_displayed_objects.enabled = True
