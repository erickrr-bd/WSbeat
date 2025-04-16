"""
Class that manages the operation of WSbeat.
"""
from os import path
from json import loads
from ssl import CERT_NONE
from threading import Thread
from libPyElk import libPyElk
from libPyLog import libPyLog
from datetime import datetime
from libPyUtils import libPyUtils
from .Constants_Class import Constants
from websocket import create_connection
from dataclasses import dataclass, field
from libPyConfiguration import libPyConfiguration

@dataclass
class WSBeat:

	logger: libPyLog = field(default_factory = libPyLog)
	utils: libPyUtils = field(default_factory = libPyUtils)
	constants: Constants = field(default_factory = Constants)
	elasticsearch: libPyElk = field(default_factory = libPyElk)


	def start_wsbeat(self) -> None:
		"""
		Method that starts WSBeat.
		"""
		try:
			self.logger.create_log("Author: Erick Roberto Rodríguez Rodríguez", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx", 2, "_start", use_stream_handler = True)
			self.logger.create_log("Github: https://github.com/erickrr-bd/WSbeat", 2, "_start", use_stream_handler = True)
			self.logger.create_log("WSBeat v1.1 - April 2025", 2, "_start", use_stream_handler = True)
			if path.exists(self.constants.WSBEAT_CONFIGURATION):
				self.logger.create_log(f"Configuration found: {self.constants.WSBEAT_CONFIGURATION}", 2, "_readConfiguration", use_stream_handler = True)
				configuration = libPyConfiguration()
				data = self.utils.read_yaml_file(self.constants.WSBEAT_CONFIGURATION)
				configuration.convert_dict_to_object(data)
				if configuration.use_authentication:
					if configuration.authentication_method == "HTTP Authentication":
						conn_es = self.elasticsearch.create_connection_http_auth(configuration, self.constants.KEY_FILE)
					elif configuration.authentication_method == "API Key":
						conn_es = self.elasticsearch.create_connection_api_key(configuration, self.constants.KEY_FILE)
				else:
					conn_es = self.elasticsearch.create_connection_without_auth(configuration)
				self.logger.create_log(f"Connection established: {','.join(configuration.es_host)}", 2, "_clusterConnection", use_stream_handler = True)
				self.logger.create_log(f"ElasticSearch Cluster Name: {conn_es.info()["cluster_name"]}", 2, "_clusterConnection", use_stream_handler = True)
				self.logger.create_log(f"ElasticSearch Cluster UUID: {conn_es.info()["cluster_uuid"]}", 2, "_clusterConnection", use_stream_handler = True)
				self.logger.create_log(f"ElasticSearch Version: {conn_es.info()["version"]["number"]}", 2, "_clusterConnection", use_stream_handler = True)
				if configuration.use_authentication:
					self.logger.create_log("Authentication enabled", 2, "_clusterConnection", use_stream_handler = True)
					self.logger.create_log("Authentication Method: HTTP Authentication", 2, "_clusterConnection", use_stream_handler = True) if configuration.authentication_method == "HTTP Authentication" else self.logger.create_log("Authentication Method: API Key", 2, "_clusterConnection", use_stream_handler = True)
				else:
					self.logger.create_log("Authentication disabled. Not recommended for security reasons.", 3, "_clusterConnection", use_stream_handler = True)
				self.logger.create_log("Certificate verification enabled", 2, "_clusterConnection", use_stream_handler = True) if configuration.verificate_certificate_ssl else self.logger.create_log("Certificate verification disabled. Not recommended for security reasons.", 3, "_clusterConnection", use_stream_handler = True)
				pipelines = self.utils.get_yaml_files_in_folder(self.constants.PIPELINES_FOLDER)
				if pipelines:
					self.logger.create_log(f"{str(len(pipelines))} pipeline(s) in: {self.constants.PIPELINES_FOLDER}", 2 , "_readPipelines", use_stream_handler = True)
					for pipeline in pipelines:
						pipeline_data = self.utils.read_yaml_file(f"{self.constants.PIPELINES_FOLDER}/{pipeline}")
						Thread(name = pipeline[:-5], target = self.start_pipeline, args = (conn_es, pipeline_data)).start()
				else:
					self.logger.create_log(f"No pipelines in: {self.constants.PIPELINES_FOLDER}", 3, "_readPipelines", use_stream_handler = True)
			else:
				self.logger.create_log("Configuration not found.", 4, "_readConfiguration", use_stream_handler = True)
		except Exception as exception:
			self.logger.create_log("Error starting WSBeat. For more information, see the logs.", 4, "_start", use_stream_handler = True)
			self.logger.create_log(exception, 4, "_start", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)


	def start_pipeline(self, conn_es, pipeline_data: dict) -> None:
		"""
		Method that executes a pipeline.

		Parameters:
			conn_es (ElasticSearch): A straightforward mapping from Python to ES REST endpoints.
			pipeline_data (dict): Dictionary with pipeline configuration.
		"""
		try:
			self.logger.create_log(f"Loading pipeline: {pipeline_data["name"]}", 2, "_loadPipeline", use_stream_handler = True)
			headers = {"Authorization" : "Bearer {}".format(pipeline_data["bearer_token"])}
			ssl_options = {"cert_reqs" : CERT_NONE}
			web_socket = create_connection(pipeline_data["websocket_url"], header = headers, sslopt = ssl_options, timeout = 300,)
			self.logger.create_log(f"WebSocket Connection: {pipeline_data["websocket_url"]}", 2, f"_{pipeline_data["name"]}", use_stream_handler = True)
			while web_socket.connected:
				now = datetime.now()
				result = web_socket.recv()
				result_json = loads(result)
				result_json["@timestamp"] = datetime.utcnow().isoformat()
				self.elasticsearch.add_new_document(conn_es, f"{pipeline_data["index_name"]}-{str(now.date())}", result_json)
				self.logger.create_log(f"New document added to the index: {pipeline_data["index_name"]}-{str(now.date())}", 2, f"_{pipeline_data["name"]}", use_stream_handler = True)
		except Exception as exception:
			self.logger.create_log(f"Error in pipeline: {pipeline_data["name"]}. For more information, see the logs.", 4, "_start", use_stream_handler = True)
			self.logger.create_log(exception, 4, f"_{pipeline_data["name"]}", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
