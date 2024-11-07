from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages the configuration of WSBeat.
"""
class WSBeatConfiguration:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def create_configuration(self):
		"""
		Method that creates the WSBeat configuration.
		"""
		try:
			wsbeat_data = []
			master_nodes = self.dialog.create_integer_inputbox("Enter the total number of master nodes:", 8, 50, "1")
			tuple_to_form = self.utils.generate_tuple_to_form(int(master_nodes), "IP Address")
			es_host = self.dialog.create_form("Enter IP addresses:", tuple_to_form, 15, 50, "ElasticSearch Hosts", True, validation_type = 1)
			wsbeat_data.append(es_host)
			es_port = self.dialog.create_port_inputbox("Enter the port to communicate with ElasticSearch:", 9, 50, "9200")
			wsbeat_data.append(es_port)
			use_ssl = self.dialog.create_yes_or_no("\nIs the SSL/TLS protocol required for communication between WSBeat and ElasticSearch?", 9, 50, "SSL/TLS Connection")
			if use_ssl == "ok":
				wsbeat_data.append(True)
				verificate_certificate_ssl = self.dialog.create_yes_or_no("\nIs SSL certificate verification required?", 7, 50, "Certificate SSL Verification")
				if verificate_certificate_ssl == "ok":
					wsbeat_data.append(True)
					certificate_file = self.dialog.create_file(self.constants.SSL_CERTIFICATE_FOLDER, 8, 50, "Select the CA certificate:", ".pem")
					wsbeat_data.append(certificate_file)
				else:
					wsbeat_data.append(False)
			else:
				wsbeat_data.append(False)
			use_authentication = self.dialog.create_yes_or_no("\nIs an authentication method (HTTP Authentication or API Key) required for communication between WSBeat and ElasticSearch?", 10, 50, "Authentication Method")
			if use_authentication == "ok":
				wsbeat_data.append(True)
				passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
				option = self.dialog.create_radiolist("Select a option:", 9, 55, self.constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
				wsbeat_data.append(option)
				if option == "HTTP Authentication":
					http_authentication_user = self.utils.encrypt_data(self.dialog.create_inputbox("Enter username:", 8, 50, "http_user"), passphrase)
					wsbeat_data.append(http_authentication_user)
					http_authentication_password = self.utils.encrypt_data(self.dialog.create_passwordbox("Enter the password:", 8, 50, "password", True), passphrase)
					wsbeat_data.append(http_authentication_password)
				elif option == "API Key":
					api_key_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the API Key ID:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
					wsbeat_data.append(api_key_id)
					api_key = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
					wsbeat_data.append(api_key)
			else:
				wsbeat_data.append(False)
			index_name = self.dialog.create_inputbox("Enter the name of the index:", 8, 50, "logs")
			wsbeat_data.append(index_name)
			url = self.dialog.create_inputbox("Enter the URL for communication via WebSocket:", 8, 50, "wss://logs:443")
			wsbeat_data.append(url)
			bearer_token = self.dialog.create_inputbox("Enter the Bearer Token:", 8, 50, "3yqTaskewalsll98jkloper")
			wsbeat_data.append(bearer_token)
			self.create_configuration_file(wsbeat_data)
			if path.exists(self.constants.WSBEAT_CONFIGURATION_FILE):
				self.dialog.create_message("\nWSBeat configuration created.", 7, 50 , "Notification Message")
				self.logger.create_log("WSBeat configuration created.", 2, "_createConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.create_message("\nError creating WSBeat configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_createConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def create_configuration_file(self, wsbeat_data):
		"""
		Method that creates the WSBeat configuration file.

		:arg wsbeat_data (Dict): Dictionary with configuration data.
		"""
		wsbeat_data_json = {
			"es_host" : wsbeat_data[0],
			"es_port" : int(wsbeat_data[1]),
			"use_ssl" : wsbeat_data[2]
		}

		if wsbeat_data[2]:
			wsbeat_data_json.update({"verificate_certificate_ssl" : wsbeat_data[3]})
			if wsbeat_data[3]:
				certificate_file = self.constants.SSL_CERTIFICATE_FOLDER + '/' + path.basename(wsbeat_data[4])
				wsbeat_data_json.update({"certificate_file" : certificate_file})
				self.utils.copy_file(wsbeat_data[4], self.constants.SSL_CERTIFICATE_FOLDER)
				self.utils.change_owner(certificate_file, self.constants.USER, self.constants.GROUP, "640")
				last_index = 4
			else:
				last_index = 3
		else:
			last_index = 2
		wsbeat_data_json.update({"use_authentication" : wsbeat_data[last_index + 1]})
		if wsbeat_data[last_index + 1]:
			wsbeat_data_json.update({"authentication_method" : wsbeat_data[last_index + 2]})
			if wsbeat_data[last_index + 2] == "HTTP Authentication":
				wsbeat_data_json.update({"http_authentication_user" : wsbeat_data[last_index + 3], "http_authentication_password" : wsbeat_data[last_index + 4]})
			elif wsbeat_data[last_index + 2] == "API Key":
				wsbeat_data_json.update({"api_key_id" : wsbeat_data[last_index + 3], "api_key" : wsbeat_data[last_index + 4]})
			last_index += 4
		else:
			last_index += 1
		wsbeat_data_json.update({"index_name" : wsbeat_data[last_index + 1], "url" : wsbeat_data[last_index + 2], "bearer_token" : wsbeat_data[last_index + 3]})

		self.utils.create_yaml_file(wsbeat_data_json, self.constants.WSBEAT_CONFIGURATION_FILE)
		self.utils.change_owner(self.constants.WSBEAT_CONFIGURATION_FILE, self.constants.USER, self.constants.GROUP, "640")


	def modify_configuration(self):
		"""
		Method that modifies one or more values of the WSBeat configuration.
		"""
		try:
			options = self.dialog.create_checklist("Select one or more options:", 14, 65, self.constants.OPTIONS_WSBEAT_CONFIGURATION, "WSBeat Configuration")
			wsbeat_data = self.utils.read_yaml_file(self.constants.WSBEAT_CONFIGURATION_FILE)
			if "Host" in options:
				self.modify_es_host(wsbeat_data)
			if "Port" in options:
				self.modify_es_port(wsbeat_data)
			if "SSL/TLS" in options:
				self.modify_use_ssl(wsbeat_data)
			if "Authentication" in options:
				self.modify_authentication_method(wsbeat_data)
			if "Index" in options:
				self.modify_index_name(wsbeat_data)
			if "URL" in options:
				self.modify_url(wsbeat_data)
			if "Token" in options:
				self.modify_bearer_token(wsbeat_data)
			self.utils.create_yaml_file(wsbeat_data, self.constants.WSBEAT_CONFIGURATION_FILE)
		except Exception as exception:
			self.dialog.create_message("\nError modifying WSBeat configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def modify_es_host(self, wsbeat_data):
		"""
		Method that modifies the ElasticSerach Hosts.

		Returns a dictionary with the modified data.
		
		:arg wsbeat_data (Dict): Dictionary with configuration data.
		"""
		option = self.dialog.create_menu("Select a option:", 10, 50, self.constants.OPTIONS_ES_HOSTS_MENU, "ElasticSearch Hosts Menu")
		match option:
			case "1":
				master_nodes = self.dialog.create_integer_inputbox("Enter the total number of master nodes:", 8, 50, "1")
				tuple_to_form = self.utils.generate_tuple_to_form(int(master_nodes), "IP Address")
				es_host = self.dialog.create_form("Enter IP addresses:", tuple_to_form, 15, 50, "Add ElasticSearch Hosts", True, validation_type = 1)
				wsbeat_data["es_host"].extend(es_host)
				self.logger.create_log("Modified configuration. ElasticSearch hosts added.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
				self.dialog.create_message("\nModified configuration. ElasticSearch hosts added.", 8, 50, "Notification Message")
			case "2":
				tuple_to_form = self.utils.convert_list_to_tuple(wsbeat_data["es_host"], "IP Address")
				es_host = self.dialog.create_form("Enter IP addresses:", tuple_to_form, 15, 50, "Modify ElasticSearch Hosts", True, validation_type = 1)
				if not wsbeat_data["es_host"] == es_host:
					wsbeat_data["es_host"] = es_host
					self.logger.create_log("Modified configuration. ElasticSearch hosts modified.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
					self.dialog.create_message("\nModified configuration. ElasticSearch hosts modified.", 8, 50, "Notification Message")
				else:
					self.dialog.create_message("\nConfiguration not modified.", 7, 50, "Notification Message")
			case "3":
				tuple_to_rc = self.utils.convert_list_to_tuple_rc(wsbeat_data["es_host"], "IP Address")
				options = self.dialog.create_checklist("Select one or more options:", 15, 50, tuple_to_rc, "Remove ElasticSearch Hosts")
				text = self.utils.get_string_from_list(options, "Selected ElasticSearch Hosts:")
				self.dialog.create_scrollbox(text, 15, 60, "Remove ElasticSearch Hosts")
				is_remove = self.dialog.create_yes_or_no("\nAre you sure to remove the selected ElasticSearch Hosts?\n\n**NOTE: This action cannot be undone.", 10, 50, "Remove ElasticSearch Hosts")
				if is_remove == "ok":
					[wsbeat_data["es_host"].remove(item) for item in options]
					self.logger.create_log("Modified configuration. ElasticSearch hosts removed.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
					self.dialog.create_message("\nModified configuration. ElasticSearch hosts removed.", 8, 50, "Notification Message")
				else:
					self.dialog.create_message("\nConfiguration not modified.", 7, 50, "Notification Message")
		return wsbeat_data


	def modify_es_port(self, wsbeat_data):
		"""
		Method that modifies the ElasticSerach Port.

		Returns a dictionary with the modified data.
		
		:arg wsbeat_data (Dict): Dictionary with configuration data.
		"""
		current_es_port = str(wsbeat_data["es_port"])
		es_port = self.dialog.create_port_inputbox("Enter the port to communicate with ElasticSearch:", 9, 50, current_es_port)
		if not es_port == current_es_port:
			wsbeat_data["es_port"] = int(es_port)
			self.logger.create_log("Modified configuration. ElasticSearch port was modified.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			self.dialog.create_message("\nModified configuration. ElasticSearch port was modified.", 8, 50, "Notification Message")
		else:
			self.dialog.create_message("\nConfiguration not modified.", 7, 50, "Notification Message")
		return wsbeat_data


	def modify_use_ssl(self, wsbeat_data):
		"""
		Method that modifies the SSL/TLS configuration.

		Returns a dictionary with the modified data.
		
		:arg wsbeat_data (Dict): Dictionary with configuration data.
		"""
		if wsbeat_data["use_ssl"]:
			option = self.dialog.create_radiolist("Select a option:", 9, 70, self.constants.OPTIONS_YES_SSL, "SSL/TLS Connection")
			if option == "Disable":
				del wsbeat_data["verificate_certificate_ssl"]
				if "certificate_file" in wsbeat_data:
					del wsbeat_data["certificate_file"]
				wsbeat_data["use_ssl"] = False
			elif option == "Certificate Verification":
				if wsbeat_data["certificate_file"]:
					option = self.dialog.create_radiolist("Select a option:", 9, 65, self.constants.OPTIONS_YES_VERIFICATE_CERTIFICATE, "Certificate SSL Verification")
					if option == "Disable":
						if "certificate_file" in wsbeat_data:
							del wsbeat_data["certificate_file"]
						wsbeat_data["verificate_certificate_ssl"] = False
					elif option == "Certificate File":
						new_certificate_file = self.dialog.create_file(wsbeat_data["certificate_file"], 8, 50, "Select the CA certificate:", ".pem")
						certificate_file = self.constants.SSL_CERTIFICATE_FOLDER + '/' + path.basename(new_certificate_file)
						wsbeat_data["certificate_file"] = certificate_file
						self.utils.copy_file(new_certificate_file, self.constants.SSL_CERTIFICATE_FOLDER)
						self.utils.change_owner(certificate_file, self.constants.USER, self.constants.GROUP, "640")
				else:
					option = self.dialog.create_radiolist("Select a option:", 8, 70, self.constants.OPTIONS_NO_VERIFICATE_CERTIFICATE, "Certificate SSL Verification")
					if option == "Enable":
						wsbeat_data["verificate_certificate_ssl"] = True
						new_certificate_file = self.dialog.create_file(self.constants.SSL_CERTIFICATE_FOLDER, 8, 50, "Select the CA certificate:", ".pem")
						certificate_file = self.constants.SSL_CERTIFICATE_FOLDER + '/' + path.basename(new_certificate_file)
						wsbeat_data.update({"certificate_file" : certificate_file})
						self.utils.copy_file(new_certificate_file, self.constants.SSL_CERTIFICATE_FOLDER)
						self.utils.change_owner(certificate_file, self.constants.USER, self.constants.GROUP, "640")
		else:
			option = self.dialog.create_radiolist("Select a option:", 8, 70, self.constants.OPTIONS_NO_SSL, "SSL/TLS Connection")
			if option == "Enable":
				wsbeat_data["use_ssl"] = True
				verificate_certificate_ssl = self.dialog.create_yes_or_no("\nIs SSL certificate verification required?", 7, 50, "Certificate SSL Verification")
				if verificate_certificate_ssl == "ok":
					new_certificate_file = self.dialog.create_file(self.constants.SSL_CERTIFICATE_FOLDER, 8, 50, "Select the CA certificate:", ".pem")
					certificate_file = self.constants.SSL_CERTIFICATE_FOLDER + '/' + path.basename(new_certificate_file)
					wsbeat_data.update({"verificate_certificate_ssl" : True, "certificate_file" : certificate_file})
					self.utils.copy_file(new_certificate_file, self.constants.SSL_CERTIFICATE_FOLDER)
					self.utils.change_owner(certificate_file, self.constants.USER, self.constants.GROUP, "640")
				else:
					wsbeat_data.update({"verificate_certificate_ssl" : False})
		return wsbeat_data


	def modify_authentication_method(self, wsbeat_data):
		"""
		Method that modifies the Authentication Method configuration.

		Returns a dictionary with the modified data.
		
		:arg wsbeat_data (Dict): Dictionary with configuration data.
		"""
		if wsbeat_data["use_authentication"]:
			option = self.dialog.create_radiolist("Select a option:", 9, 55, self.constants.OPTIONS_YES_AUTHENTICATION, "Authentication Method")
			if option == "Disable":
				wsbeat_data["use_authentication"] = False
				if wsbeat_data["authentication_method"] == "HTTP Authentication":
					del wsbeat_data["http_authentication_user"]
					del wsbeat_data["http_authentication_password"]
				elif wsbeat_data["authentication_method"] == "API Key":
					del wsbeat_data["api_key_id"]
					del wsbeat_data["api_key"]
				del wsbeat_data["authentication_method"]
				self.logger.create_log("Modified configuration. Authentication was disabled.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			elif option == "Method":
				passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
				if wsbeat_data["authentication_method"] == "HTTP Authentication":
					option = self.dialog.create_radiolist("Select a option:", 9, 55, self.constants.OPTIONS_MODIFY_AUTHENTICATION, "HTTP Authentication")
					if option == "Disable":
						del wsbeat_data["http_authentication_user"]
						del wsbeat_data["http_authentication_password"]
						wsbeat_data["authentication_method"] = "API Key"
						api_key_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the API Key ID:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
						api_key = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
						wsbeat_data.update({"api_key_id" : api_key_id, "api_key": api_key})
						self.logger.create_log("Modified configuration. The authentication method was changed to API key.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
					elif option == "Data":
						options = self.dialog.create_checklist("Select one or more options:", 9, 55, self.constants.OPTIONS_HTTP_AUTHENTICATION, "HTTP Authentication")
						if "Username" in options:
							http_authentication_user = self.utils.encrypt_data(self.dialog.create_inputbox("Enter username:", 8, 50, "http_user"), passphrase)
							wsbeat_data["http_authentication_user"] = http_authentication_user
							self.logger.create_log("Modified configuration. HTTP Authentication User was modified.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
						if "Password" in options:
							http_authentication_password = self.utils.encrypt_data(self.dialog.create_passwordbox("Enter the password:", 8, 50, "password", True), passphrase)
							wsbeat_data["http_authentication_password"] = http_authentication_password
							self.logger.create_log("Modified configuration. HTTP Authentication Password was modified.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
				elif wsbeat_data["authentication_method"] == "API Key":
					option = self.dialog.create_radiolist("Select a option:", 9, 55, self.constants.OPTIONS_MODIFY_AUTHENTICATION, "HTTP Authentication")
					if option == "Disable":
						del wsbeat_data["api_key_id"]
						del wsbeat_data["api_key"]
						wsbeat_data["authentication_method"] = "HTTP Authentication"
						http_authentication_user = self.utils.encrypt_data(self.dialog.create_inputbox("Enter username:", 8, 50, "http_user"), passphrase)
						http_authentication_password = self.utils.encrypt_data(self.dialog.create_passwordbox("Enter the password:", 8, 50, "password", True), passphrase)
						wsbeat_data.update({"http_authentication_user" : http_authentication_user, "http_authentication_password": http_authentication_password})
						self.logger.create_log("Modified configuration. The authentication method was changed to HTTP Authentication.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
					elif option == "Data":
						options = self.dialog.create_checklist("Select one or more options:", 9, 55, self.constants.OPTIONS_API_KEY, "API Key")
						if "ID" in options:
							api_key_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the API Key ID:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
							wsbeat_data["api_key_id"] = api_key_id
							self.logger.create_log("Modified configuration. API Key ID was modified.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
						if "API Key" in options:
							api_key = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
							wsbeat_data["api_key"] = api_key
							self.logger.create_log("Modified configuration. API Key was modified.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		else:
			option = self.dialog.create_radiolist("Select a option:", 8, 55, self.constants.OPTIONS_NO_AUTHENTICATION, "Authentication Method")
			if option == "Enable":
				passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
				wsbeat_data["use_authentication"] = True
				option = self.dialog.create_radiolist("Select a option:", 9, 55, self.constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
				wsbeat_data.update({"authentication_method" : option})
				if option == "HTTP Authentication":
					http_authentication_user = self.utils.encrypt_data(self.dialog.create_inputbox("Enter username:", 8, 50, "http_user"), passphrase)
					http_authentication_password = self.utils.encrypt_data(self.dialog.create_passwordbox("Enter the password:", 8, 50, "password", True), passphrase)
					wsbeat_data.update({"http_authentication_user" : http_authentication_user, "http_authentication_password" : http_authentication_password})
					self.logger.create_log("Modified configuration. HTTP authentication was enabled.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
				elif option == "API Key":
					api_key_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the API Key ID:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
					api_key = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
					wsbeat_data.update({"api_key_id" : api_key_id, "api_key" : api_key})
					self.logger.create_log("Modified configuration. API Key authentication was enabled.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		return wsbeat_data


	def modify_index_name(self, wsbeat_data):
		"""
		Method that modifies the Index name.

		Returns a dictionary with the modified data.
		
		:arg wsbeat_data (Dict): Dictionary with configuration data.
		"""
		current_index_name = wsbeat_data["index_name"]
		index_name = self.dialog.create_inputbox("Enter the name of the index:", 8, 50, current_index_name)
		if not index_name == current_index_name:
			wsbeat_data["index_name"] = index_name
			self.logger.create_log("Modified configuration. Index name was modified.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			self.dialog.create_message("\nModified configuration. Index name was modified.", 8, 50, "Notification Message")
		else:
			self.dialog.create_message("\nConfiguration not modified.", 7, 50, "Notification Message")
		return wsbeat_data


	def modify_url(self, wsbeat_data):
		"""
		Method that modifies the URL.

		Returns a dictionary with the modified data.
		
		:arg wsbeat_data (Dict): Dictionary with configuration data.
		"""
		current_url = wsbeat_data["url"]
		url = self.dialog.create_inputbox("Enter the URL for communication via WebSocket:", 8, 50, current_url)
		if not url == current_url:
			wsbeat_data["url"] = url
			self.logger.create_log("Modified configuration. URL was modified.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			self.dialog.create_message("\nModified configuration. URL was modified.", 7, 50, "Notification Message")
		else:
			self.dialog.create_message("\nConfiguration not modified.", 7, 50, "Notification Message")
		return wsbeat_data


	def modify_bearer_token(self, wsbeat_data):
		"""
		Method that modifies the Bearer Token.

		Returns a dictionary with the modified data.
		
		:arg wsbeat_data (Dict): Dictionary with configuration data.
		"""
		current_bearer_token = wsbeat_data["bearer_token"]
		bearer_token = self.dialog.create_inputbox("Enter the Bearer Token:", 8, 50, current_bearer_token)
		if not bearer_token == current_bearer_token:
			wsbeat_data["bearer_token"] = bearer_token
			self.logger.create_log("Modified configuration. Bearer Token was modified.", 3, "_modifyConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			self.dialog.create_message("\nModified configuration. Bearer Token was modified.", 7, 50, "Notification Message")
		else:
			self.dialog.create_message("\nConfiguration not modified.", 7, 50, "Notification Message")
		return wsbeat_data


	def display_configuration(self):
		"""
		Method that displays the WSBeat configuration.
		"""
		try:
			data_string = self.utils.convert_yaml_data_to_string(self.constants.WSBEAT_CONFIGURATION_FILE)
			text = "\nWSBeat Configuration:\n\n" + data_string
			self.dialog.create_scrollbox(text, 18, 70, "WSBeat Configuration")
		except Exception as exception:
			self.dialog.create_message("\nError displaying WSBeat configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_displayConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")