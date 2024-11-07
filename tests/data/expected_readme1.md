# README

This is a test readme.

This will be filled:
```python:tests/data/example_section.py:s:A
print("Printing only section A")
```

This won't be updated:
```yaml
name: Test
description: Description
```

This will be filled:
```python:tests/data/example_section.py:s:B
print("Printing only section B")
```

This won't be updated:
```
print("Hello, World!")
```

This will be updated:
```python:tests/data/example.py
print("Hello, World! from script")

```
