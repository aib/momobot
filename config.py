def from_file(filename):
	try:
		with open(filename, 'r') as f:
			return f.readlines()[0].strip()
	except FileNotFoundError:
		return None
