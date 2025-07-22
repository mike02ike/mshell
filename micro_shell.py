import os
import sys

def process_input(user_input):
    if " | " in user_input:
        handle_pipe(user_input)
    elif user_input.startswith("file"): 
        filename = user_input.split()[1]
        handle_file_input(filename)
    else:
        handle_command(user_input)

def handle_pipe(user_input):
    commands = user_input.split(" | ")
    previous_fd = None  # File descriptor for previous command's read end

    for i, cmd in enumerate(commands):
        parts = cmd.strip().split()
        command = parts[0]
        args = parts[1:]

        if i < len(commands) - 1:  # If not the last command
            read_fd, write_fd = os.pipe()
        else:
            read_fd, write_fd = None, None

        execute_command(command, args, False, False, False, None, None, previous_fd, write_fd)

        if previous_fd is not None:
            os.close(previous_fd)  # Close previous command's read end
        
        previous_fd = read_fd  # Update previous_fd for next iteration

def handle_file_input(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith("#"):  # Skip comments
                    continue
                user_input = line.strip()
                if user_input:  # Only process non-empty lines
                    print(f"Executing command from file: {user_input}")
                    handle_command(user_input)
    except FileNotFoundError:
        print(f"File not found: {filename}")

def handle_command(user_input):
    args = user_input.split()  # Split input into command + arguments
    command = args[0]
    args = args[1:]

    background = False
    if args and args[-1] == "&":
        background = True
        args = args[:-1]  # Remove "&" from args

    output_redirect = False
    input_redirect = False
    output_file = None
    input_file = None
        
    if ">" in args:
        try:
            output_redirect = True
            output_file = args[args.index(">") + 1]
        except IndexError:
            print("Output redirection symbol '>' not followed by a file name.")
            return

    if "<" in args:
        try:
            input_redirect = True
            input_file = args[args.index("<") + 1]
        except IndexError:
            print("Input redirection symbol '<' not followed by a file name.")
            return

    if command == "cd":
        handle_cd(args)
    elif command == "inspiration":
        handle_inspiration()
    else:
        execute_command(command, args, output_redirect, background, input_redirect, input_file, output_file)

def handle_cd(args):
    try:
        if len(args) == 0:
            os.chdir(os.environ["HOME"])
        elif len(args) == 1:
            os.chdir(args[0])
        else:
            print("cd takes one argument")
    except FileNotFoundError:
        print(f"No such directory: {args[0]}")

def handle_inspiration():
    os.environ["phrase"] = "We're almost at the finish line!"
    print(os.environ["phrase"])

def execute_command(command, args, output_redirect=None, background=None, input_redirect=None, input_file=None, output_file=None, is_pipe=False, read_fd=None, write_fd=None):
    pid = os.fork()
    
    if pid < 0:  # Fork failed
        print("Fork failed")
        return
    
    elif pid == 0:  # Child process
        if read_fd is not None:  # If there's a pipe input, redirect stdin
            os.dup2(read_fd, 0) # Redirect stdin to read end of pipe
            os.close(read_fd)
        
        if write_fd is not None:  # If there's a pipe output, redirect stdout
            os.dup2(write_fd, 1) # Redirect stdout to write end of pipe
            os.close(write_fd)
        
        if input_redirect:
            try:
                fd = os.open(input_file, os.O_RDONLY)  # Open file for reading
                os.dup2(fd, 0)  # Redirect stdin to file
                os.close(fd)  # Close file descriptor
                
                args = args[:args.index("<")]  # Remove "<" and filename from args
            except (IndexError, FileNotFoundError):
                print("Error: Invalid input redirection syntax")
                sys.exit(1)
        
        if output_redirect:
            try:
                fd = os.open(output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)  # Open file for writing
                os.dup2(fd, 1)  # Redirect stdout to file
                os.close(fd)  # Close file descriptor
                
                args = args[:args.index(">")]  # Remove ">" and filename from args
            except (IndexError, FileNotFoundError):
                print("Error: Invalid output redirection syntax")
                sys.exit(1)

        directories = os.environ["PATH"].split(":")  # Get system PATH directories
        for directory in directories:
            try:
                os.execv(f"{directory}/{command}", [command] + args)
            except FileNotFoundError:
                continue
            except OSError:
                print(f"{command}: Not executable")
                
        print(f"Command not found: {command}")
        sys.exit(1)
    
    else:  # Parent process
        if read_fd is not None:
            os.close(read_fd)  # Close read end in parent
        elif write_fd is not None:
            os.close(write_fd)  # Close write end in parent
        elif not background:
            os.wait()  # Wait for child process to finish
        else:
            print(f"Parent, Child PID: {pid} (Background task)")

def main():
    if len(sys.argv) > 1:  # Check if a file argument is given
        handle_file_input(sys.argv[1])
        return
    while True:
        sys.stdout.flush()
        user_input = input("\nmshell$ ")
        
        if user_input == "quit":
            break
        if user_input == "":
            continue
        
        process_input(user_input)

if __name__ == "__main__":
    main()