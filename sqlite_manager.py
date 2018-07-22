import sqlite3

class SqliteDatabase(object):

	def __init__(self, dbname='sqlite.db'):

		self.dbname = dbname
		self.database = sqlite3.connect(self.dbname)
		self.dbcursor = self.database.cursor()
		self.database.commit()
		self.database.close()

	def create_table(self, table_name, table_matrix):

		self.database = sqlite3.connect(self.dbname)
		self.dbcursor = self.database.cursor()

		self.create_table_syntax = "CREATE TABLE IF NOT EXISTS %s (" % (table_name)

		for column in table_matrix:

			self.create_table_syntax += (column[0] + " " + column[1] + ", ")

		self.create_table_syntax = self.create_table_syntax[:-2]
		self.create_table_syntax += ")"

		self.dbcursor.execute(self.create_table_syntax)

		self.database.commit()
		self.database.close()

	def insert_into(self, table_name, table_args):

		self.database = sqlite3.connect(self.dbname)
		self.dbcursor = self.database.cursor()

		col_names_obj = self.dbcursor.execute('SELECT * FROM %s' % (table_name))
		col_names = list(map(lambda x: x[0], col_names_obj.description)) # Research this
		col_names.pop(0)

		if(len(table_args) == len(col_names)):

			self.insert_into_syntax = ("INSERT INTO %s(" % (table_name))
			values_string = "("

			for col in col_names:

				self.insert_into_syntax += (col + ", ")
				values_string += ("?, ")

			self.insert_into_syntax = self.insert_into_syntax[:-2]
			self.insert_into_syntax += ")"

			values_string = values_string[:-2]
			values_string += ")"

			self.insert_into_syntax += (" VALUES %s" % (values_string))

			self.dbcursor.execute(self.insert_into_syntax, table_args)
			self.database.commit()
			self.database.close()

		else:

			print('Not enough arguments')
