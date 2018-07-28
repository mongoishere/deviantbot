import os, devbot, datetime, pdb, datetime, random, time
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

                input("Type Something > ")

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
                print('This value is not a list')
            

if __name__ == '__main__':

    main_menu = DevbotMenu()
    main_menu.add_function('print_something', print, ['Dakurochi %s' % ('rocks')])
    main_menu.add_function('print_something_second', print, ['Something funny'])
    main_menu.select_function(1)
    main_menu.select_function(2)
    main_menu.generate_menu()