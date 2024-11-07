from os import path
from sys import exit
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .WSBeat_Configuration_Class import WSBeatConfiguration

"""
Class that manages the operation of WSbeat-Tool.
"""
class WSBeatTool:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def main_menu(self):
		"""
		Main menu.
		"""
		try:
			option = self.dialog.create_menu("Select a option:", 12, 50, self.constants.OPTIONS_MAIN_MENU, "Main Menu")
			self.main_menu_switch(option)
		except KeyboardInterrupt:
			pass


	def configuration_menu(self):
		"""
		Configuration menu.
		"""
		option = self.dialog.create_menu("Select a option", 9, 50, self.constants.OPTIONS_CONFIGURATION_MENU, "Configuration Menu")
		self.configuration_menu_switch(option)


	def main_menu_switch(self, option):
		"""
		Method that performs an action based on the option chosen in the "Main Menu".

		:arg option (string): Chosen option.
		"""
		match option:
			case "1":
				self.configuration_menu()
			case "2":
				print("Opcion 2")
			case "3":
				print("Oocpion 3")
			case "4":
				print("Opcion 4")
			case "5":
				exit(1)


	def configuration_menu_switch(self, option):
		"""
		Method that performs an action based on the option chosen in the "Configuration Menu".

		:arg option (string): Chosen option.
		"""
		self.wsbeat_configuration() if option == "1" else self.wsbeat_agent_configuration()


	def wsbeat_configuration(self):
		"""
		Method that creates, modifies or displays the WSBeat's configuration.
		"""
		wsbeat_configuration = WSBeatConfiguration()
		if not path.exists(self.constants.WSBEAT_CONFIGURATION_FILE):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.OPTIONS_NO_CONFIGURATION, "WSBeat Configuration")
			if option == "Create":
				wsbeat_configuration.create_configuration()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.OPTIONS_YES_CONFIGURATION, "WSBeat Configuration")
			wsbeat_configuration.modify_configuration() if option == "Modify" else wsbeat_configuration.display_configuration()





