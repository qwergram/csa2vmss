import sys

def parse_input(defaults=None):
    if defaults is None: defaults = {}
    for item in sys.argv[1:]:
        if item.startswith('-') and '=' in item:
            key, value = item[1:].split('=', 1)
            if value.isdigit(): value = int(value)
            elif value.replace('.', '').isdigit(): value = float(value)
            elif value.lower() == "true": value = True
            elif value.lower() == "false": value = False
            defaults[key] = value
    return defaults