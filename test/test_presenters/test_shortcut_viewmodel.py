import os
import pytest
from unittest.mock import patch, MagicMock
from src.core.shortcuts.shortcut import Shortcut, ShortcutBinding
from presenters.shortcut_presenter import ShortcutPresenter
from src.core.shortcuts.shortcut import Shortcut


class DummyApp:
    pass


@pytest.fixture
def presenter():
    return ShortcutPresenter(app=DummyApp())


def test_check_binding_conditions_valid_list(presenter):
    shortcuts = [
        Shortcut(
            id="open_file",
            keys=["Ctrl+O"],
            category="File",
            context=["Global"],
            description="Open a file",
            enable_threading=False
        ),
        Shortcut(
            id="save_file",
            keys=["Ctrl+S"],
            category="File",
            context=["Global"],
            description="Save a file",
            enable_threading=False
        ),
    ]
    bindings = [
        ShortcutBinding(id="open_file"),
        ShortcutBinding(id="save_file"),
    ]

    result, message = presenter._check_binding_conditions(
        bingings=bindings, shortcut=shortcuts
    )
    assert result is True
    assert message == "Binding conditions are met"


def test_check_binding_conditions_valid_individual(presenter):
    shortcut = Shortcut(
        id="open_file",
        keys=["Ctrl+O"],
        category="File",
        context=["Global"],
        description="Open a file",
        enable_threading=False,
    )
    binding = ShortcutBinding(id="open_file")

    result, message = presenter._check_binding_conditions(
        bingings=binding, shortcut=shortcut
    )
    assert result is True
    assert message == "Binding conditions are met"


def test_check_binding_conditions_length_mismatch(presenter):
    shortcuts = [
        Shortcut(
            id="open_file",
            keys=["Ctrl+O"],
            category="File",
            context=["Global"],
            description="Open a file",
            enable_threading=False,
        )
    ]
    bindings = [
        ShortcutBinding(id="open_file"),
        ShortcutBinding(id="save_file"),  # Extra binding
    ]

    result, message = presenter._check_binding_conditions(
        bingings=bindings, shortcut=shortcuts
    )
    assert result is False
    assert message == "Binding conditions are not met, length mismatch"


def test_check_binding_conditions_invalid_list_types(presenter):
    # Pass a list, but wrong types inside
    bindings = ["invalid_binding"]
    shortcuts = ["invalid_shortcut"]

    result, message = presenter._check_binding_conditions(
        bingings=bindings, shortcut=shortcuts
    )
    assert result is False
    assert "list has invalid types" in message


def test_check_binding_conditions_invalid_totally(presenter):
    # Completely wrong types
    result, message = presenter._check_binding_conditions(
        bingings="invalid", shortcut=123
    )
    assert result is False
    assert (
        message
        == "Binding conditions are not met, expected either both lists or both single objects"
    )
def test_load_from_file_file_not_exists(presenter):
    with patch("os.path.exists", return_value=False):
        result = presenter.load_from_file("non_existent_file.json")
        assert result is None
def test_load_from_file_success(presenter):
    mock_shortcut = MagicMock(spec=Shortcut)
    with (
        patch("os.path.exists", return_value=True),
        patch(
            "src.core.shortcuts.ShortcutManager.load_from_file",
            return_value=[mock_shortcut],
        ),
    ):

        result = presenter.load_from_file("valid_file.json")
        assert result == [mock_shortcut]
def test_load_from_file_os_error(presenter):
    with patch("os.path.exists", return_value=True), patch(
        "src.core.shortcuts.ShortcutManager.load_from_file", side_effect=OSError("Error")
    ):
        result = presenter.load_from_file("valid_file.json")
        assert result is None

@pytest.fixture
def shortcut_presenter():
    mock_app = MagicMock()
    return ShortcutPresenter(mock_app)

def test_bind_shortcut_valid(shortcut_presenter):
    shortcuts = [
        Shortcut(id="bind1", keys="Ctrl+A", category="General", context="Global", description="Test shortcut 1",enable_threading=False),
        Shortcut(id="bind2", keys="Ctrl+B", category="General", context="Global", description="Test shortcut 2",enable_threading=False)
    ]
    bindings = [ShortcutBinding(id="bind1"), ShortcutBinding(id="bind2")]

    shortcut_presenter.bind_shortcut(to_bind=shortcuts, bindings=bindings)

    for shortcut, binding in zip(shortcuts, bindings):
        assert shortcut.bingings == binding

def test_bind_shortcut_invalid_conditions(shortcut_presenter):
    shortcuts = [
        Shortcut(
            id="bind1",
            keys="Ctrl+A",
            category="General",
            context="Global",
            description="Test shortcut 1",
            enable_threading=False,
        )
    ]
    bindings = [ShortcutBinding(id="bind2")]

    shortcut_presenter.bind_shortcut(to_bind=shortcuts, bindings=bindings)

    for shortcut in shortcuts:
        assert shortcut.bingings is None

def test_export_shortcuts_valid(shortcut_presenter, tmp_path):
    export_path = tmp_path / "exported_shortcuts.json"
    shortcut_presenter.export_shortcuts(path=str(export_path))

    assert export_path.exists()

def test_export_shortcuts_invalid_path(shortcut_presenter):
    invalid_path = "invalid:/path/exported_shortcuts.json"

    with pytest.raises(OSError):
        shortcut_presenter.export_shortcuts(path=invalid_path)
