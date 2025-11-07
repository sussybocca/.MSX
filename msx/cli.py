# cli.py
import argparse
from .extension import create_extension
from .tester import test_extension
from .signer import sign_extension

def main():
    parser = argparse.ArgumentParser(description=".msx CLI")
    subparsers = parser.add_subparsers(dest="command")

    # create-extension command
    parser_create = subparsers.add_parser("create-extension")
    parser_create.add_argument("name", help="Extension name")

    # test-extension command
    parser_test = subparsers.add_parser("test-extension")
    parser_test.add_argument("path", help="Path to extension folder")

    # sign-extension command
    parser_sign = subparsers.add_parser("sign-extension")
    parser_sign.add_argument("path", help="Path to extension folder")

    args = parser.parse_args()

    if args.command == "create-extension":
        create_extension(args.name)
    elif args.command == "test-extension":
        test_extension(args.path)
    elif args.command == "sign-extension":
        sign_extension(args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
