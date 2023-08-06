from .combine import combine


def merge(left: dict, right: dict, ignore: set = None, __path: str = ''):
	"""Recursively merge two dictionaries.

	:param left: Left dictionary.
	:param right: Right dictionary.
	:param ignore: Keys to ignore when merging, specified as a set of key-paths.
	:param __path: Internal; used to track the key-path of the current merge operation.
	:return: Merged dictionary. Does not modify input dictionaries.
	:raises KeyError: A conflict is encountered.
	"""
	if ignore is None:
		ignore = set()

	keypath = keypath_for(__path)
	left_keys = set(left.keys())
	right_keys = set(right.keys())

	conflicts = left_keys & right_keys
	output = {}

	for key in conflicts:
		path = keypath(key)

		if path not in ignore:
			output[key] = combine(left[key], right[key], ignore, path)

	output.update(add_keys_from(left, left_keys, right_keys, ignore, __path))
	output.update(add_keys_from(right, right_keys, left_keys, ignore, __path))

	return output


def keypath_for(__path: str):
	"""Helper function to generate a keypath function for the current level of recursion."""

	def keypath(key_: str):
		# captures __path parameter
		return f'{__path}.{key_}' if __path else key_

	return keypath


def add_keys_from(data: dict, left_keys: set, right_keys: set, ignore: set, __path: str):
	"""Returns keys from data if the keys exist in left_keys and not right_keys."""
	keypath = keypath_for(__path)
	output = {}

	for key in left_keys - right_keys:
		path = keypath(key)

		if path in ignore:
			continue

		left_value = data[key]

		if isinstance(left_value, dict):
			output[key] = merge(left_value, {}, ignore, path)
		else:
			output[key] = left_value

	return output
