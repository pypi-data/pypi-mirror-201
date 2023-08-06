import subprocess
import shutil
import sys
import shlex
from .logger import print_error
UNIX_XTERM_SYNTAX = ["konsole","rxvt","uxterm","xterm -bg black -fg white"]
def get_term_cmd():
    if sys.platform=="win32":
        return "start \'\' \'{}\'"
    elif sys.platform=="darwin":
        return "open -W -a Terminal.app \'{}\'"
    elif sys.platform.lower().startswith("linux"):
        if shutil.which("gnome-terminal"):
            return "gnome-terminal -x \'{}\'"
        for term in UNIX_XTERM_SYNTAX:
            if shutil.which(term):
                return f"{term} -e \'{{}}\'"

def run_term(cmd,term_cmd=None):
    if term_cmd is None:
        term_cmd=get_term_cmd()
        if term_cmd is None:
            print_error(f"We could not find a terminal for you! Current terminal list: {UNIX_XTERM_SYNTAX}. If your terminal is not there, specify the terminal you are using with --term option. \n If you think this is an error with ascvid, please use the GitHub issue tracker.")
            exit(1)
    term=term_cmd.format(cmd)
    print(shlex.split(term))
    popen=subprocess.Popen(shlex.split(term),stderr=subprocess.PIPE)
    stderr_out,*_=popen.communicate()
    if popen.returncode!=0:
        print_error(f"Command {term} failed with returncode {popen.returncode}! STDERR output: \n{stderr_out}")
