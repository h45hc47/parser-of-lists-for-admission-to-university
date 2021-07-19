from parsers import parsers


def run():
    for parser in parsers:
        print(f"User parser <{parser.__class__.__name__}>")
        parser()


if __name__ == '__main__':
    run()
