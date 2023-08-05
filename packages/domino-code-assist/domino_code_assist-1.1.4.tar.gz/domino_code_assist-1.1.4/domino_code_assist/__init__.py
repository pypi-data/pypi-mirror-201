"""Dominocode"""

__version__ = "1.1.4"

import os

# isort: skip_file

import domino_code_assist.logging_workaround

from . import data
from .assistant import init
from .components import MarkdownFromCell, CardGridLayout


try:
    if not os.environ.get("DOMINO_PROJECT_ID"):
        from dotenv import load_dotenv

        load_dotenv()
except ImportError:
    pass


def _prefix():
    import sys
    from pathlib import Path

    prefix = sys.prefix
    here = Path(__file__).parent
    # for when in dev mode
    if (here.parent / "prefix").exists():
        prefix = str(here.parent)
    return prefix


def _jupyter_labextension_paths():
    return [
        {
            "src": f"{_prefix()}/prefix/share/jupyter/labextensions/domino-code-assist/",
            "dest": "domino-code-assist",
        }
    ]


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": f"{_prefix()}/prefix/share/jupyter/nbextensions/domino-code-assist/",
            "dest": "domino-code-assist",
            "require": "domino-code-assist/extension",
        }
    ]


def _jupyter_server_extension_points():
    return [
        {
            "module": "myextension.app",
        }
    ]
