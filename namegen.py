import random
import os

class UsernameGen(object):

	def cyberpunk(self):

		with open("namelists/cybergirl.txt") as cyberfile:

			name_data = cyberfile.read()
			name_list = name_data.split(",")

			for ind, name in enumerate(name_list):

				name_list[ind] = name.replace('"', '')

			name_list_len = len(name_list)

			name_prefix = name_list[random.randint(0, name_list_len)]
			name_suffix = random.randint(100, 9999)

			gen_name = name_prefix + str(name_suffix)
			
			return gen_name

if __name__ == '__main__':

	Application = UsernameGen()
	Application.cyberpunk()