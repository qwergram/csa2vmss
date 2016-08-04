import sys

def parse(enum, content):
    if content.startswith("-") and '=' in content:
        return (content.split('=')[0][1:], content.split('=')[1])
    else:
        return enum, content

if __name__ == "__main__":
    params = {}
    for i, param in enumerate(sys.argv):
        param = parse(i, param)
        params[param[0]] = param[1]
    print(params)
