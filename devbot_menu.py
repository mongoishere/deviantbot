import os, devbot, devbot_functions, datetime, datetime, random, time, sqlite_manager

from termcolor import colored
# Here we are creating our menu for devbot to be able to manage the deviantbot

class DevbotMenu(object):

    def __init__(self):

        self.function_list = {} # Dictionary to hold the list of functions

    def generate_menu(self):

        # Here is where we print the values in the menu

        while True:
            try:
                for index, key in enumerate(self.function_list.keys()):
                    print("[%s] %s" % ((colored((index+1), 'green'), key)))

                self.select_function(int(input("Select Option %s " % colored(">", 'green'))))

            except KeyboardInterrupt:
                print(colored("\nTaking a step back...", 'cyan'))
                break

    def add_function(self, func_title, func_name, args=None):

        if(not(args)):
            self.function_list[func_title] = func_name # Create function list

        else:
            args_list = []

            for argument in args:
                args_list.append(argument)

            self.function_list[func_title] = [func_name, args_list]

    def select_function(self, func_opt):

        for index, key in enumerate((self.function_list.keys())):
            
            if isinstance(self.function_list[key], list):

                if(func_opt == (index+1)):
                    # Here we can open up a new terminal window ro run this command on another thread
                    self.function_list[key][0](*self.function_list[key][1])
            else:

                if(func_opt == (index+1)):
                    self.function_list[key]()

    def create_bot_menu(self):

        masterdb = 'databases/masterbot.db'

        user_responses = []

        input_prompts = [
            "Enter Bot Name",
            "Enter Bot Email",
            "Enter Bot Password"
        ]

        for prompt in input_prompts:

            user_responses.append(input("%s %s " % (prompt, colored(">>", 'green'))))

        devbot_functions.DevbotFunctions.create_new_bot(None, (*user_responses), masterdb)

    def spam_bot_menu(self):

        masterdb = 'databases/masterbot.db'

        user_responses = []

        input_prompts = [
            "Enter Desired Bot",
            "Enter Target Username",
            "Enter Note Content",
            "Enter Spam Count"
        ]

        for prompt in input_prompts:

            user_responses.append(input("%s %s " % (prompt, colored(">>", 'green'))))
        
        devbot_functions.DevbotFunctions.spam_notes(None, (*user_responses), masterdb)

    def bot_preferences_menu(self):

        masterdb = 'databases/masterbot.db'

        masterbot_database = sqlite_manager.SqliteDatabase(masterdb)
        bot_records = masterbot_database.fetch_all_rows('bot_info')
        
        for ind, bot in enumerate(bot_records):

            print("[%s] %s" % (colored(ind+1, 'green'), bot[1]))

        bot_selection = int(input("Select Bot %s " % colored(">>", 'green')))
        bot_name = bot_records[bot_selection-1][1]
        bot_menu = DevbotMenu()
        bot_menu.add_function(('Change %s\'s Picture' % (bot_name)), print)
        bot_menu.add_function(('Change %s\'s Bio' % (bot_name)), print)
        bot_menu.add_function(('Change %s\'s Birthday' % (bot_name)), print)
        bot_menu.generate_menu()

if __name__ == '__main__':

    main_menu = DevbotMenu()
    main_menu.add_function('Create a new bot', main_menu.create_bot_menu)
    main_menu.add_function('Spam someone', main_menu.spam_bot_menu)
    main_menu.add_function('Change Bot Preferences', main_menu.bot_preferences_menu)
    main_menu.generate_menu()
