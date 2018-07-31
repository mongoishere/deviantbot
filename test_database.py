import sqlite_manager

masterdb = 'databases/masterbot.db'

db = sqlite_manager.SqliteDatabase(masterdb)
result = db.fetch_row('bot_password', 'bot_info', 'bot_name', 'cipheradarlin')
print(result)
