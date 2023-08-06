from sys import argv
from typing import Any

from PyQt5.QAxContainer import QAxWidget  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
from pythoncom import (  # pylint: disable=no-name-in-module
    CoInitialize,
    CoUninitialize,
    PumpWaitingMessages,
)
from win32com.client import Dispatch, WithEvents


def coInitialize() -> None:
    CoInitialize()


def coUninitialize() -> None:
    CoUninitialize()


def pumpWaitingMessages() -> bool:
    WM_QUIT = PumpWaitingMessages()
    return not WM_QUIT


def dispatch(clsid: Any) -> Any:
    return Dispatch(clsid)


def withEvents(obj: Any, user_event_class: Any) -> Any:
    return WithEvents(obj, user_event_class)


def qAxWidget(control: str) -> QAxWidget:
    return QAxWidget(control)


def qApplication() -> QApplication:
    return QApplication(argv)
