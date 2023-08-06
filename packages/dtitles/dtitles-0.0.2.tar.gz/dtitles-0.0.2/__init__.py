import ctypes

def title(input: str):
    ctypes.windll.kernel32.SetConsoleTitleA(input.encode('ascii'))