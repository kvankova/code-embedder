# README 3

This is a test README file for testing the code embedding process.

## Python objects

This section contains examples of Python objects.

```python:tests/data/example_python_objects.py:verify_email
def verify_email(email: str) -> bool:
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is not None
```

```python:tests/data/example_python_objects.py:Person
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    # String representation of the class
    def __str__(self) -> str:
        return f"Person(name={self.name}, age={self.age})"
```
