from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from dataclasses import dataclass
from libPyDialog import libPyDialog
from .Constants_Class import Constants

@dataclass
class Pipelines:

	name: str = None
	index_name: str = None
	websocket_url: str = None
	bearer_token: str = None


	def __init__(self):
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def define_name(self) -> None:
		"""
		Method that defines the name of the new pipeline.
		"""
		self.name = self.dialog.create_filename_inputbox("Enter the name of the pipeline:", 8, 50, "pipeline1")


	def define_index_name(self) -> None:
		"""
		Method that defines the name of the index where the data will be ingested.
		"""
		self.index_name = self.dialog.create_inputbox("Enter the index name:", 8, 50, "logs")


	def define_websocket_url(self) -> None:
		"""
		Method that defines the connection URL to the websocket.
		"""
		self.websocket_url = self.dialog.create_url_inputbox("Enter the URL for communication via WebSocket:", 8, 50, "wss://logs:443")


	def define_bearer_token(self) -> None:
		"""
		Method that defines the bearer token for authentication.
		"""
		self.bearer_token = self.dialog.create_inputbox("Enter the Bearer Token:", 8, 50, "3yqTaskewalsll98jkloper")


	def convert_object_to_dict(self) -> dict:
		"""
		Method that converts an object of type Pipelines into a dictionary.

		Returns:
			pipeline_data_json (dict): Dictionary with the object's data.
		"""
		pipeline_data_json = {
			"name" : self.name,
			"index_name" : self.index_name,
			"websocket_url" : self.websocket_url,
			"bearer_token" : self.bearer_token
		}
		return pipeline_data_json


	def create_file(self, pipeline_data: dict) -> None:
		"""
		Method that creates the YAML file corresponding to the pipeline.

		Parameters:
			pipeline_data (dict): Data to save in the YAML file.
		"""
		try:
			pipeline_file = f"{self.constants.PIPELINES_FOLDER}/{pipeline_data["name"]}.yaml"
			self.utils.create_yaml_file(pipeline_data, pipeline_file)
			self.utils.change_owner(pipeline_file, self.constants.USER, self.constants.GROUP, "644")
			if path.exists(pipeline_file):
				self.dialog.create_message(f"\nPipeline created: {pipeline_data["name"]}", 7, 50, "Notification Message")
				self.logger.create_log(f"Pipeline created: {pipeline_data["name"]}", 2, "__createPipeline", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except Exception as exception:
			self.dialog.create_message("\nError creating pipeline. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_createPipeline", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def convert_dict_to_object(self, pipeline_data: dict) -> None:
		"""
		Method that converts a dictionary into an object of type Pipelines.

		Parameters:
			pipeline_data (dict): Dictionary to convert.
		"""
		self.name = pipeline_data["name"]
		self.index_name = pipeline_data["index_name"]
		self.websocket_url = pipeline_data["websocket_url"]
		self.bearer_token = pipeline_data["bearer_token"]


	def modify_pipeline(self) -> None:
		"""
		Method that modifies the configuration of a pipeline.
		"""
		try:
			pipelines = self.utils.get_yaml_files_in_folder(self.constants.PIPELINES_FOLDER)
			if pipelines:
				pipelines.sort()
				tuple_to_rc = self.utils.convert_list_to_tuple_rc(pipelines, "Pipeline Name")
				option = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Pipeline(s)")
				options = self.dialog.create_checklist("Select one or more options:", 18, 70, self.constants.PIPELINE_FIELDS, "Pipeline Fields")
				pipeline_data = self.utils.read_yaml_file(f"{self.constants.PIPELINES_FOLDER}/{option}")
				self.convert_dict_to_object(pipeline_data)
				original_hash = self.utils.get_hash_from_file(f"{self.constants.PIPELINES_FOLDER}/{option}")
				if "Name" in options:
					print("Hola")
				if "Index" in options:
					print("Hola2")
				if "URL" in options:
					print("Hola3")
				if "Bearer Token" in options:
					print("Hola4")
				pipeline_data = self.convert_object_to_dict()
				self.utils.create_yaml_file(pipeline_data, f"{self.constants.PIPELINES_FOLDER}/{self.name}.yaml")
				new_hash = self.utils.get_hash_from_file(f"{self.constants.PIPELINES_FOLDER}/{self.name}.yaml")
				self.dialog.create_message("\nPipeline not modified.", 7, 50, "Notification Message") if new_hash == original_hash else self.dialog.create_message("\nPipeline modified.", 7, 50, "Notification Message")
			else:
				self.dialog.create_message(f"\nNo pipeline(s) in: {self.constants.PIPELINES_FOLDER}", 8, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError modifying pipeline configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_modifyPipeline", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def display_configuration(self) -> None:
		"""
		Method that displays the configuration of a pipeline.
		"""
		try:
			pipelines = self.utils.get_yaml_files_in_folder(self.constants.PIPELINES_FOLDER)
			if pipelines:
				pipelines.sort()
				tuple_to_rc = self.utils.convert_list_to_tuple_rc(pipelines, "Pipeline Name")
				option = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Pipeline(s)")
				pipeline_str = self.utils.convert_yaml_to_str(f"{self.constants.PIPELINES_FOLDER}/{option}")
				text = f"\n{option[:-5]}\n\n{pipeline_str}"
				self.dialog.create_scrollbox(text, 18, 70, "Pipeline Configuration") 
			else:
				self.dialog.create_message(f"\nNo pipeline(s) in: {self.constants.PIPELINES_FOLDER}", 8, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError displaying pipeline configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_displayPipelineConfig", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")
