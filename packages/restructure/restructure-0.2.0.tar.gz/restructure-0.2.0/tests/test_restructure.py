import copy
import unittest

from restructure import restructure


class TestRestructure(unittest.TestCase):
	def test_no_operations(self):
		data = {
			'key1': 'value1',
		}
		spec = {}
		expected = {
			'key1': 'value1',
		}
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_simple(self):
		data = {
			'key1': 'value1',
		}
		spec = {
			'key1': 'key2',
		}
		expected = {
			'key2': 'value1',
		}
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_preserves_unspecified(self):
		data = {
			'key1': 'value1',
			'key3': 'value3',
		}
		spec = {
			'key1': 'key2',
		}
		expected = {
			'key2': 'value1',
			'key3': 'value3',
		}
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_same_key(self):
		data = {
			'key1': 'value',
		}
		spec = {
			'key1': 'key1',
		}
		expected = copy.deepcopy(data)
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_nested(self):
		data = {
			'key1': {
				'key2': {
					'key3': 'value',
				},
			},
		}
		spec = {
			'key1.key2.key3': 'key.data',
		}
		expected = {
			'key': {
				'data': 'value',
			},
		}
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_same_key_nested(self):
		data = {
			'key1': {
				'key2': {
					'key3': 'value',
				},
			},
		}
		spec = {
			'key1.key2.key3': 'key1.key2.key3',
		}
		expected = copy.deepcopy(data)
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_swap_keys(self):
		data = {
			'key1': 'value1',
			'key2': 'value2',
		}
		spec = {
			'key1': 'key2',
			'key2': 'key1',
		}
		expected = {
			'key1': 'value2',
			'key2': 'value1',
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)

	def test_swap_keys_nested(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
			'key3': {
				'key4': 'value2',
			},
		}
		spec = {
			'key1.key2': 'key3.key4',
			'key3.key4': 'key1.key2',
		}
		expected = {
			'key1': {
				'key2': 'value2',
			},
			'key3': {
				'key4': 'value1',
			},
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)

	def test_reverse_nesting(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
		}
		spec = {
			'key1.key2': 'key2.key1',
		}
		expected = {
			'key2': {
				'key1': 'value1',
			},
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)

	def test_swap_nested_key_order(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
			'key3': {
				'key4': 'value2',
			},
		}
		spec = {
			'key1.key2': 'key4.key3',
			'key3.key4': 'key2.key1',
		}
		expected = {
			'key4': {
				'key3': 'value1',
			},
			'key2': {
				'key1': 'value2',
			},
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)

	def test_swap_keys_nested_sibling(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
			'key3': {
				'key4': 'value2',
			},
		}
		spec = {
			'key1.key2': 'key3.key5',
		}
		expected = {
			'key3': {
				'key4': 'value2',
				'key5': 'value1',
			},
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)

	def test_move_to_separate_flat_key(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
		}
		spec = {
			'key1.key2': 'key3',
		}
		expected = {
			'key3': 'value1',
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)

	def test_move_to_same_flat_key(self):
		data = {
			'key1': {
				'key2': {
					'key3': 'value1',
				},
			},
		}
		spec = {
			'key1.key2.key3': 'key1',
		}
		expected = {
			'key1': 'value1',
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)

	def test_move_to_nested(self):
		data = {
			'key1': 'value1',
		}
		spec = {
			'key1': 'key1.key2.key3',
		}
		expected = {
			'key1': {
				'key2': {
					'key3': 'value1',
				},
			},
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)

	def test_key_conflict(self):
		data = {
			'key1': 'value1',
			'key2': 'value2',
		}
		spec = {
			'key1': 'key2',
		}
		expected = copy.deepcopy(data)
		with self.assertRaises(KeyError):
			restructure(data, spec)
		self.assertEqual(expected, data)

	def test_key_spec_conflict(self):
		data = {
			'key1': 'value1',
			'key3': 'value2',
		}
		spec = {
			'key1': 'key2',
			'key3': 'key2',
		}
		expected = copy.deepcopy(data)
		with self.assertRaises(KeyError):
			restructure(data, spec)
		self.assertEqual(expected, data)

	def test_data_key_contains_delimiter(self):
		data = {
			'key1': {
				'key2.key3': ...,
			},
		}
		spec = {
			'key1.key2.key3': 'key1.data',
		}
		with self.assertRaises(KeyError):
			restructure(data, spec)

	def test_operations_preserve_input_data(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
		}
		spec = {
			'key1.key2': 'key3',
		}
		expected = copy.deepcopy(data)
		restructure(data, spec)
		self.assertEqual(expected, data)

	def test_multiple_from_one_chain(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
		}
		spec = {
			'key1': 'key3',
			'key1.key2': 'key4',
		}
		expected = {
			'key3': {
				'key2': 'value1',
			},
			'key4': 'value1',
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)

	def test_duplicate_destinations(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
		}
		spec = {
			'key1': 'key3',
			'key1.key2': 'key3',
		}
		with self.assertRaisesRegex(KeyError, r'key3'):
			restructure(data, spec)

	def test_duplicate_set_destinations(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
		}
		spec = {
			'key1': {'key3', 'key4'},
			'key1.key2': 'key3',
		}
		with self.assertRaisesRegex(KeyError, r'key3'):
			restructure(data, spec)

	def test_multiple_destinations_same_source(self):
		data = {
			'key1': 'value1',
		}
		spec = {
			'key1': {'key2', 'key3'},
		}
		expected = {
			'key2': 'value1',
			'key3': 'value1',
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)
		self.assertIs(data['key2'], data['key3'])

	def test_multiple_nested_same_source(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
		}
		spec = {
			'key1.key2': {'key3.key4', 'key5.key6'},
		}
		expected = {
			'key3': {
				'key4': 'value1',
			},
			'key5': {
				'key6': 'value1',
			},
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)
		self.assertIs(data['key3']['key4'], data['key5']['key6'])

	def test_preserve_by_self_in_destinations(self):
		data = {
			'key1': 'value1',
		}
		spec = {
			'key1': {'key1', 'key2'},
		}
		expected = {
			'key1': 'value1',
			'key2': 'value1',
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)
		self.assertIs(data['key1'], data['key2'])

	def test_preserve_nested_by_self_in_destinations(self):
		data = {
			'key1': {
				'key2': 'value1',
			}
		}
		spec = {
			'key1.key2': {'key1.key2', 'key3.key4'},
		}
		expected = {
			'key1': {
				'key2': 'value1',
			},
			'key3': {
				'key4': 'value1',
			},
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)
		self.assertIs(data['key1']['key2'], data['key3']['key4'])

	def test_copy_to_parents_and_child(self):
		data = {
			'key1': {
				'key2': {
					'key3': 'value1',
				},
			},
		}
		spec = {
			'key1.key2.key3': {'key1.key2.key3.key4', 'key1.key2.key5', 'key1.key6', 'key7'},
		}
		expected = {
			'key1': {
				'key2': {
					'key3': {
						'key4': 'value1',
					},
					'key5': 'value1',
				},
				'key6': 'value1',
			},
			'key7': 'value1',
		}
		data = restructure(data, spec)
		self.assertEqual(expected, data)

	def test_copy_to_parent_conflict(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
		}
		spec = {
			'key1.key2': {'key1.key2', 'key1'},
		}
		with self.assertRaisesRegex(KeyError, r'key1'):
			restructure(data, spec)

	def test_copy_to_child_conflict(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
		}
		spec = {
			'key1.key2': {'key1.key2', 'key1.key2.key3'},
		}
		with self.assertRaisesRegex(KeyError, r'key1.key2'):
			restructure(data, spec)

	def test_parent_to_last_child(self):
		data = {
			'key1': {
				'key2': {
					'key3': 'value1',
				},
			},
		}
		spec = {
			'key1.key2': 'key1.key2.key3',
		}
		actual = restructure(data, spec)
		expected = {
			'key1': {
				'key2': {
					'key3': {
						'key3': 'value1',
					},
				},
			},
		}
		self.assertEqual(expected, actual)

	def test_merge_dictionaries(self):
		data = {
			'key1': {
				'key2': {
					'key3': 'value1',
				},
			},
			'key4': {
				'key5': 'value2',
			},
		}
		spec = {
			'key4': 'key1.key2',
		}
		expected = {
			'key1': {
				'key2': {
					'key3': 'value1',
					'key5': 'value2',
				},
			},
		}
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_merge_dictionary_and_value(self):
		data = {
			'key1': {
				'key2': {
					'key3': 'value1',
				},
			},
			'key4': {
				'key5': 'value2',
			},
			'key6': 'value1',
		}
		spec = {
			'key4': 'key1.key2',
			'key6': 'key1.key2.key3',
		}
		expected = {
			'key1': {
				'key2': {
					'key3': 'value1',
					'key5': 'value2',
				},
			},
		}
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_clear_flat_key_by_None(self):
		data = {
			'key1': 'value1',
		}
		spec = {
			'key1': None,
		}
		expected = {}
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_clear_flat_key_by_empty_string(self):
		data = {
			'key1': 'value1',
		}
		spec = {
			'key1': '',
		}
		expected = {}
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_clear_child_key_clears_empty_chain(self):
		data = {
			'key1': {
				'key2': 'value1',
			},
		}
		spec = {
			'key1.key2': None,
		}
		expected = {}
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)

	def test_clear_child_key(self):
		data = {
			'key1': {
				'key2': 'value1',
				'key3': 'value2',
			},
		}
		spec = {
			'key1.key2': None,
		}
		expected = {
			'key1': {
				'key3': 'value2',
			},
		}
		actual = restructure(data, spec)
		self.assertEqual(expected, actual)


if __name__ == '__main__':
	unittest.main()
