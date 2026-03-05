import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Utility functions for the project.")
    parser.add_argument("--example", type=str, help="An example argument.")
    args = parser.parse_args()
    return args

# EOF
