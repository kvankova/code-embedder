import re


# Function verifying an email is valid
def verify_email(email: str) -> bool:
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is not None


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    # String representation of the class
    def __str__(self) -> str:
        return f"Person(name={self.name}, age={self.age})"
