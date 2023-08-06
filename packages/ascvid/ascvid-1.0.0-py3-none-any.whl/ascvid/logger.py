import colorama
import sys
colorama.init()

def print_error(err_message):
    print(f"{colorama.Fore.LIGHTRED_EX}   ascvid: !! [ERROR] !!\n{err_message}{colorama.Fore.RESET}",file=sys.stderr)
def print_warning(warning,ask=None):
    print(f"{colorama.Fore.LIGHTYELLOW_EX}   ascvid: ! [WARNING] !\n{warning}{colorama.Fore.RESET}",file=sys.stderr)
    if ask is not None:
        print(f"{colorama.Fore.LIGHTCYAN_EX} ascvid: ? [DIALOG] ? => {ask} ?{colorama.Fore.RESET}",file=sys.stderr,end=None)
        return input()

