# -*- coding: utf-8 -*-
import sys
import argparse
from pawnlib.builder.generator import generate_banner
from pawnlib.__version__ import __version__ as _version
from pawnlib.config.globalconfig import pawnlib_config as pawn, pconf, Null
from concurrent.futures import ThreadPoolExecutor
# from pawnlib.utils.log import AppLogger
# from pawnlib.utils.http import disable_ssl_warnings
# from pawnlib.typing import check, converter
# from pawnlib.output import *
from pawnlib.output.color_print import *

from toolchains.utils import http
from toolchains.resource import CheckURL, ALLOW_OPERATOR
from pawnlib.typing import date_utils, str2bool, StackList
import time

import signal
from pawnlib.utils import handle_keyboard_interrupt_signal
import copy

# def handle_ctrl_c(signal, frame):
#     pawn.console.log(f"Got ctrl+c, going down! signal={signal}")
#     sys.exit(0)
# signal.signal(signal.SIGINT, handle_ctrl_c)

handle_keyboard_interrupt_signal()

__version__ = "0.0.1"


def get_parser():
    parser = argparse.ArgumentParser(description='HTTPING')
    parser = get_arguments(parser)
    return parser


def get_arguments(parser):
    parser.add_argument('url', help='url', type=str, nargs='?',default="")
    parser.add_argument('-c', '--command', type=str, help='command', default=None, choices=["start", "stop", "restart", None])
    parser.add_argument('-v', '--verbose', action='count', help='verbose mode. view level', default=0)
    parser.add_argument('-q', '--quiet', action='count', help='quiet mode', default=0)
    parser.add_argument('-s', '--sleep', type=float, help='sleep time seconds.', default=1)
    parser.add_argument('-m', '--method', type=lambda s : s.upper(), help='method.', default="get")
    parser.add_argument('-t', '--timeout', type=int, help='timeout seconds ', default=10)
    parser.add_argument('--success', nargs='+', help='success criteria.', default=['status_code==200'])
    parser.add_argument('--logical-operator',
                        type=str,
                        help='logical operator for checking success condition',
                        choices=["and", "or"],
                        default="and"
                        )
    parser.add_argument('--ignore-ssl', type=str2bool, help='ignore ssl certificate ', default=False)
    parser.add_argument('-d', '--data', type=json.loads, help="data parameter", default={})
    parser.add_argument('--headers', type=json.loads, help="header parameter", default={})
    parser.add_argument('-w', '--workers', type=int, help="max worker process", default=10)
    parser.add_argument('--stack-limit', type=int, help="error stack limit", default=3)

    return parser

def check_url_process(args):
    check_url = CheckURL(
        url=args.url,
        method=args.method,
        timeout=args.timeout * 1000,
        data=args.data,
        headers=args.headers,
        success_criteria=args.success,
        success_operator=args.logical_operator,
        ignore_ssl=args.ignore_ssl,
    )
    # pawn.increase(total_count=1)
    args.total_count += 1

    if args.verbose == 0:
        check_url.response.text = ""

    response_time = int(check_url.response.timing.get('total') * 1000)
    args.response_time.push(response_time)

    avg_response_time = f"{int(args.response_time.mean())}"
    max_response_time = f"{int(args.response_time.max())}"
    min_response_time = f"{int(args.response_time.min())}"
    status_code = check_url.response.status_code

    if args.fail_count > 0:
        count_msg = f'S:{args.error_stack_count}/[red]E:{args.fail_count}[/red]/T:{args.total_count}'
    else:
        count_msg = f'S:{args.error_stack_count}/E:{args.fail_count}/T:{args.total_count}'

    message = f"<{count_msg}> name={args.section_name}, url={args.url}, " \
              f"status_code={status_code}, {response_time:>4}ms " \
              f"(avg: {avg_response_time}, max: {max_response_time}, min: {min_response_time})"

    if args.verbose > 0:
        if status_code != 999:
            message = f"{message} 📄 [i]{check_url.response}[/i]"
        else:
            message = f"{message} 😞 "

    if check_url.is_success():
        pawn.console.log(f"[green][ OK ][/green] {message}")
    else:
        # pawn.increase(fail_count=1)
        args.fail_count += 1
        args.error_stack_count +=1

        if args.error_stack_count > args.stack_limit:
            pawn.console.log(f"[red][ERROR][/red] Error Stack Count: {args.error_stack_count}, SEND_SLACK")
            args.error_stack_count = 0

        pawn.console.log(f"[red][FAIL] {message}[/red][bold] Error={check_url.response.error}[/bold]")

    # pawn.console.log(res)
    return args

def check_url_loop(args=None, section_name=None):
    while True:
        check_url_process(args, section_name)
        time.sleep(args.sleep)

def convert_list_criteria(arguments):
    result = []
    for argument in arguments:
        criteria = convert_criteria(argument)
        if criteria:
            result.append(criteria)
    return result

def convert_criteria(argument):
    for operator in ALLOW_OPERATOR:
        if operator in argument:
            result = argument.split(operator)
            if any( word in result[0] for word in ALLOW_OPERATOR + ['=']):
                pawn.console.log(f"[red]Invalid operator - '{argument}', {result}")
                sys.exit(-1)
            result.insert(1, operator)
            return result
    return False

def _find_operator(operator, argument):
    if operator in argument:
        res = argument.split(operator)
        pawn.console(res)
        return operator, argument

