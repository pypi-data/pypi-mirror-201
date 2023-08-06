import unittest

from restructure.merge import merge


class TestMerge(unittest.TestCase):
	def test_merge_flat(self):
		data1 = {
			'key1': 'value1',
		}
		data2 = {
			'key2': 'value2',
		}
		expected = {
			'key1': 'value1',
			'key2': 'value2',
		}
		output = merge(data1, data2)
		self.assertEqual(expected, output)

	def test_merge_nested(self):
		data1 = {
			'key1': {
				'key2': 'value1',
			},
		}
		data2 = {
			'key1': {
				'key3': 'value2',
			},
		}
		expected = {
			'key1': {
				'key2': 'value1',
				'key3': 'value2',
			},
		}
		output = merge(data1, data2)
		self.assertEqual(expected, output)

	def test_merge_ignore_flat(self):
		data1 = {
			'key1': 'value1',
		}
		data2 = {
			'key2': 'value2',
			'key3': 'value3',
		}
		expected = {
			'key1': 'value1',
			'key2': 'value2',
		}
		output = merge(data1, data2, ignore={'key3', })
		self.assertEqual(expected, output)

	def test_merge_ignore_nested(self):
		data1 = {
			'key1': {
				'key2': 'value2',
			},
		}
		data2 = {
			'key1': {
				'key3': 'value3',
				'key4': 'value4',
			},
		}
		expected = {
			'key1': {
				'key2': 'value2',
				'key3': 'value3',
			},
		}
		output = merge(data1, data2, ignore={'key1.key4', })
		self.assertEqual(expected, output)

	def test_merge_ignore_nested_root(self):
		data1 = {
			'key1': {
				'key2': 'value2',
			},
		}
		data2 = {
			'key1': {
				'key3': 'value3',
				'key4': 'value4',
			},
		}
		expected = {}
		output = merge(data1, data2, ignore={'key1', })
		self.assertEqual(expected, output)

	def test_merge_equal_data(self):
		data1 = {
			'key1': 'value1',
		}
		data2 = {
			'key1': 'value1',
		}
		expected = {
			'key1': 'value1',
		}
		output = merge(data1, data2)
		self.assertEqual(expected, output)

	def test_merge_conflict(self):
		data1 = {
			'key1': 'value1',
		}
		data2 = {
			'key1': 'value2',
		}
		with self.assertRaisesRegex(KeyError, 'key1'):
			merge(data1, data2)

	def test_nested_merge_conflict(self):
		data1 = {
			'key1': {
				'key2': 'value1',
			},
		}
		data2 = {
			'key1': {
				'key2': 'value2',
			},
		}
		with self.assertRaisesRegex(KeyError, 'key1.key2'):
			merge(data1, data2)

	def test_merge_preserves_input_data(self):
		data1 = {
			'key1': 'value1',
		}
		data2 = {
			'key2': 'value2',
		}
		merge(data1, data2)
		self.assertEqual({'key1': 'value1'}, data1)
		self.assertEqual({'key2': 'value2'}, data2)


if __name__ == '__main__':
	unittest.main()
