import platform

def is_windows() -> bool:
    """Test if the used device is windows.
    
    :return: True if it's windows, else False
    """
    return platform.system()=='Windows'