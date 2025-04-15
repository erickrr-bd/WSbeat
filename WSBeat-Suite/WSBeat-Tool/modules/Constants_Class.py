from typing import List
from dataclasses import dataclass, field

@dataclass(frozen = True)
class Constants:
	"""
	Message displayed in the background.
	"""
	BACKTITLE: str = "WSBEAT-TOOL v1.1 by Erick Rodriguez"

	"""
	WSBeat configuration file.
	"""
	WSBEAT_CONFIGURATION: str = "/etc/WSBeat-Suite/WSBeat/configuration/wsbeat.yaml"

	"""
	WSBeat-Agent configuration file.
	"""
	WSBEAT_AGENT_CONFIGURATION: str = "/etc/WSBeat-Suite/WSBeat-Agent/configuration/wsbeat_agent.yaml"

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
	LOG_FILE: str = "/var/log/WSBeat/wsbeat-tool-log"

	"""
	Owner user.
	"""
	USER: str = "wsbeat_user"

	"""
	Owner group.
	"""
	GROUP: str = "wsbeat_group"

	"""
	Options displayed in the "Main Menu".
	"""
	MAIN_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "Configuration"), ("2", "Pipelines"), ("3", "Service"), ("4", "About"), ("5", "Exit")])

	"""
	Options displayed in the "Configuration Menu".
	"""
	CONFIGURATION_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "WSBeat"), ("2", "WSBeat-Agent")])

	"""
	Options that are displayed when the configuration file doesn't exist.
	"""
	CONFIGURATION_OPTIONS_FALSE: List = field(default_factory = lambda : [("Create", "Create the configuration file", 0)])
	
	"""
	Options that are displayed when the configuration file exists.
	"""
	CONFIGURATION_OPTIONS_TRUE: List = field(default_factory = lambda : [("Modify", "Modify the configuration file", 0), ("Display", "Display the configuration file", 0)])

	"""
	Pipeline fields.
	"""
	PIPELINE_FIELDS: List = field(default_factory = lambda : [("Name", "Pipeline's name", 0), ("Index", "ElasticSearch's index name", 0), ("URL", "Websocket URL Connection", 0), ("Bearer Token", "Bearer Token", 0)])