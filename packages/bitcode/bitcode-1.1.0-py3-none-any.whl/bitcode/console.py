"""\
Reference: 123web.uk/bitpy/docs/console.html
"""

def write(*text, end="", split="", flush=True):
	"""Print the given text to stdout"""
	print(*text, end=end, sep=split, flush=flush)