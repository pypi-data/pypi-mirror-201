#!/usr/bin/env python3
import argparse
from pawnlib.builder.generator import generate_banner
from pawnlib.__version__ import __version__ as _version
from pawnlib.output.color_print import *
from pawnlib.config import pawnlib_config as pawn
from pawnlib.output import write_json
from pawnlib.resource import server
from pawnlib.typing.generator import json_rpc, random_token_address
from pawnlib.utils import IconRpcHelper, IconRpcTemplates
from InquirerPy import prompt
from pawnlib.utils import disable_ssl_warnings
from pawnlib.input import PromptWithArgument, PrivateKeyValidator, StringCompareValidator, PrivateKeyOrJsonValidator

disable_ssl_warnings()


def get_parser():
    parser = argparse.ArgumentParser(description='ICON')
    parser = get_arguments(parser)
    return parser


def get_arguments(parser):
    parser.add_argument(
        'command',
        help='account, icx_sendTransaction, icx_sendTransaction_v3, get_transactionResult, icx_getBalance, icx_getTotalSupply',
        nargs='?'
    )
    parser.add_argument('--url', metavar='url',
                        help=f'loopchain baseurl. default: None', default=None)
    parser.add_argument('--from', metavar='address', dest='from_addr',
                        help=f'from address. default: None', default=None)
    parser.add_argument('--to', metavar='address', dest="to_addr",
                        help=f'to address. default: None', default=None)
    parser.add_argument('--address', metavar='address',
                        help=f'icx address. default: None', default=None)
    parser.add_argument('--txhash', metavar='txhash', help='txhash')
    parser.add_argument('--icx', metavar='amount', type=float,
                        help=f'icx amount to transfer. unit: icx. ex) 1.0. default:0.001', default=0.001)
    parser.add_argument('--fee', metavar='amount', type=float,
                        help='transfer fee. default: 0.01', default=0.001)
    parser.add_argument('--pk', metavar='private_key',
                        help=f'hexa string. default: None', default=None)
    parser.add_argument('--debug', action='store_true', help=f'debug mode. True/False')
    parser.add_argument('-n', '--number', metavar='number', type=int,
                        help=f'try number. default: None', default=None)

    parser.add_argument('--nid', metavar='nid', type=str, help=f'network id default: None', default=None)

    parser.add_argument('-c', '--config', metavar='config',
                        help=f'config name')

    parser.add_argument('-k', '--keystore-name', metavar='key_store',
                        help=f'keystore file name')

    parser.add_argument('-p', '--password', metavar='password',
                        help=f'keystore file password')

    parser.add_argument('-t', '--timeout', metavar='timeout', type=float, help=f'timeout')
    parser.add_argument('-w', '--worker', metavar='worker', type=int, help=f'worker')
    parser.add_argument('-i', '--increase', metavar='increase_count', type=int, help=f'increase count number')
    parser.add_argument('--increase-count', metavar='increase_count', type=int, help=f'increase count number', default=1)

    parser.add_argument('-r', '--rnd_icx', metavar='rnd_icx', help=f'rnd_icx', default="no")

    parser.add_argument('-m', '--method', metavar='method', help='method for JSON-RPC', default="")

    return parser


def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers['size'] == 'jumbo':
        options.append('helicopter')
    return options


def get_methods(answers):
    icon_tpl = IconRpcTemplates()
    return icon_tpl.get_methods(answers['category'])


def get_required(answers):
    icon_tpl = IconRpcTemplates(category=answers['category'], method=answers['method'])
    pawn.console.log(f"get_required => {icon_tpl.get_required_params()}, {answers['category']}, {answers['method']}")

    return icon_tpl.get_required_params()


def main():
    banner = generate_banner(
        app_name="RPC",
        author="jinwoo",
        description="JSON-RPC request",
        font="graffiti",
        version=_version
    )
    print(banner)

    parser = get_parser()
    args, unknown = parser.parse_known_args()
    args.subparser_name = "icon"
    pawn.set(
        PAWN_DEBUG=args.debug,
        data=dict(
            args=args
        )
    )
    pawn.console.log(f"args = {args}")

    icon_tpl = IconRpcTemplates()
    # print(icon_tpl.get_category())
    # print(icon_tpl.get_methods())

    category = None
    if not args.method:
        category = PromptWithArgument(
            message="Select a category to use in JSON-RPC.",
            choices=icon_tpl.get_category(),
            long_instruction="\nUse the up/down keys to select",
            max_height="40%",
            default="",
            argument="",
        ).select()

    PromptWithArgument(
        message=">> Select a method to use in JSON-RPC.",
        choices=icon_tpl.get_methods(category=category),
        long_instruction="\nUse the up/down keys to select",
        type="list",
        max_height="40%",
        default="",
        argument="method",
    ).select()



    if args.command == "rpc":
        pawn.console.log("Interactive Mode")
        questions = [
            {
                'type': 'list',
                'name': 'category',
                'message': 'What do you want to do?',
                'choices': icon_tpl.get_category() + ["wallet"],
                #     [
                #     'Order a pizza',
                #     'Make a reservation',
                #     Separator(),
                #     'Ask for opening hours',
                #     {
                #         'name': 'Contact support',
                #         'disabled': 'Unavailable at this time'
                #     },
                #     'Talk to the receptionist'
                # ]
            },
            {
                'type': 'list',
                'name': 'method',
                'message': 'Which vehicle you want to use for delivery?',
                # 'choices': lambda cate: icon_tpl.get_methods(answers['category']),
                'choices': get_methods,
            },
        ]

        answers = prompt(questions)
        dump(answers)
        payload = icon_tpl.get_rpc(answers['category'], answers['method'])
        required_params = icon_tpl.get_required_params()

        if required_params:
            _questions = []
            for k, v in required_params.items():
                _questions.append({'type': 'input', 'name': k.lower(), 'message': f'What\'s "{k}" parameter?'})
                # from 주소면 wallet 디렉토리를 읽어서 리스트를 보여준다.

            payload['params'] = prompt(_questions)

        pawn.console.log(f"payload={payload}")
        res = IconRpcHelper().rpc_call(url=args.url, payload=payload)
        dump(res)


if __name__ == '__main__':
    main()
