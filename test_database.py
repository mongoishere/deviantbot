import sqlite_manager


db = sqlite_manager.SqliteDatabase('test.db')

db.create_table('test_table',
    [
        ['id', 'INTEGER PRIMARY KEY'],
        ['fst_column', 'TEXT'],
        ['snd_column', 'TEXT'],
        ['thd_column', 'TEXT']
    ]
)

db.insert_into('test_table', 
    ['something', 'something_else', 'something_elser']
)


db.insert_into('test_table', 
    ['something', 'something_elser', 'something_elser'], True, 'snd_column', 'something_elser'
)
