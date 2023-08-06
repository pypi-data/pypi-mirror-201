"""
This module contains scrapyio 'settings' tests
and ensures that configuration file loading
and scrapyio configurations work as expected.
"""

import pytest


def test_config_loading_without_test_env(monkeypatch, clear_sys_modules):
    monkeypatch.delenv("TESTING")
    with pytest.raises(ModuleNotFoundError):
        __import__("scrapyio.settings")


def test_config_loading_with_test_env(monkeypatch, clear_sys_modules):
    monkeypatch.setenv("TESTING", "TRUE")
    mod = __import__("scrapyio.settings")
    CONFIGS = mod.settings.CONFIGS
    assert CONFIGS.__name__ == "scrapyio.templates.configuration_template"
