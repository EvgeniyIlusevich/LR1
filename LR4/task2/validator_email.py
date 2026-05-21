import re

def is_valid_email(line):
    return re.match(r'^[\w.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', line) is not None