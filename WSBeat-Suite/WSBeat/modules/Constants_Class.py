"""
Class that manages WSBeat constants.
"""
class Constants:
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
	LOG_FILE = "/var/log/WSBeat/wsbeat-log"

	"""
	Owner user.
	"""
	USER = "wsbeat_user"

	"""
	Owner group.
	"""
	GROUP = "wsbeat_group"