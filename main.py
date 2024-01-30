import argparse

BUFFER_SIZE = 1024 * 64


def main() -> None:
    parser = argparse.ArgumentParser()
    gp = parser.add_mutually_exclusive_group(required=True)
    gp.add_argument("-e", "--encrypt", help="Encrypt File/Folder", type=str)
    gp.add_argument("-d", "--decrypt", help="Decrypt File/Folder", type=str)
    parser.add_argument("-p", "--password", help="Password", type=str, required=True)
    parser.add_argument("-o", "--output", help="Output file", type=str)
    args = parser.parse_args()


if __name__ == "__main__":
    main()
