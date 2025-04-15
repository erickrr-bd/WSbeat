#! /usr/bin/env python3.12

"""
Main function.
"""
from modules.WSBeat_Tool_Class import WSBeatTool

if __name__ == "__main__":
	wsbeat_tool = WSBeatTool()
	while True:
		wsbeat_tool.main_menu()
