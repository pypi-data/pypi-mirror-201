import re
import unittest

from restructure.combine import combine


class TestCombine(unittest.TestCase):
	def test_combine_two_dictionaries(self):
		left = {
			'key1': 'value1',
		}
		right = {
			'key2': 'value2',
		}
		expected = {
			'key1': 'value1',
			'key2': 'value2',
		}
		actual = combine(left, right)
		self.assertEqual(expected, actual)

	def test_combine_two_dictionaries_with_ignore(self):
		left = {
			'key1': 'value1',
		}
		right = {
			'key2': 'value2',
		}
		expected = {
			'key1': 'value1',
		}
		actual = combine(left, right, {'key2'})
		self.assertEqual(expected, actual)

	def test_combine_two_nested_dictionaries(self):
		left = {
			'key1': {
				'key2': 'value2',
			},
		}
		right = {
			'key1': {
				'key3': 'value3',
			},
		}
		expected = {
			'key1': {
				'key2': 'value2',
				'key3': 'value3',
			},
		}
		actual = combine(left, right)
		self.assertEqual(expected, actual)

	def test_combine_two_nested_dictionaries_with_ignore(self):
		left = {
			'key1': {
				'key2': 'value2',
			},
		}
		right = {
			'key1': {
				'key3': 'value3',
			},
		}
		expected = {
			'key1': {
				'key2': 'value2',
			},
		}
		actual = combine(left, right, {'key1.key3'})
		self.assertEqual(expected, actual)

	def test_combine_two_equal_values(self):
		left = 'value'
		right = 'value'
		actual = combine(left, right)
		self.assertEqual(left, actual)

	def test_combine_two_different_values(self):
		left = 'value1'
		right = 'value2'
		with self.assertRaisesRegex(KeyError, re.compile(r'cannot be combined', re.IGNORECASE)):
			combine(left, right)

	def test_combine_dictionaries_with_different_values(self):
		left = {
			'key1': 'value1',
		}
		right = {
			'key1': 'value2',
		}
		with self.assertRaisesRegex(KeyError, 'key1'):
			combine(left, right)

	def test_combine_nested_dictionaries_with_different_values(self):
		left = {
			'key1': {
				'key2': 'value1',
			},
		}
		right = {
			'key1': {
				'key2': 'value2',
			},
		}
		with self.assertRaisesRegex(KeyError, 'key1.key2'):
			combine(left, right)


if __name__ == '__main__':
	unittest.main()
