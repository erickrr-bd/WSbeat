"""
Class that manages WSBeat constants.
"""
class Constants:
	"""
	Message displayed in the background.
	"""
	BACKTITLE = "WSBEAT-TOOLv1.0 by Erick Rodriguez"

	"""
	WSBeat configuration file path.
	"""
	WSBEAT_CONFIGURATION_FILE = "/etc/WSBeat-Suite/WSBeat/configuration/wsbeat.yaml"

	"""
	SSL certificate folder.
	"""
	SSL_CERTIFICATE_FOLDER = "/etc/WSBeat-Suite/WSBeat/certificates"

	"""
	Encryption key path.
	"""
	KEY_FILE = "/etc/WSBeat-Suite/WSBeat/configuration/key"

	"""
	WSBeat's log file.
	"""
	LOG_FILE = "/var/log/WSBeat/wsbeat-tool-log"

	"""
	Owner user.
	"""
	USER = "wsbeat_user"

	"""
	Owner group.
	"""
	GROUP = "wsbeat_group"

	"""
	Options displayed in the "Main Menu".
	"""
	OPTIONS_MAIN_MENU = [("1", "Configuration"),
						 ("2", "Service"),
						 ("3", "View Logs"),
						 ("4", "About"),
						 ("5", "Exit")]

	"""
	Options displayed in the "Configuration Menu".
	"""
	OPTIONS_CONFIGURATION_MENU = [("1", "WSBeat"),
					      		  ("2", "WSBeat-Agent")]

	"""
	Options displayed when WSBeat's configuration doesn't exist.
	"""
	OPTIONS_NO_CONFIGURATION = [("Create", "Create the configuration file", 0)]

	"""
	Options displayed when WSBeat's configuration exists.
	"""
	OPTIONS_YES_CONFIGURATION = [("Modify", "Modify the configuration file", 0),
								 ("Display", "Display the configuration file", 0)]

	"""
	Options displayed to select an authentication method.
	"""
	OPTIONS_AUTHENTICATION_METHOD = [("HTTP Authentication", "Use HTTP Authentication", 0),
								     ("API Key", "Use API Key", 0)]

	"""
	Options displayed when WSBeat settings are to be modified.
	"""
	OPTIONS_WSBEAT_CONFIGURATION = [("Host", "ElasticSearch Host", 0),
							 	    ("Port", "ElasticSearch Port", 0),
							 	 	("SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							 	 	("Authentication", "Enable or disable authentication method", 0),
							 	 	("Index", "Index name", 0),
							 	 	("URL", "Connection URL", 0),
							 	 	("Token", "Bearer Token", 0)]

	"""
	Options displayed in the "ElasticSearch Hosts Menu".
	"""
	OPTIONS_ES_HOSTS_MENU = [("1", "Add New Hosts"),
					   		 ("2", "Modify Hosts"),
					   		 ("3", "Remove Hosts")]

	"""
	Options displayed when the use of SSL/TLS is enabled.
	"""
	OPTIONS_YES_SSL = [("Disable", "Disable SSL/TLS communication", 0),
					   ("Certificate Verification", "Modify certificate verification", 0)]

	"""
	Options displayed when the use of SSL/TLS is disabled.
	"""
	OPTIONS_NO_SSL = [("Enable", "Enable SSL/TLS communication", 0)]

	"""
	Options displayed when certificate verification is enabled.
	"""
	OPTIONS_YES_VERIFICATE_CERTIFICATE = [("Disable", "Disable certificate verification", 0),
								   		  ("Certificate File", "Change certificate file", 0)]

	"""
	Options displayed when certificate verification is disabled.
	"""
	OPTIONS_VERIFICATE_CERTIFICATE_FALSE = [("Enable", "Enable certificate verification", 0)]

	"""
	Options displayed when an authentication method is enabled.
	"""
	OPTIONS_YES_AUTHENTICATION = [("Disable", "Disable authentication method", 0),
								  ("Method", "Modify authentication method", 0)]

	"""
	Options displayed when an authentication method is to be modified.
	"""
	OPTIONS_MODIFY_AUTHENTICATION = [("Disable", "Disable authentication method", 0),
									 ("Data", "Modify authentication method data", 0)]

	"""
	Options displayed when an authentication method is disabled.
	"""
	OPTIONS_NO_AUTHENTICATION = [("Enable", "Enable authentication", 0)]

	"""
	Options displayed when the authentication method is HTTP Authentication.
	"""
	OPTIONS_HTTP_AUTHENTICATION = [("Username", "Username for HTTP Authentication", 0),
								   ("Password", "User password", 0)]

	"""
	Options displayed when the authentication method is API Key.
	"""
	OPTIONS_API_KEY = [("ID", "API Key ID", 0),
					   ("API Key", "API Key", 0)]