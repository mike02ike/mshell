
#!/usr/bin/env python3
#shebang

#my comments are all mine and im displaying my learning as I go, thanks

import os #holds process related functions like fork, execv and waitpid
import sys

def runcmd(cmd):
    pid = os.fork() #create new process
    if pid == 0: #if the created process is a child process
        try:
            print(f"Executing command: {cmd}")
            os.execv(cmd[0], cmd)
        except FileNotFoundError:
            print(f"Command {cmd[0]} not found!")
            sys.exit(1) #if the file is not found it sends FileNotFoundError, this handles that.
    return pid #add new process to list of processes


def main ():
    #defining commands as a list where its elements are the parameters of the commands
    commands = [
        #["/bin/cat", "/proc/cpuinfo"], this doesnt work because im using macos so i had to find the macos equivilent
        ["/usr/sbin/sysctl", "-n", "machdep.cpu.brand_string"],
        ["/bin/echo", "Hello World"],
        ["/usr/bin/python3", "spinner.py", "1000000"],
        ["/usr/bin/uname", "-a"]
    ]

    pids = []
    for cmd in commands:
        pids.append(runcmd(cmd))

    for pid in pids:
        os.waitpid(pid, 0)#wait for all the child process to complete

    runcmd(["/usr/bin/python3", "./spinner.py", "2000000"])


if __name__ == "__main__":
    main()

