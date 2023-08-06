import unittest

from dictanykey.dictanykey import DictAnyKey as TestClass


class TestInit(unittest.TestCase):
    def test_keys_values(self):
        d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two')])
        self.assertListEqual([1, 2, [1, 2]], d._get_keys_list())
        self.assertListEqual(['one', 'two', 'one two'], d._get_values_list())


class TestLen(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, 'one'), (2, 'two'), (3, 'three')])
        self.assertEqual(len(d), 3)
    
    def test_unhashable(self):
        d = TestClass([([1], 'one'), ([2], 'two'), ([1, 2], 'one two')])
        self.assertEqual(len(d), 3)

    def test_mix(self):
        d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two')])
        self.assertEqual(len(d), 3)

    def test_empty(self):
        d = TestClass()
        self.assertEqual(len(d), 0)


class TestDictConvert(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, 'one'), (2, 'two'), (3, 'three')])
        new_d = dict(d)
        self.assertEqual(d, new_d)


class TestIter(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, 'one'), (2, 'two'), (3, 'three')])
        iterator = iter(d)
        zero = next(iterator)
        self.assertEqual(zero, 1)
        one = next(iterator)
        self.assertEqual(one, 2)
        two = next(iterator)
        self.assertEqual(two, 3)
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_unhashable(self):
        d = TestClass([([1], 'one'), ([2], 'two'), ([1, 2], 'one two')])
        iterator = iter(d)
        zero = next(iterator)
        self.assertEqual(zero, [1])
        one = next(iterator)
        self.assertEqual(one, [2])
        two = next(iterator)
        self.assertEqual(two, [1, 2])
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_mix(self):
        d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two')])
        iterator = iter(d)
        zero = next(iterator)
        self.assertEqual(zero, 1)
        one = next(iterator)
        self.assertEqual(one, 2)
        two = next(iterator)
        self.assertEqual(two, [1, 2])
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_empty(self):
        d = TestClass()
        iterator = iter(d)
        with self.assertRaises(StopIteration):
            next(iterator)
    

class TestContains(unittest.TestCase):
    d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two')])

    def test_hashable(self):
        one_in = 1 in TestContains.d
        three_in = 3 in TestContains.d
        self.assertTrue(one_in)
        self.assertFalse(three_in)

    def test_unhashable(self):
        one_two_in = [1, 2] in TestContains.d
        one_one_in = [1, 1] in TestContains.d
        self.assertTrue(one_two_in)
        self.assertFalse(one_one_in)

    def test_dict_key(self):
        d = TestClass([({1: 'one', 2: 'two'}, 12), ])
        two_one_in = {2: 'two', 1: 'one'} in d
        two_three_in = {2: 'two', 3: 'three'} in d
        self.assertTrue(two_one_in)
        self.assertFalse(two_three_in)


class TestSetItem(unittest.TestCase):
    def test_new(self):
        d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two')])
        d[3] = 'three'
        self.assertListEqual([1, 2, [1, 2], 3], d._get_keys_list())
        self.assertListEqual(['one', 'two', 'one two', 'three'], d._get_values_list())

    def test_old(self):
        d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two')])
        d[1] = 'ONE'
        self.assertListEqual([1, 2, [1, 2]], d._get_keys_list())
        self.assertListEqual(['ONE', 'two', 'one two'], d._get_values_list())

    def test_dict_key_new(self):
        d = TestClass([({1: 'one', 2: 'two'}, 12), ])
        d[{3: 'three', 4: 'four'}] = 34
        self.assertListEqual([{2: 'two', 1: 'one'}, {4: 'four', 3: 'three'}], d._get_keys_list())
        self.assertListEqual([12, 34], d._get_values_list())

    def test_dict_key_old(self):
        d = TestClass([({1: 'one', 2: 'two'}, 12), ])
        d[{2: 'two', 1: 'one'}] = 2211
        self.assertListEqual([{2: 'two', 1: 'one'}], d._get_keys_list())
        self.assertListEqual([2211], d._get_values_list())


class TestGetItem(unittest.TestCase):
    d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two'), ({1: 'ONE', 2: 'TWO'}, 'ONE TWO')])

    def test_hashable(self):
        value = TestGetItem.d[1]
        self.assertEqual(value, 'one')

    def test_unhashable(self):
        value = TestGetItem.d[[1, 2]]
        self.assertEqual(value, 'one two')

    def test_dict_key(self):
        value = TestGetItem.d[{2: 'TWO', 1: 'ONE'}]
        self.assertEqual(value, 'ONE TWO')

    def test_key_error(self):
        with self.assertRaises(KeyError):
            value = TestGetItem.d[3]
        with self.assertRaises(KeyError):
            value = TestGetItem.d[{1: 'ONE'}]


