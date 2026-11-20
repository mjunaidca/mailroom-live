# mailroom-live: the starting point.
# Uses only ideas from lessons 13.1 to 13.7.


def greet(name: str) -> str:
    return "Hello from " + name + "!"


assert greet("mailroom-live") == "Hello from mailroom-live!", "greet should say hello"

print(greet("mailroom-live"))
