import argparse

parser = argparse.ArgumentParser()
parser.add_argument("a")
args = parser.parse_args()

print(args.a)