class TestDel(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two')])
        del d[1]
        self.assertListEqual([2, [1, 2]], d._get_keys_list())
        self.assertListEqual(['two', 'one two'], d._get_values_list())

    def test_unhashable(self):
        d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two')])
        del d[[1, 2]]
        self.assertListEqual([1, 2], d._get_keys_list())
        self.assertListEqual(['one', 'two'], d._get_values_list())

    def test_dict_key(self):
        d = TestClass([({1: 'one', 2: 'two'}, 12), ({4: 'four', 3: 'three'}, 43)])
        del d[{3: 'three', 4: 'four'}]
        self.assertListEqual([{2: 'two', 1: 'one'}], d._get_keys_list())
        self.assertListEqual([12], d._get_values_list())
        
    def test_key_error(self):
        d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two')])
        with self.assertRaises(KeyError):
            del d[3]
        with self.assertRaises(KeyError):
            del d[[1, 1]]


class TestKeysMethod(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, 'one'), (2, 'two'), (3, 'three')])
        self.assertListEqual([1, 2, 3], d._get_keys_list())

    def test_unhashable(self):
        d = TestClass([([1, 1], 'one'), ([2, 8], 'two'), ([3, 9], 'three')])
        self.assertListEqual([[1, 1], [2, 8], [3, 9]], d._get_keys_list())

    def test_mix(self):
        d = TestClass([(1, 'one'), ([2, 2], 'two two'), (2, 'two')])
        self.assertListEqual([1, [2, 2], 2], d._get_keys_list())

    def test_empty(self):
        d = TestClass([])
        self.assertListEqual([], d._get_keys_list())


class TestValuesMethod(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, 'one'), (2, 'two'), (3, 'three')])
        self.assertListEqual(['one', 'two', 'three'], d._get_values_list())

    def test_unhashable(self):
        d = TestClass([([1, 1], 'one'), ([2, 8], 'two'), ([3, 9], 'three')])
        self.assertListEqual(['one', 'two', 'three'], d._get_values_list())

    def test_mix(self):
        d = TestClass([(1, 'one'), ([2, 2], 'two two'), (2, 'two')])
        self.assertListEqual(['one', 'two two', 'two'], d._get_values_list())

    def test_empty(self):
        d = TestClass([])
        self.assertListEqual([], d._get_keys_list())


class TestItemsMethod(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, 'one'), (2, 'two'), (3, 'three')])
        self.assertListEqual([(1, 'one'), (2, 'two'), (3, 'three')], d._get_items_list())

    def test_unhashable(self):
        d = TestClass([([1, 1], 'one'), ([2, 8], 'two'), ([3, 9], 'three')])
        self.assertListEqual([([1, 1], 'one'), ([2, 8], 'two'), ([3, 9], 'three')], d._get_items_list())

    def test_mix(self):
        d = TestClass([(1, 'one'), ([2, 2], 'two two'), (2, 'two')])
        self.assertListEqual([(1, 'one'), ([2, 2], 'two two'), (2, 'two')], d._get_items_list())

    def test_empty(self):
        d = TestClass([])
        self.assertListEqual([], d._get_items_list())


class TestGetMethod(unittest.TestCase):
    d = TestClass([(1, 'one'), (2, 'two'), ([1, 2], 'one two'), ({1: 'ONE', 2: 'TWO'}, 'ONE TWO')])

    def test_hashable(self):
        value = TestGetItem.d.get(1)
        self.assertEqual(value, 'one')

    def test_unhashable(self):
        value = TestGetItem.d.get([1, 2])
        self.assertEqual(value, 'one two')

    def test_dict_key(self):
        value = TestGetItem.d.get({2: 'TWO', 1: 'ONE'})
        self.assertEqual(value, 'ONE TWO')

    def test_default(self):
        value = TestGetItem.d.get(3, default='NaN')
        self.assertEqual(value, 'NaN')
        value = TestGetItem.d.get({1: 'ONE'}, 'Missing')
        self.assertEqual(value, 'Missing')


class TestCopyMethod(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, 'one'), (2, 'two'), (3, 'three')])
        c = d.copy()
        self.assertTrue(d == c)

    def test_unhashable(self):
        d = TestClass([([1, 1], 'one'), ([2, 8], 'two'), ([3, 9], 'three')])
        c = d.copy()
        self.assertTrue(d == c)

    def test_mix(self):
        d = TestClass([(1, 'one'), ([2, 2], 'two two'), (2, 'two')])
        c = d.copy()
        self.assertTrue(d == c)


class TestPopMethod(unittest.TestCase):
    def test_hashable(self):
        d = TestClass([(1, 'one'), (2, 'two'), (3, 'three')])
        value = d.pop(1)