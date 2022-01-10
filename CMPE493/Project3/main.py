import sys
from utils import *
from model import Library


class LibraryAPI:
    def __init__(self):
        self.isTerminated = False

    def retrieve_input(self):
        '''
        Retrieving input from stdin by the user.
        '''
        command = input(">>> ")
        return command

    def display_info(self):
        '''
        - Displays a greeting message and explains the vision
        behind the application and API.
        '''
        print("Welcome to Libraria API.")
        print("Here you can create your own library,")
        print("and get recommendations by our system.")
        print("Before start using Libraria, please")
        print("specify the recommendations count.")

    def display_help(self):
        '''
        - Display tool for showing available commands as a help
        section in the API. 
        '''
        print("Available commands in Libraria:")
        print("- help: Displays `help`.")
        print("- load <file_path>: Loads the list of")
        print("\tbooks, which are described as book urls.")
        print("- query single <book_url>: Queries the")
        print("\tsingle book and displays statistics")
        print("\tand recommendations.")
        print("- query multiple <file_path>: Queries each")
        print("\tbook url in the file and displays statistics")
        print("\tand recommendations.")
        print("- recalibrate: Starts to update the books")
        print("\tthat are processed in the Libraria with the")
        print("\tcurrent downloaded books.")
        print("- add <book_url>: Adds the book to the library")
        print("\twith the given book url.")
        print("- remove <book_url>: Removes the book from ")
        print("\tthe downloaded books and asks you to select")
        print("\tif you want to recalibrate after removal.")
        print("- read <book_url>: Displays the book to the")
        print("\tscreen and shows the contents of the book.")
        print("- exit: Terminates the Libraria.")

    def command_selector(self, command):
        '''
        - Takes the string input and decides the desired action
        to execute, which can be any of the below.
        '''
        command_tokens = str(command).split()
        base_command = command_tokens[0]
        command_params = command_tokens[1:]

        if base_command == "help":
            self.display_help()
        elif base_command == "stateload":
            self.library.load_resources()
        elif base_command == "statedump":
            self.library.dump_resources()
        elif base_command == "booklistload":
            self.library.load_booklist(command_params[0])
        elif base_command == "query":
            self.library.compose_a_query(command_params[0], command_params[1])
        elif base_command == "lastqueryscore":
            self.library.display_last_query_scores()
        elif base_command == "recalibrate":
            self.library.calculate_tf_idf()
        elif base_command == "add":
            self.library.add_to_library(command_params[0])
        elif base_command == "remove":
            self.library.remove_from_library(command_params[0])
        elif base_command == "read":
            self.library.read_a_book(command_params[0])
        elif base_command == "exit":
            self.isTerminated = True
        else:
            print("Invalid command. Try again")

    def init_library(self):
        '''
        - Initializes the library API and runs a Libraria
        instance which is connected to the stdin to perform
        several processes.
        '''
        self.display_info()
        rec_count = input("Enter recommendation count: ")
        # Strips whitespace
        rec_count = rec_count.strip()
        try:
            if rec_count != "\n" and rec_count != "\r":
                rec_count = int(rec_count)
        except ValueError:
            # In description, it says 18 as default value, 
            # but my application can support any logical and
            # reasonable value that user enters.
            rec_count = 18
            print("Invalid value. Set to default as 18.")
        self.library = Library(rec_count)
        print("To see available commands in Libraria,")
        print("type `help` to the prompt.")

    def start_api(self):
        '''
        - Starts the API and waits for user input to
        perform a task.
        '''
        self.init_library()
        while not self.isTerminated:
            command = self.retrieve_input()
            self.command_selector(command)
        print("Hope you will come here to read again.")

if __name__ == "__main__":
    libapi = LibraryAPI()
    libapi.start_api()
