def combine(left_value, right_value, ignore: set = None, __path: str = ''):
	"""Combines two values into one, if possible."""

	if ignore is None:
		ignore = set()

	if isinstance(left_value, dict) and isinstance(right_value, dict):
		from .merge import merge
		return merge(left_value, right_value, ignore, __path)
	elif left_value == right_value:
		return left_value
	else:
		# TODO: If types match & both support a combine method, such as a set union or list
		#       extend, use that instead of raising an error.
		if __path:
			raise KeyError(f'Conflict at key: {__path}')
		else:
			raise KeyError('Values cannot be combined.')
