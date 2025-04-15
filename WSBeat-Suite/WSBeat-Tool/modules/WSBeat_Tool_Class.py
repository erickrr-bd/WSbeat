from os import path
from sys import exit
from dataclasses import dataclass
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from libPyConfiguration import libPyConfiguration
from libPyAgentConfiguration import libPyAgentConfiguration

"""
Class that manages the operation of WSbeat-Tool.
"""
@dataclass
class WSBeatTool:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def main_menu(self) -> None:
		"""
		Main menu.
		"""
		try:
			option = self.dialog.create_menu("Select a option:", 12, 50, self.constants.MAIN_MENU_OPTIONS, "Main Menu")
			self.switch_main_menu(int(option))
		except KeyboardInterrupt:
			pass


	def configuration_menu(self) -> None:
		"""
		Configuration menu.
		"""
		option = self.dialog.create_menu("Select a option", 9, 50, self.constants.CONFIGURATION_MENU_OPTIONS, "Configuration Menu")
		self.switch_configuration_menu(int(option))


	def switch_main_menu(self, option: int) -> None:
		"""
		Method that performs an action based on the option chosen in the "Main Menu".

		Parameters:
			option (int): Chosen option.
		"""
		match option:
			case 1:
				self.configuration_menu()
			case 2:
				print("Opcion 2")
			case 3:
				print("Oocpion 3")
			case 4:
				self.display_about()
			case 5:
				exit(1)


	def switch_configuration_menu(self, option: int) -> None:
		"""
		Method that performs an action based on the option chosen in the "Configuration Menu".

		Parameters:
			option (int): Chosen option.
		"""
		self.define_configuration() if option == 1 else self.define_agent_configuration()


	def define_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the WSBeat configuration..
		"""
		if not path.exists(self.constants.WSBEAT_CONFIGURATION):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.CONFIGURATION_OPTIONS_FALSE, "WSBeat Configuration")
			if option == "Create":
				self.create_configuration()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.CONFIGURATION_OPTIONS_TRUE, "WSBeat Configuration")
			self.modify_configuration() if option == "Modify" else self.display_configuration()


	def create_configuration(self) -> None:
		"""
		Method that creates the WSBeat configuration.
		"""
		wsbeat_data = libPyConfiguration(self.constants.BACKTITLE)
		wsbeat_data.define_es_host()
		wsbeat_data.define_verificate_certificate()
		wsbeat_data.define_use_authentication(self.constants.KEY_FILE)
		wsbeat_data.create_file(wsbeat_data.convert_object_to_dict(), self.constants.WSBEAT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def modify_configuration(self) -> None:
		"""
		Method that updates or modifies the WSBeat configuration.
		"""
		wsbeat_data = libPyConfiguration(self.constants.BACKTITLE)
		wsbeat_data.modify_configuration(self.constants.WSBEAT_CONFIGURATION, self.constants.KEY_FILE, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display_configuration(self) -> None:
		"""
		Method that displays the WSBeat configuration.
		"""
		wsbeat_data = libPyConfiguration(self.constants.BACKTITLE)
		wsbeat_data.display_configuration(self.constants.WSBEAT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def define_agent_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the WSBeat-Agent configuration.
		"""
		if not path.exists(self.constants.WSBEAT_AGENT_CONFIGURATION):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.CONFIGURATION_OPTIONS_FALSE, "WSBeat-Agent Configuration")
			if option == "Create":
				self.create_agent_configuration()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.CONFIGURATION_OPTIONS_TRUE, "WSBeat-Agent Configuration")
			self.modify_agent_configuration() if option == "Modify" else self.display_agent_configuration()


	def create_agent_configuration(self) -> None:
		"""
		Method that creates the WSBeat-Agent configuration.
		"""
		wsbeat_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		wsbeat_agent_data.define_frequency_time()
		wsbeat_agent_data.define_telegram_bot_token(self.constants.KEY_FILE)
		wsbeat_agent_data.define_telegram_chat_id(self.constants.KEY_FILE)
		wsbeat_agent_data.create_file(wsbeat_agent_data.convert_object_to_dict(), self.constants.WSBEAT_AGENT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def modify_agent_configuration(self) -> None:
		"""
		Method that updates or modifies the WSBeat-Agent configuration.
		"""
		wsbeat_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		wsbeat_agent_data.modify_agent_configuration(self.constants.WSBEAT_AGENT_CONFIGURATION, self.constants.KEY_FILE, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display_agent_configuration(self) -> None:
		"""
		Method that displays the WSBeat-Agent configuration.
		"""
		wsbeat_agent_data = libPyAgentConfiguration(self.constants.BACKTITLE)
		wsbeat_agent_data.display_agent_configuration(self.constants.WSBEAT_AGENT_CONFIGURATION, self.constants.LOG_FILE, self.constants.USER, self.constants.GROUP)


	def display_about(self) -> None:
		"""
		Method that displays the about of the application.
		"""
		try:
			text = "\nAuthor: Erick Roberto Rodríguez Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\nGithub: https://github.com/erickrr-bd/WSbeat\nWSBeat v1.1 - April 2025" + "\n\nEasy data ingestion into ElasticSearch using Python and\nwebsockets."
			self.dialog.create_scrollbox(text, 13, 60, "About")
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error") 
			