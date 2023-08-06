from pywinauto import Application


def startApplication(cmd: str, backend: str = "win32") -> Application:
    return Application(backend=backend).start(cmd)
