"""\
Reference: 123web.uk/bitpy/docs/console.html
"""

def write(*text, end="", split="", flush=True):
	"""Print the given text to stdout"""
	print(*text, end=end, sep=split, flush=flush)

def writeln(*text, split="", flush=True):
	"""Print the given text to stdout, and appends a new line"""
	write(*text, end="\n", split=split, flush=flush)
