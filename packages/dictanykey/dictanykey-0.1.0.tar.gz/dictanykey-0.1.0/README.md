# DictAnyKey: Python Dictionary That Can Use Any Key
[![PyPI Latest Release](https://img.shields.io/pypi/v/dictanykey.svg)](https://pypi.org/project/dictanykey/)

## What is it?

**DictAnyKey** is a Python package that provides a dictionary like object that can use unhashable keys (such as list and dict) as well as hashable keys.

## Main Features
Here are just a few of the things that DictAnyKey does well:
  
  - Use unhashable objects as keys, such as list and dict but with slower retrieval.
  - Stores and retrieves values using hashable keys at same speed as built in dict.
  - Maintains order of insertion just like built in dict.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/eddiethedean/dictanykey

```sh
# PyPI
pip install dictanykey
```

## Dependencies
- [python >= 3.6]

## Example
```sh
from dictanykey import DictAnyKey

# Start with empty DictAnyKey
d = DictAnyKey()

# Add value with unhashable key
d[[1, 2]] = 'one two'

# Add value with hashable key
d[1] = 'one'

# Get value with key
d[[1, 2]] -> 'one two'

str(d) -> '{[1, 2]: "one two", 1: "one"}'

# Delete items with del
del d[[1, 2]]

# Start with filled in DictAnyKey, use list of tuples
d = DictAnyDict([([2, 2], 'two two'), (2, 'two')])

str(d) -> '{[2, 2]: "two two", 2: "two"}'

# Has keys, values, and items methods (all results are iterable)
d.keys() -> DictKeys([[2, 2], 2])
d.values() -> DictValues('two two', 'two')
d.items() -> DictItems([([2, 2], 'two two'), (2, 'two')])

# check for key membership
[2, 2] in d -> True
[3, 4] in d -> False

# Has get method with default parameter
d.get(5, default='Missing') -> 'Missing'
d.get([2, 2], default='Missing') -> 'two two'
```