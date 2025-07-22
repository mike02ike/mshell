import argparse
import re

def handle_chat():
    # code for chatting with chatbot
    reply = ""
    print("System: Hello, are you male or female?")

    reply = input("User: ")
    handle_reply(reply)

    reply = input("User: ")
    handle_reply(reply)

    reply = input("User: ")
    handle_reply(reply)

def handle_reply(reply):
    # this function handles the logic for each reply
    # it's used for both modes
    if reply == "female":
        print("System: How excellent! Are you a CS major!")
    elif reply == "male":
        print("System: Me too. Are you a CS major?")
    elif reply == "no":
        print("System: Too bad. Anyway, what's an animal you like, and two you don't?")
    elif reply == "yes":
        print("System: Excellent, I am too. What's an animal you don't like, and two you do?")
    else:
        #regex to separate reply by spaces and commas
        words = re.split(r'[ ,]+', reply)
        print(f"System: {words[0]} are awesome, but I hate {words[-1]} too. Bye for now.")

def handle_read(filename):
    # code for reading user-side commands from a file
    reply = ""

    print("System: Hello, are you male or female?")

    # open the file for reading
    with open(filename, "r") as file:
        # read each line and store it in 'reply'
        for line in file:
            reply = line.strip()  # use strip() to remove any trailing newline characters
            print(reply)
            handle_reply(reply)

def main():
    # create the argument parser
    parser = argparse.ArgumentParser(description="Select between two modes: chat or read")

    # create subparsers for the two modes
    subparsers = parser.add_subparsers(dest="mode", help="Modes of operation")

    # subparser for 'chat' mode
    subparsers.add_parser("chat", help="Chat with the chatbot")

    # subparser for 'read' mode
    read_parser = subparsers.add_parser("read", help="Read a file with commands")
    read_parser.add_argument("filename", type=str, help="The name of the file to read")

    # parse the arguments
    args = parser.parse_args()

    # logic for each mode
    if args.mode == "chat":
        handle_chat()
    elif args.mode == "read":
        handle_read(args.filename)
    else:
        print("Please select a valid mode: chat or read")

if __name__ == "__main__":
    main()


