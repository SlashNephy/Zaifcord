# coding=utf-8
import colorama
from colorama import Back, Fore

colorama.init(autoreset=True)

class Utils:
    @classmethod
    def printError(cls, message: str, critical: bool=False) -> None:
        print(f"{Back.RED}[Error]{Back.RESET} {message}")
        if critical:
            exit(1)

    @classmethod
    def printInfo(cls, message: str) -> None:
        print(f"{Back.BLUE}[Info]{Back.RESET} {message}")

    @classmethod
    def printDebug(cls, message: str) -> None:
        print(f"{Back.GREEN}[Debug]{Back.RESET} {Fore.LIGHTBLACK_EX}{message}{Fore.RESET}")