# def _update_args_from_config():
#     pconfig = pconf().PAWN_CONFIG
#     config_file = pconf().PAWN_CONFIG_FILE
#     if pconfig.as_dict():
#         for section, section_value in pconfig.as_dict().items():
#             pawn.console.log(section, section_value)
#             for conf_key, conf_value in section_value.items():
#                 pawn.console.log(conf_key, conf_value)
#         pawn.console.log(f"Find config file={config_file}")
#         for key, value in pconfig.default.as_dict().items():
#             if getattr(pconf().args, key, None):
#                 pawn.console.log(f"Update argument from {config_file}, {key}={value} <ignore args={getattr(pconf().args, key, None)}>")
#                 setattr(pconf().args, key, value)

from  dataclasses import dataclass
from typing import Callable
from pawnlib.config import NestedNamespace

class ErrorCounter:
    def __init__(self, stack_overflow_callback: Callable=None, name="", stack_limit: int=5, max_error_count: int=10000):
        self.stack_overflow_callback = stack_overflow_callback
        self.name = name
        self.stack_limit = stack_limit
        self.max_error_count = max_error_count
        self.counter = NestedNamespace(
            name=self.name,
            stack=0,
            error=0,
            total=0
        )

    def count_up(self):
        self.counter.total += 1

    def error_up(self):
        if self.counter.error > self.max_error_count:
            self.counter.error = 0
        self.counter.error += 1
        self.counter.stack += 1
        if self.stack_limit and self.counter.stack >= self.stack_limit:
            if self.stack_overflow_callback:
                self.stack_overflow_callback(self.counter)
            self.counter.stack = 0

    def ns(self):
        return self.counter

    def get(self):
        return self.counter

    def __str__(self):
        return f"<ErrorCounter> {self.name} S:{self.counter.stack}/E:{self.counter.error}/T:{self.counter.total}"


def generate_task_from_config():
    tasks = []
    pconfig = pconf().PAWN_CONFIG
    config_file = pconf().PAWN_CONFIG_FILE
    pconf_dict = pconfig.as_dict()

    if pconf_dict:
        pawn.console.log(f"Found config file={config_file}")
        for section_name, section_value in pconf_dict.items():
            pawn.console.log(section_name, section_value)
            args = copy.deepcopy(pconf().args)
            args.section_name = section_name
            args.response_time = StackList()
            args.error_stack_count = 0
            args.total_count = 0
            args.fail_count = 0

            for conf_key, conf_value in section_value.items():
                if getattr(args, conf_key, None):
                    pawn.console.log(f"Update argument from {config_file}, <{section_name}> {conf_key}={conf_value} <ignore args={getattr(args, conf_key, None)}>")
                    setattr(args, conf_key, conf_value)
                    # if args_dict.get(key, None) is not None:
                    #     pawn.console.log(f"Update argument from {config_file}, {key}={value} <ignore args={args_dict.get(key)}>")
                    #     args_dict[key] = value
                    #     # setattr(args, key, value)

                    # tasks.append((args, section_name))
            tasks.append(args)
    return tasks




class ThreadPoolRunner:
    def __init__(self, func=None, tasks=[], max_workers=10, verbose=0):
        self.func = func
        self.tasks = tasks
        self.max_workers = max_workers
        self.results = []
        self.sleep = 1
        self.verbose = verbose

    def run(self):
        self.results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
        # for _args in tasks:
        #     # args, task_name = t
        #     # this_status = pool.submit(check_url_process,  args, task_name)
        #     thread_status = pool.submit(check_url_process,  _args, _args.section_name)
        #     pawn.console.log(f"{_args.section_name} -> {thread_status}")
            self.results = pool.map(self.func, self.tasks)

            if self.verbose > 0:
                for result in self.results:
                    pawn.console.log(result)

    def forever_run(self):
        while True:
            self.run()
            # pawn.console.log(self.results)
            time.sleep(self.sleep)


def main():
    banner = generate_banner(
        app_name="httping",
        author="jinwoo",
        description="http ping",
        font="graffiti",
        version=f"{__version__} - pawn({_version})"
    )
    print(banner)

    parser = get_parser()
    args, unknown = parser.parse_known_args()
    args.success = convert_list_criteria(args.success)

    pawn.set(
        args=args,
        try_pass=False,
        last_execute_point=0,
        data={
            "response_time": StackList(),
        },
        fail_count=0,
        total_count=0,
    )
    # _update_args_from_config()

    tasks = generate_task_from_config()

    pawn.console.log(tasks)

    from multiprocessing.pool import ThreadPool
    from multiprocessing import Queue
    from concurrent.futures import ThreadPoolExecutor

    # with ThreadPool(args.worker) as pool:
    #     pool.map(check_url_loop, tasks)
    ThreadPoolRunner(
        func=check_url_process,
        tasks=tasks,
        max_workers=args.workers
    ).forever_run()

    # with ThreadPoolExecutor(max_workers=args.worker) as pool:
    #     # for _args in tasks:
    #     #     # args, task_name = t
    #     #     # this_status = pool.submit(check_url_process,  args, task_name)
    #     #     thread_status = pool.submit(check_url_process,  _args, _args.section_name)
    #     #     pawn.console.log(f"{_args.section_name} -> {thread_status}")
    #     results = pool.map(check_url_process, tasks)
    #     for result in results:
    #         pawn.console.log(result)

    exit()

    pawn.console.log(args.__dict__)

    if args.quiet:
        pawn.console.log("Starting quiet mode")
        pawn.console = Null()
    if len(args.success) == 0:
        pawn.console.log("[yellow]Success criteria is empty. Skip HTTP condition checks")
        # sys.exit(f"Invalid arguments with success criteria = {args.success}")

    pawn.console.log(f"Success Criteria = {args.success}")

    args.try_pass = False

    if args.verbose > 2:
        pawn.set(PAWN_DEBUG=True)


    check_url_process(args)

    # while True:
    #     check_url_process(args)
    #     time.sleep(args.sleep)


if __name__ == "__main__":
    main()

