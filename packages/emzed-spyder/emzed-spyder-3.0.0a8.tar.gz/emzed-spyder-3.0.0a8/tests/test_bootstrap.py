#! /usr/bin/env python
# Copyright 2020 Uwe Schmitt <uwe.schmitt@id.ethz.ch>

import subprocess
import sys
import time
import types

import pytest


@pytest.fixture(scope="function")
def with_fake_emzed():
    fake_emzed = types.ModuleType("fake_emzed")
    sys.modules["emzed"] = fake_emzed
    yield
    del sys.modules["emzed"]


def test_bootstrap(tmp_path):
    temp_venv_folder = tmp_path
    from emzed_spyder import utils

    utils.setup_venv_for_remote_interpreter(temp_venv_folder)

    started = time.time()
    utils.setup_venv_for_remote_interpreter(temp_venv_folder)
    assert time.time() - started < 10

    local_python_path = str(utils.python_executable_in(temp_venv_folder))
    subprocess.check_call([local_python_path, "-c", "'import emzed, emzed_gui'"])


def test_project_new(tmp_path, monkeypatch, with_fake_emzed):

    # patch stuff to use different temporary folders:
    import emzed_spyder.utils as utils

    sys.modules["emzed_spyder.utils"].emzed_projects = tmp_path / "emzed3_projects"
    sys.modules["emzed_spyder.utils"].emzed_folder = tmp_path / "emzed3"

    import emzed_spyder.remote_interpreter_startup as r

    r._utils = utils

    def fake_get_ipython():
        return fake_ipython()

    class fake_ipython:
        def find_magic(self, name):
            return fake_edit

    edit_called = False

    def fake_edit(name):
        nonlocal edit_called
        edit_called = True

    __builtins__["get_ipython"] = fake_get_ipython

    r.emzed_project_new("abc")

    assert edit_called
