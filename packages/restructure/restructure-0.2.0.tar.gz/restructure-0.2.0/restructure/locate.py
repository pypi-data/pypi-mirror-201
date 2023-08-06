def locate(index: str, data: dict, make_keys: bool = False):
	"""Locates the "target" key in a dictionary, as indexed using a key-path.

	Returns a tuple of the format (parent_dict, target_key)

	Does not assert that the target key exists, only tells you where it would be.

	e.g.

		index = key1.key2
		data = {
			'key1': {
				'key2': ...,
			},
		}
		return data['key1'], 'key2'

	When make_keys is True, creates parent keys along the way if they do not exist.

	:param index: The key-path to locate.
	:param data: The dictionary to search.
	:param make_keys: Whether to create parent keys along the way if they do not exist.
	:returns: A tuple of the format (parent_dict, target_key)
	:raises KeyError: A parent key along the key-path does not exist, and make_keys is False.
	:raises TypeError: A parent key along the key-path is not a dictionary.
	"""
	path = index.split('.')
	parent_dict = data

	for i, key in enumerate(path[:-1]):
		if make_keys:
			parent_dict = parent_dict.setdefault(key, {})
		else:
			try:
				parent_dict = parent_dict[key]
			except KeyError as e:
				raise KeyError(f'{".".join(path[:i + 1])} does not exist!') from e
			except TypeError as e:
				path_str = ".".join(path[:i])
				if path_str:
					path_str = f' at key: {path_str}'
				raise TypeError(f'Value{path_str} is not a dictionary!') from e

	if not isinstance(parent_dict, dict):
		raise TypeError(f'Value at key: {".".join(path[:-1])} is not a dictionary!')

	return parent_dict, path[-1]
