import unittest

from restructure.locate import locate


class TestLocate(unittest.TestCase):
	def test_locate_key_exists_flat(self):
		data = {
			'key1': ...,
		}
		parent, key = locate('key1', data)
		self.assertIs(data, parent)
		self.assertEqual(key, 'key1')

	def test_locate_key_does_not_exist_flat(self):
		data = {}
		parent, key = locate('key1', data)
		self.assertIs(data, parent)
		self.assertEqual(key, 'key1')

	def test_locate_key_exists_nested(self):
		data = {
			'key1': {
				'key2': ...,
			},
		}
		parent, key = locate('key1.key2', data)
		self.assertIs(data['key1'], parent)
		self.assertEqual(key, 'key2')

	def test_locate_key_does_not_exist_nested(self):
		data = {
			'key1': {},
		}
		parent, key = locate('key1.key2', data)
		# locate does not assert that the target key exists, it only tells you where it would be.
		self.assertIs(data['key1'], parent)
		self.assertEqual(key, 'key2')

	def test_locate_parent_does_not_exist(self):
		data = {}
		with self.assertRaisesRegex(KeyError, r'key1 does not exist'):
			# Because locate only tells you where the target key would be, must use an extra key
			# `key2` to attempt to access `key1` which does not exist.
			locate('key1.key2', data)

	def test_locate_nested_parent_does_not_exist(self):
		data = {
			'key1': {},
		}
		with self.assertRaisesRegex(KeyError, r'key1.key2 does not exist'):
			# Must use an additional key `key3` to attempt to access `key2` which does not exist.
			locate('key1.key2.key3', data)

	def test_locate_parent_is_not_a_dictionary(self):
		data = {
			'key1': ...,
		}
		with self.assertRaisesRegex(TypeError, r'Value at key: key1 is not a dictionary'):
			locate('key1.key2', data)

	def test_locate_nested_parent_is_not_a_dictionary(self):
		data = {
			'key1': {
				'key2': ...,
			},
		}
		with self.assertRaisesRegex(TypeError, r'Value at key: key1.key2 is not a dictionary'):
			locate('key1.key2.key3', data)

	def test_locate_input_is_not_a_dictionary(self):
		data = ...
		with self.assertRaisesRegex(TypeError, r'Value is not a dictionary'):
			locate('key1.key2.key3', data)

	def test_located_parent_is_not_a_dictionary(self):
		data = {
			'key1': ...,
		}
		with self.assertRaisesRegex(TypeError, r'Value at key: key1 is not a dictionary'):
			locate('key1.key2', data)

	def test_located_nested_parent_is_not_a_dictionary(self):
		data = {
			'key1': {
				'key2': ...,
			},
		}
		with self.assertRaisesRegex(TypeError, r'Value at key: key1.key2 is not a dictionary'):
			locate('key1.key2.key3', data)


if __name__ == '__main__':
	unittest.main()
