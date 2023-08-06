import sys
from helpers import make_more_human

# Accept an entire file as input
def main():
    if len(sys.argv) < 2:
        print("Usage: python testing.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, "r") as f:
        text: str = f.read()

    max_tokens = len(text) if len(text) < 4096 else 4096
    make_more_human(text, max_tokens=max_tokens)

def cli_entry_point():
    main()
