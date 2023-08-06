#!/usr/bin/env python3
import argparse
from pawnlib.builder.generator import generate_banner
from toolchains.__version__ import __full_version__ as toolchain_version
from pawnlib.output.color_print import *
from pawnlib.config import pawnlib_config as pawn, pconf
from pawnlib.utils import icx_signer
from pawnlib.utils.operate_handler import run_with_keyboard_interrupt
from pawnlib.input import PromptWithArgument

icx_signer.compressed = True

def get_parser():
    parser = argparse.ArgumentParser(description='ICON')
    parser = get_arguments(parser)
    return parser


def get_arguments(parser):
    parser.add_argument(
        'sub_command',
        help='create, load',
        nargs='?'
    )

    parser.add_argument('-pk', '--private-key', metavar='private_key', help='A private key string in hexadecimal. default: None',
                        default=None)
    parser.add_argument('-d', '--debug', action='store_true', help='debug mode. True/False', default=False)
    parser.add_argument('-k', '--keystore', metavar='keystore', help='keystore filename or keystore text')
    parser.add_argument('-p', '--password', metavar='password', help='keystore\'s password')
    parser.add_argument('-l', '--load-type', metavar='load_type', help='load type (file or text)', choices=["file", "text"])
    parser.add_argument('--base-dir', metavar='base_dir', help='base directory', default=os.getcwd())
    return parser

def private_key_validator(private_key):
    if icx_signer.is_private_key(private_key) or private_key == "":
        return True
    return "Invalid private key "


def least_length_validator(text, length=1):
    if len(text) >= length or text != "":
        return True
    return f"Must be at least {length} word(s) "


def main_program():
    banner = generate_banner(
        app_name="WALLET",
        author="jinwoo",
        description="Wallet tools",
        font="graffiti",
        version=toolchain_version
    )
    print(banner)
    parser = get_parser()
    args, unknown = parser.parse_known_args()

    if args.sub_command == "wallet":
        args.sub_command = None

    # pawn.console.log(f"args = {args}")
    args.subparser_name = "wallet"
    pawn.set(
        PAWN_DEBUG=args.debug,
        data=dict(
            args=args
        )
    )
    args.sub_command = PromptWithArgument(
        message="What do you want to do?",
        choices=
        [
            {"name": "Load wallet", "value": "load"},
            {"name": "Create wallet", "value": "create"},
        ],
        instruction="",
        max_height="40%",
        default="",
        argument="sub_command",
        verbose=0,
    ).fuzzy()

    pawn.console.log(f"sub_command = {args.sub_command}")

    wallet_cli = icx_signer.WalletCli(args=pconf().data.args)

    if args.sub_command == "load":
        # load_wallet()
        wallet_cli.load()

    elif args.sub_command == "create":
        wallet_cli.create()


def main():
    run_with_keyboard_interrupt(main_program)


if __name__ == '__main__':
    main()

