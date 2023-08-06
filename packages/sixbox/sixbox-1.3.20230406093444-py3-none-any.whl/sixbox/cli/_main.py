# -*- coding: utf-8 -*-
"""sixbox is a tool for managing and running CWL workflow.
sixbox provides the following commands:
    Information
    ===========
    config     : Modify configuration values in config.yaml
    cwls       : Show the existing CWL Workflow in cwldb

    Package Management
    ==================
    install    : install sixbox package
    update     : Updates sixbox package to the latest compatible version

    CWL Workflow Management
    =======================
    pull       : Get CWL Workflow from sixoclock.net
    commit     : Commit your CWL Workflow into your cwldb

    CWL Workflow Running
    ====================
    run        : running cwltool
Additional help for each command can be accessed by using:
    conda <command> -h
"""
import sys
from .commands import log

PARSER = None
# from .sixbox_parsers import generate_parser

def generate_parser():
    """
    定义一个parser处理函数，统一处理parse接口。
    """
    global PARSER
    if PARSER is not None:
        return PARSER
    from .sixbox_parsers import generate_parser
    PARSER = generate_parser()
    return PARSER


def main(*args, **kwargs):
    """
    sixbox cli 的main函数
    """
    
    if not args: # 依据系统判断
        # print('ok')
        if sys.platform == 'win32' and sys.version_info[0] == 2:
            args = sys.argv = win32_unicode_argv()
        else:
            args = sys.argv 

    sys_args = args # 记录以备用
    if len(args) == 1: # 默认打印sixbox帮助信息
        args = args + ['-h']

    if len(args) > 1:
 
        argv1 = args[1].strip()
        try:
            if argv1 == 'run':
            # run命令单独捕获错误并打印
                try:
                    p = generate_parser()
                    args = p.parse_args(args[1:])

                    from .sixbox_parsers import do_call
                    exit_code = do_call(args, p)
                    if isinstance(exit_code, int):
                        args = p.parse_args(sys_args[1:] + ['-h'])
                    # else:
                    #     # 交给cwltool
                    #     from cwltool import main
                    #     cmd = list(exit_code)
                    #     main.run(cmd)
                except Exception as err:
                    log.error(err)
                    # print(err)
            else:
                # 其它参数由argparser包管理
                p = generate_parser()
                args = p.parse_args(args[1:])

                from .sixbox_parsers import do_call
                exit_code = do_call(args, p)
                if isinstance(exit_code, int):
                    args = p.parse_args(sys_args[1:] + ['-h']) # 打印命令帮助信息
        except Exception as err:
            log.error('ERRO when run command: {} \n'.format(sys_args[1:]))
            log.error(err)
            # pass
            
            p = generate_parser()
            args = p.parse_args(sys_args[1:] + ['-h']) # 打印命令帮助信息



if __name__ == '__main__':
    sys.exit(main())

