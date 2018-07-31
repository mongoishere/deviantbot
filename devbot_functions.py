import pdb, devbot, sqlite_manager

class DevbotFunctions(object):

    def __init__(self):

        pass

    def create_new_bot(self, bot_name, bot_email, bot_pwd, masterdb):

        devbot = devbot.DeviantBot([bot_name, bot_email, bot_pwd], masterdb)
        devbot.register()

    
    def spam_message(self, bot_name):
        
        devbot = devbot.DeviantBot([])
        

if __name__ == '__main__':

    masterdb = 'databases/masterbot.db'

    application = DevbotFunctions()
    application.create_new_bot('dlfkjsdljflsd', 'dfskldjflkdsj@gmail.com', 'strongpassword', masterdb)
