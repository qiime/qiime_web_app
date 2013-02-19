
def export_grid(grid_data, headers):
	""" Accepts headers (as a tuple), and a list of data (as tuples)
		and produces tabular data
	"""
	# Write the header row
	data = '\t'.join(map(str, list(headers))) + '\n'

	# Write the individual rows
	for row in grid_data:
		data += '\t'.join(map(str, list(row))) + '\n'

	return data
