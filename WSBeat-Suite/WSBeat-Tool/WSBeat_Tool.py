#! /usr/bin/env python3.12

from modules.WSBeat_Tool_Class import WSBeatTool

wsbeat_tool = WSBeatTool()

if __name__ == "__main__":
	while True:
		wsbeat_tool.main_menu()