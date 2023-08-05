import os
import sys
from sixbox.backend import Api
import sixbox.backend.errors
from .commands import  Config, libMaps, Pretty_printer, log, Unauthorized_log


"""
搜索
"""


def search_app(args, version): 
    """
    search CWL-software from Sixoclock repository
    """
    term = args.term

    # 初始化table
    table = Pretty_printer(template= ["tag", "provider", "name","resource_id", "description"])
    api = Api(Config["channel"], oauth_token=Config["token"]) # fix: url要读取配置文件里的channel，（为什么要设置channel？参考conda配置文件~/.condarc里的channel）

    try: 
        pipes = api.apps.search(term)

    except sixbox.backend.errors.Unauthorized:
        Unauthorized_log()
        sys.exit()
    except Exception as err:
        print(err)
        log.error('somethings wrong')
        sys.exit()

        # 默认打印所有
    for app in pipes["data"]:    
        name = app["name"]
        provider = app["provider"]
        resource_id = app["resource_id"]
        description = app["description"]
        table.add_row(["{}/{}".format(provider, name), provider, name,  resource_id, description])
    print(table)


def search_case(args, version): 
    """
    search CWL-case from Sixoclock repository
    """
    term = args.term

    # 初始化table
    table = Pretty_printer(template= ["tag", "provider", "name","resource_id", "description"])
    api = Api(Config["channel"], oauth_token=Config["token"]) # fix: url要读取配置文件里的channel，（为什么要设置channel？参考conda配置文件~/.condarc里的channel）

    try: 
        pipes = api.cases.search(term)

    except sixbox.backend.errors.Unauthorized:
        Unauthorized_log()
        sys.exit()
    except Exception as err:
        print(err)
        log.error('somethings wrong')
        sys.exit()

        # 默认打印所有
    for app in pipes["data"]:    
        name = app["name"]
        provider = app["provider"]
        resource_id = app["resource_id"]
        description = app["description"]
        table.add_row(["{}/{}".format(provider, name), provider, name,  resource_id, description])
    print(table)