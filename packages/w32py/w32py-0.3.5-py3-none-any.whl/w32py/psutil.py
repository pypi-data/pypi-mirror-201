from psutil import process_iter


def isRunning(names: set[str]) -> bool:
    for proc in process_iter():
        if proc.name() in names:
            return True
    return False
