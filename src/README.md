# Med-Ex Source Code

This directory contains the source code for the Med-Ex prototype. This prototype has been built primarily for Linux-based (particularly Debian-based) systems and uses a command line interface. The program runs locally and is not connected to a cloud-based server as of yet. To run the program, one can run main.py using any standard python interface (such as conda or python3), preferably on a terminal. However, a bash script (run_tool.sh) has also been prepared to ease the usage by users comfortable with terminal interface.

## Prerequisites

1. **Python 3.8 or higher.**
2. **Crypto**
	```shell
	pip3 install pycrypto
	```
3. **Bullet**
	```shell
	pip3 install bullet
	```
4. **PrettyTable**
	```shell
	pip3 install prettytable
	```
