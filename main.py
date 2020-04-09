import sys

from src.compatibility_caculator import compatibility_calculator

if len(sys.argv) <= 1:
    print("Usage: {} <Islander 1 Name>, <Islander 2 Name>, ...".format(sys.argv[0]), file=sys.stderr)
else:
    try:
        compatibility_calculator(sys.argv[1:])
    except ValueError as ve:
        print("{}".format(ve), file=sys.stderr)
