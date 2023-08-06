#!/usr/bin/env python
# -*- coding: utf-8 -*-
# * filename   : jdb_py.py
# * created at : 2023-04-06 12:35:19
# * Author     : xiliuya <xiliuya@aliyun.com>

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

from subprocess import Popen, PIPE

from pygments import highlight
from pygments.lexers import JavaLexer
from pygments.formatters import Terminal256Formatter, TerminalFormatter

import os
import time
import sys

jdb_completer = WordCompleter([
    'run', 'threads', 'thread', 'suspend', 'resume', 'where', 'wherei', 'up',
    'down', 'kill', 'interrupt', 'print', 'dump', 'eval', 'set', 'locals',
    'classes', 'class', 'methods', 'fields', 'threadgroups', 'threadgroup',
    'stop in', 'stop at', 'clear', 'catch', 'ignore', 'watch', 'unwatch',
    'trace', 'untrace', 'step', 'step up', 'next', 'stepi', 'cont', 'list',
    'use', 'exclude', 'classpath', 'monitor', 'unmonitor', 'read', 'lock',
    'threadlocks', 'pop', 'reenter', 'redefine', 'disablegc', 'enablegc', '!!',
    '#', 'help', 'version', 'exit', 'quit', 'method'
],
                              ignore_case=True)


def print_usage():
    usage_str = '''Usage: jdb-py <options> <class> <arguments>

where options include:
    -? -h --help -help print this help message and exit
    -sourcepath <directories separated by ":">
                      directories in which to look for source files
    -attach <address>
                      attach to a running VM at the specified address using standard connector
    -listen <address>
                      wait for a running VM to connect at the specified address using standard connector
    -listenany
                      wait for a running VM to connect at any available address using standard connector
    -launch
                      launch VM immediately instead of waiting for 'run' command
    -listconnectors   list the connectors available in this VM
    -connect <connector-name>:<name1>=<value1>,...
                      connect to target VM using named connector with listed argument values
    -dbgtrace [flags] print info for debugging jdb
    -tclient          run the application in the HotSpot(TM) Client Compiler
    -tserver          run the application in the HotSpot(TM) Server Compiler

options forwarded to debuggee process:
    -v -verbose[:class|gc|jni]
                      turn on verbose mode
    -D<name>=<value>  set a system property
    -classpath <directories separated by ":">
                      list directories in which to look for classes
    -X<option>        non-standard target VM option

<class> is the name of the class to begin debugging
<arguments> are the arguments passed to the main() method of <class>
    '''
    print(usage_str)


def main(jdb_commond=''):
    # 启动 jdb
    jdb_process = Popen('jdb ' + jdb_commond,
                        shell=True,
                        stdin=PIPE,
                        stdout=PIPE)
    term_format = Terminal256Formatter if os.getenv(
        'TERM') == 'xterm-256color' else TerminalFormatter

    try:
        while True:
            user_input = prompt('>>> ',
                                history=FileHistory('jdb_history.txt'),
                                auto_suggest=AutoSuggestFromHistory(),
                                completer=jdb_completer)

            # 交互 jdb
            if user_input == '':
                user_input = '!!'

            input_str = user_input + '\n'
            jdb_process.stdin.write(input_str.encode('utf-8'))
            jdb_process.stdin.flush()
            jdb_process.stdout.flush()

            # 以下延时为经验值
            time.sleep(0.3)
            line = jdb_process.stdout.read1(10000).decode('utf-8')
            print(highlight(line, JavaLexer(), term_format()))

            # 退出 jdb
            if user_input.strip().lower() == 'exit' or user_input.strip(
            ).lower() == 'quit':
                jdb_process.terminate()
                break
    except (KeyboardInterrupt, EOFError):
        jdb_process.terminate()
    except BrokenPipeError:
        print('BrokenPipeError')


def run():
    print(sys.argv[1:])
    commond = ' '.join(sys.argv[1:])
    if commond == '-h' or commond == '--help':
        print_usage()
    else:
        main(commond)
        print('jdb is shutdown.')


if __name__ == "__main__":
    run()
