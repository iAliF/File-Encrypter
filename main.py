import argparse
import os
import zipfile
from typing import Optional

import pyAesCrypt

from utils import check_path

BUFFER_SIZE = 1024 * 64


def add_to_zip(path: str, output: str, is_dir: bool) -> str:
    zip_name = f"{output}.zip"
    zip_file = zipfile.ZipFile(zip_name, "w")

    if is_dir:
        for root, _, files in os.walk(path):
            for file in files:
                zip_file.write(os.path.join(root, file))
    else:
        zip_file.write(path)

    zip_file.close()

    return zip_name


def encrypt(path: str, passwd: str, output: Optional[str]) -> None:
    exists, is_dir = check_path(path)
    if not exists:
        print("Path Not Exists")
        return

    # First, we add folder/file to zip. Then we will encrypt the zip file.
    output = output or f"{path}.enc"
    zip_name = add_to_zip(path, output, is_dir)

    try:
        pyAesCrypt.encryptFile(zip_name, output, passwd, BUFFER_SIZE)
    except ValueError:
        # Todo: Handle errors
        print("Something went wrong")

    # Delete the zip file.
    os.remove(zip_name)

    print("Encrypted Successfully")


def decrypt_file(target: str, passwd: str) -> None:
    f_exists, _ = check_path(target)
    if not f_exists:
        print("Path Not Exists")
        return

    zip_name = f"{target}.zip"
    try:
        pyAesCrypt.decryptFile(target, zip_name, passwd, BUFFER_SIZE)

        zip_file = zipfile.ZipFile(zip_name)
        zip_file.extractall("./")
        zip_file.close()
        os.remove(zip_name)
        print("Decrypted Successfully")
    except ValueError:
        print(f"Something went wrong")


def main() -> None:
    parser = argparse.ArgumentParser()
    gp = parser.add_mutually_exclusive_group(required=True)
    gp.add_argument("-e", "--encrypt", help="Encrypt File/Folder", type=str)
    gp.add_argument("-d", "--decrypt", help="Decrypt File/Folder", type=str)
    parser.add_argument("-p", "--password", help="Password", type=str, required=True)
    parser.add_argument("-o", "--output", help="Output file", type=str)
    args = parser.parse_args()

    if args.encrypt:
        encrypt(args.encrypt, args.password, args.output)
    elif args.decrypt:
        decrypt_file(args.decrypt, args.password)


if __name__ == "__main__":
    main()
