import random, time, os, sqlite_manager, datetime, pdb
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from threading import Thread

colors = {
	"red": "\033[31m",
	"green": "\33[92m",
	"red_highlight": "\33[101m",
	"yellow": "\33[33m",
	"endcol": '\033[0m'
}

class DeviantBot(Thread):

	# Creates the bot information and will attempt to register if does not exist

	def __init__(self, creds, masterdb):

		if(len(creds) < 3):

			die('Not Enough Credential Values')
	
		super(DeviantBot, self).__init__() # Keep Thread constructor
		self.bot_profile = webdriver.FirefoxProfile()
		self.bot_browser_opts = webdriver.FirefoxOptions()
		#self.bot_browser_opts.add_argument('--headless')
		self.bot_browser = webdriver.Firefox()
		self.credentials = creds
		self.print_log_message('Starting Bot')
		self.deviant_main = "https://www.deviantart.com/"
		self.deviant_join = "https://www.deviantart.com/join/"
		self.deviant_profile = ("https://www.deviantart.com/%s" % (self.credentials[0]))
		self.deviant_login = "https://www.deviantart.com/users/login"
		self.deviant_note = "https://www.deviantart.com/notifications/notes/#1_0"
		self.deviant_forum = "https://forum.deviantart.com/community/projects/"
		self.whatsip = "http://whatismyip.host/"
		self.imagepath = "profile_pics/"
		dbpath = ('databases/%s_database.db' % (self.credentials[0]))
		self.bot_database = sqlite_manager.SqliteDatabase(dbpath)
		self.master_database = sqlite_manager.SqliteDatabase(masterdb)
		self.generate_bot_database()

	def generate_bot_database(self):

		self.master_database.create_table('bot_info',
			[
				['primaryID', 'INTEGER PRIMARY KEY'],
				['bot_name', 'TEXT'],
				['bot_created', 'smalldatetime'],
				['bot_email', 'TEXT'],
				['bot_password', 'TEXT']
			]
		)

		# Insert into masterdb if the bot does not exist

		self.master_database.insert_into('bot_info',
			[self.credentials[0], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.credentials[1], self.credentials[2]], True, 'bot_name', self.credentials[0]
		)

		#self.master_database.insert_into('bot_info',
		#	[self.credentials[0], 0, self.credentials[1], self.credentials[2]], True, 'bot_name', self.credentials[0]
		#)

		self.bot_database.create_table('messages',
			[
				['primaryID', 'INTEGER PRIMARY KEY'],
				['to_uname', 'TEXT'],
				['from_uname', 'TEXT'],
				['date', 'smalldatetime'],
				['content', 'TEXT'],
				['mode', 'INTEGER']
			]
		)

		self.bot_database.create_table('forums_made',
			[
				['primaryID', 'INTEGER PRIMARY KEY'],
				['forum_name', 'TEXT'],
				['forum_content', 'TEXT'],
				['forum_link', 'TEXT'],
				['forum_created', 'smalldatetime'],
				['forum_genre', 'TEXT']
			]
		)

	def register(self):

		self.print_log_message("Navigating to %s" % (self.deviant_join))
		self.bot_browser.get(self.deviant_join)
		register_page_text = self.bot_browser.page_source
		register_page_soup = BeautifulSoup(register_page_text, 'html.parser')
		register_page_form = self.bot_browser.find_element_by_id('form1')

		register_page_cusername = self.bot_browser.find_element_by_id('cusername')
		register_page_email1 = self.bot_browser.find_element_by_id('email1')
		register_page_email2 = self.bot_browser.find_element_by_id('email2')
		register_page_password = self.bot_browser.find_element_by_id('password1')
		register_page_dobmonth = self.bot_browser.find_element_by_id('dobmonth')
		register_page_dobday = self.bot_browser.find_element_by_id('dobday')
		register_page_dobyear = self.bot_browser.find_element_by_id('dobyear')
		register_page_gender = self.bot_browser.find_element_by_id('gender')
		register_page_agree = self.bot_browser.find_element_by_id('agreeterms')

		determine_option = lambda opt, ind, num: opt.click() if ind == num else None
		choose_option = lambda elem, num: [determine_option(option, ind, num) for ind, option in enumerate(elem('option'))]

		self.print_log_message("Filling out register form...")
		register_page_cusername.send_keys(self.credentials[0])
		register_page_email1.send_keys(self.credentials[1])
		register_page_email2.send_keys(self.credentials[1])
		register_page_password.send_keys(self.credentials[2])

		choose_option(register_page_dobmonth.find_elements_by_tag_name, random.randint(0, 12))
		choose_option(register_page_dobday.find_elements_by_tag_name, random.randint(0, 28))
		choose_option(register_page_dobyear.find_elements_by_tag_name, random.randint(20, 100))
		choose_option(register_page_gender.find_elements_by_tag_name, random.randint(1, 2))

		register_page_agree.click()
		# Moment of truth
		register_page_form.submit()
		self.print_log_message("Successfully registered bot!")

	def login(self):

		try:
			self.print_log_message('Navigating to %s' % (self.deviant_login))
			self.bot_browser.get(self.deviant_login)

		except Exception as e:
			self.print_log_message('Exception Occured: %s...retrying' % (str(e)), False)
			self.print_log_message('Navigating to %s' % (self.deviant_login))
			self.bot_browser.get(self.deviant_login)

		self.print_log_message('Trying to find element')
		login_page_form = self.bot_browser.find_element_by_id('login')
		login_page_title = self.bot_browser.title
		login_page_username = self.bot_browser.find_element_by_id('login_username')
		login_page_password = self.bot_browser.find_element_by_id('login_password')

		self.print_log_message("Logging In")

		login_page_username.send_keys(self.credentials[0])
		login_page_password.send_keys(self.credentials[2])

		login_page_form.submit()

		wait(self.bot_browser, 15).until_not(EC.title_is(login_page_title))

	def send_notes(self, to_name, msg, mode=0):

		self.bot_browser.get(self.deviant_note)

		notes_page_intro = self.bot_browser.find_element_by_id('note-intro')
		notes_page_createbtn = notes_page_intro.find_element_by_class_name('button_create')

		notes_page_createbtn.click()

		notes_page_form = self.bot_browser.find_element_by_xpath('//form[@data-dwait-domready="Notes.compose"]')
		notes_page_subject = notes_page_form.find_element_by_class_name('subject')
		notes_page_recipient_area = notes_page_form.find_element_by_id('recipient-textareas')
		
		notes_page_message = notes_page_form.find_element_by_id('notebody')
		notes_page_recipient = notes_page_recipient_area.find_elements_by_tag_name('input')
		notes_page_subject = notes_page_subject.find_element_by_xpath('//input[@class="text f"]')
		notes_page_sendbtn = notes_page_form.find_element_by_class_name('send_note')

		for input_area in notes_page_recipient:

			try:
				input_area.send_keys(to_name)

			except:
				pass

		notes_page_subject.send_keys(to_name)
		notes_page_message.send_keys(msg)
		notes_page_sendbtn.click()

		self.print_log_message('Message Sent Successfully to %s' % (to_name))

		self.bot_database.insert_into('messages', [to_name, self.credentials[0], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg, mode])

	def create_forum(self, subject, content):

		self.bot_browser.get(self.deviant_forum)

		forum_page_form = self.bot_browser.find_element_by_xpath('//form[@name="postcomment"]')
		forum_page_topic = forum_page_form.find_element_by_id('commentsubject')
		forum_page_content = forum_page_form.find_element_by_id('commentbody')
		forum_page_submitbtn = forum_page_form.find_element_by_xpath('//a[@class="smbutton smbutton-big smbutton-green submit"]')
		forum_page_ccwriter = forum_page_form.find_element_by_class_name('ccwriter-content')

		forum_page_contentwriter = forum_page_ccwriter.find_element_by_xpath('//div[@class="writer selectable no-lub put-art-here ui-droppable empty"]')

		self.print_log_message('Found Element: %s' % (forum_page_contentwriter))

		print(forum_page_submitbtn.get_attribute('outerHTML'))

		self.bot_browser.execute_script("arguments[0].style.display = 'block';", forum_page_content)

		forum_page_topic.send_keys(subject)
		forum_page_contentwriter.send_keys(content)

		# Moment of truth
		forum_page_submitbtn.click()

		self.print_log_message('Forum %s created Successfully!' % (subject))

	def update_proxy(self):

		# Here is where we update and change the bot's proxy
		self.proxy_list = open('proxy_list', 'r')
		self.proxy_matrix = []

		for proxy in self.proxy_list:

			self.proxy_matrix.append(proxy.split(':'))

		selected_proxy = self.proxy_matrix[random.randint(0, len(self.proxy_matrix) - 1)]

		self.bot_profile.set_preference('network.proxy.type', 1)
		self.bot_profile.set_preference('network.proxy.http', selected_proxy[0])
		self.bot_profile.set_preference('network.proxy.http_port', int(selected_proxy[1]))
		self.bot_profile.set_preference('network.proxy.ssl', selected_proxy[0])
		self.bot_profile.set_preference('network.proxy.ssl_port', int(selected_proxy[1]))
		self.bot_profile.update_preferences()

		self.bot_browser.quit()

		self.bot_browser = webdriver.Firefox(firefox_profile=self.bot_profile, firefox_options=self.bot_browser_opts)

		self.bot_browser.get(self.whatsip)
		self.print_log_message(str(selected_proxy))

	def change_profile_pic(self):

		image_list = []

		for image in os.listdir(self.imagepath):
			image_list.append(image)

		self.bot_browser.get(self.deviant_profile)

		wait(self.bot_browser, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='catbar']")))

		profile_page_pic_area = self.bot_browser.find_element_by_class_name('authorative-avatar')
		profile_page_ghost_link = profile_page_pic_area.find_element_by_class_name('ghost-edit')

		
		profile_page_ghost_link.click()

		wait(self.bot_browser, 60).until(EC.visibility_of_element_located((By.XPATH, "//form[@class='file_upload']")))

		profile_page_pic_upload_form = self.bot_browser.find_element_by_class_name('file_upload')
		
		profile_page_button_area = self.bot_browser.find_element_by_class_name('buttons')

		profile_page_pic_uploadbtn = profile_page_pic_upload_form.find_element_by_xpath(
			"//input[@name='deck_file']")

		selected_image = image_list[random.randint(0, (len(image_list) - 1))]

		self.print_log_message('Image Selected: %s' % (selected_image))

		profile_page_pic_uploadbtn.send_keys(('/home/anonymous/Programming/Python/deviantbot2.0/%s%s' % (self.imagepath, selected_image)))

		wait(self.bot_browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='cropbox']")))

		profile_page_save_btn = profile_page_button_area.find_element_by_class_name(
			"smbutton-green")

		self.bot_browser.execute_script("arguments[0].click();", profile_page_save_btn)

		self.print_log_message("Profile picture has been updated")

		time.sleep(4.5)
		
	def print_log_message(self, msg, success=True):

		if(success):
			print('(%s) %s[+]%s %s' % (
				self.credentials[0],
				colors['green'],
				colors['endcol'],
				msg
			))

		else:
			print('(%s) %s[-]%s %s' % (
				self.credentials[0],
				colors['red'],
				colors['endcol'],
				msg
			))

	def run(self):

		#self.update_proxy()
		self.login()

		for i in range(30):

			self.send_notes('ilop709', 'Pull Up With Dat Strap')
			self.change_profile_pic()
			#self.change_profile_pic()

	def die(self, message):

		print(message)
		exit(1)


if __name__ == '__main__':

	masterdb_path = 'databases/masterbot.db'

	CipherBot = DeviantBot(['cipheradarlin', 'cipheradarlin@gmail.com', 'strongpassword'], masterdb_path)
	Elitra = DeviantBot(['elitraadarlin', 'elitraadarlin@gmail.com', 'strongpassword'], masterdb_path)
	#Elitra = DeviantBot(['elitraadarlin', 'elitraadarlin@gmail.com', 'strongpassword'], masterdb_path)
	#CipherBot.register()
	CipherBot.start()
	#Elitra.start()
