import os, devbot, devbot_functions, datetime, pdb, datetime, random, time
# Here we are creating our menu for devbot to be able to manage the deviantbot

class DevbotMenu(object):

    def __init__(self):

        self.function_list = {} # Dictionary to hold the list of functions

    def generate_menu(self):

        # Here is where we print the values in the menu

        while True:
            try:
                for index, key in enumerate(self.function_list.keys()):
                    print("[%s] %s" % ((index+1), key))

                self.select_function(int(input("Select Option => ")))

            except KeyboardInterrupt:
                print("\nTaking a step back...")
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

            user_responses.append(input("%s => " % (prompt)))

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

            user_responses.append(input("%s => " % (prompt)))
        
        devbot_functions.DevbotFunctions.spam_notes(None, (*user_responses), masterdb)
        

if __name__ == '__main__':

    main_menu = DevbotMenu()
    main_menu.add_function('Create a new bot', main_menu.create_bot_menu)
    main_menu.add_function('Spam someone', main_menu.spam_bot_menu)
    main_menu.generate_menu()
