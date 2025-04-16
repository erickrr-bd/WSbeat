#! /usr/bin/env python3.12

"""
Main function.
"""
from modules.WSBeat_Class import WSBeat

if __name__ == "__main__":
	wsbeat = WSBeat()
	wsbeat.start_wsbeat()
