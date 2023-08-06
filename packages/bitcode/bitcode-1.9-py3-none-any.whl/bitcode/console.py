"""\
Reference: 123web.uk/bitpy/docs/console.html
"""

import os

def write(*text, end="", split="", flush=True):
	"""Print the given text to stdout"""
	print(*text, end=end, sep=split, flush=flush)

def writeln(*text, split="", flush=True):
	"""Print the given text to stdout, and appends a new line"""
	write(*text, end="\n", split=split, flush=flush)

def beep():
	"""Play the \\a 'beep' sound in the console"""
	write("\a")

def clear():
	"""Clear the console"""
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def prompt(return_type=str):
	"""Get user input"""
	error = None
	try:
		return return_type(input())
	except:
		error = TypeError(f"console.prompt: cannot convert user input to {return_type}")
	if error:
		raise error

def get_width():
	"""Get the width of the terminal"""
	return os.get_terminal_size().columns

#	"""Get the height of the terminal"""
def colour(ansi_colour):
	"""Add an ansi-modifier / colour to the terminal"""
	write(f"\u001b[{ansi_colour}m")
