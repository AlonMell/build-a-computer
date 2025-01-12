import sys

with open(f"./{sys.argv[1]}.hack", "r") as f1, open(f"./tests/{sys.argv[1]}.hack", "r") as f2:
    for line1, line2 in zip(f1, f2):
            if line1.strip() != line2.strip():
                raise Exception("Files are not equal!")
print("Test successfull!")
