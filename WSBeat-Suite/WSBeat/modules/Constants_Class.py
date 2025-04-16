from dataclasses import dataclass

@dataclass(frozen = True)
class Constants:
	"""
	WSBeat configuration file.
	"""
	WSBEAT_CONFIGURATION: str = "/etc/WSBeat-Suite/WSBeat/configuration/wsbeat.yaml"

	"""
	Pipelines path.
	"""
	PIPELINES_FOLDER: str = "/etc/WSBeat-Suite/WSBeat/pipelines"

	"""
	Encryption key path.
	"""
	KEY_FILE: str = "/etc/WSBeat-Suite/WSBeat/configuration/key"

	"""
	WSBeat-Tool log file.
	"""
	LOG_FILE: str = "/var/log/WSBeat/wsbeat-log"

	"""
	Owner user.
	"""
	USER: str = "wsbeat_user"

	"""
	Owner group.
	"""
	GROUP: str = "wsbeat_group"
