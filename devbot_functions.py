import pdb, devbot, sqlite_manager

class DevbotFunctions(object):

    def __init__(self):

        pass

    def create_new_bot(self, bot_name, bot_email, bot_pwd, masterdb):

        deviantbot = devbot.DeviantBot([bot_name, bot_email, bot_pwd], masterdb)
        deviantbot.register()

    
    def spam_notes(self, bot_name, target, note_cont, spam_num, masterdb):
        
        master_database = sqlite_manager.SqliteDatabase(masterdb)
        bot_pass = master_database.fetch_row('bot_password', 'bot_info', 'bot_name', bot_name)

        deviantbot = devbot.DeviantBot([bot_name, 'irrelevant', bot_pass], masterdb)

        deviantbot.login()
        
        for note in range(int(spam_num)):

            deviantbot.print_log_message('Sending note [%s of %s]' % ((note+1), spam_num))
            deviantbot.send_notes(target, note_cont)


if __name__ == '__main__':

    masterdb = 'databases/masterbot.db'

    application = DevbotFunctions()
    #application.create_new_bot('dlfkjsdljflsd', 'dfskldjflkdsj@gmail.com', 'strongpassword', masterdb)
    application.spam_notes('cipheradarlin', 'ilop709', 'message', 10)
