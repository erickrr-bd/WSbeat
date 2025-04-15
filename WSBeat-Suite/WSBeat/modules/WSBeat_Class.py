from os import path
from json import loads
from ssl import CERT_NONE
from libPyElk import libPyElk
from libPyLog import libPyLog
from datetime import datetime
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from websocket import setdefaulttimeout, WebSocketApp

"""
Class that manages the operation of WSbeat.
"""
class WSBeat:

	def __init__(self):
		"""
		Class constructor.
		"""
		setdefaulttimeout(10)
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.elasticsearch = libPyElk()


	def on_error(self, websocket_app, err):
		self.logger.create_log("Websocket error. For more information, see the logs.", 4, "_wsConnection", use_stream_handler = True)
		self.logger.create_log(err, 4, "_wsConnection", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def on_message(self, websocket_app, message):
		message_json = loads(message)
		print(message_json)


	def start_wsbeat(self):
		"""
		Method that starts the operation of WSBeat.
		"""
		try:
			self.logger.create_log("Author: Erick Roberto Rodríguez Rodríguez", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Github: https://github.com/erickrr-bd/Telk-Alert", 2, "_start", use_stream_handler = True)
			self.logger.create_log("WSBeat v1.0 - November 2024", 2, "_start", use_stream_handler = True)
			if path.exists(self.constants.WSBEAT_CONFIGURATION_FILE):
				self.logger.create_log("Reading configuration: " + self.constants.WSBEAT_CONFIGURATION_FILE, 2, "_readConfiguration", use_stream_handler = True)
				wsbeat_data = self.utils.read_yaml_file(self.constants.WSBEAT_CONFIGURATION_FILE)
				"""
				if wsbeat_data["use_authentication"]:
					if wsbeat_data["authentication_method"] == "HTTP Authentication":
						conn_es = self.elasticsearch.create_connection_ha(wsbeat_data, self.constants.KEY_FILE)
					elif wsbeat_data["authentication_method"] == "API Key":
						conn_es = self.constants.create_connection_ak(wsbeat_data, self.constants.KEY_FILE)
				else:
					conn_es = self.elasticsearch.create_connection_wa(wsbeat_data)
				self.logger.create_log("Connection established: " + ','.join(wsbeat_data["es_host"]) + " Port: " + str(wsbeat_data["es_port"]), 2, "_esConnection", use_stream_handler = True)
				self.logger.create_log("ElasticSearch Cluster Name: " + conn_es.info()["cluster_name"], 2, "_esConnection", use_stream_handler = True)
				self.logger.create_log("ElasticSearch Version: " + conn_es.info()["version"]["number"], 2, "_esConnection", use_stream_handler = True)
				self.logger.create_log("Connection established using SSL/TLS", 2, "_esConnection", use_stream_handler = True) if wsbeat_data["use_ssl"] else self.logger.create_log("Connection established without SSL/TLS. Not recommended for security reasons", 3, "_esConnection", use_stream_handler = True)
				self.logger.create_log("SSL certificate verification enabled", 2, "_esConnection", use_stream_handler = True) if wsbeat_data["verificate_certificate_ssl"] else self.logger.create_log("SSL certificate verification disabled. Not recommended for security reasons", 3, "_esConnection", use_stream_handler = True)
				if wsbeat_data["verificate_certificate_ssl"]:
					self.logger.create_log("Certificate file: " + wsbeat_data["certificate_file"], 2, "_esConnection", use_stream_handler = True)	
				self.logger.create_log("Authentication method enabled", 2, "_esConnection", use_stream_handler = True) if wsbeat_data["use_authentication"] else self.logger.create_log("Authentication method disabled. Not recommended for security reasons", 3, "_esConnection", use_stream_handler = True)
				if wsbeat_data["authentication_method"]:
					self.logger.create_log("Authentication Method: " + wsbeat_data["authentication_method"], 2, "_esConnection", use_stream_handler = True)
				headers = {"Authorization" : "Bearer {}".format(wsbeat_data["bearer_token"])}
				ssl_options = {"cert_reqs" : CERT_NONE}
				web_socket = create_connection(wsbeat_data["url"], header = headers, sslopt = ssl_options, timeout = 300,)
				self.logger.create_log("WebSocket Connection: " + wsbeat_data["url"], 2, "_wsConnection", use_stream_handler = True)
				while web_socket.connected:
					now = datetime.now()
					result = web_socket.recv()
					result_json = loads(result)
					result_json["@timestamp"] = datetime.utcnow().isoformat()
					self.elasticsearch.add_document_index(conn_es, wsbeat_data["index_name"] + '-' + str(now.date()), result_json)
					self.logger.create_log("New document added to the index: " + wsbeat_data["index_name"] + '-' + str(now.date()), 2, "_addDocument", use_stream_handler = True)
				"""
				ssl_options = {"cert_reqs" : CERT_NONE}
				websocket_app = WebSocketApp(wsbeat_data["url"], header = {"Authorization" : "Bearer {}".format(wsbeat_data["bearer_token"])}, on_message = self.on_message, on_error = self.on_error)
				websocket_app.run_forever(sslopt = ssl_options)
			else:
				self.logger.create_log("Configuration not found", 4, "_readConfiguration", use_stream_handler = True)
		except Exception as exception:
			self.logger.create_log("Error in WSBeat. For more information, see the logs.", 4, "_errorWSBeat", use_stream_handler = True)
			self.logger.create_log(exception, 4, "_errorWSBeat", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)