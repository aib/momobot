def from_file(filename):
	with open(filename, 'r') as f:
		return f.readlines()[0].strip()
