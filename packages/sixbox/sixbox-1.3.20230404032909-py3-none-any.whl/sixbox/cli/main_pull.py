import os
import sys
from sixbox.backend import Api
import sixbox.backend.errors

from .commands import AppWriter, Config, libMaps, CaseWriter, log, Unauthorized_log


"""
This file contains the code to pull the CWL Workflow  from the sixboclock official website
find_metadata function can find CWL Workflow metadata path
find_resource function can find CWL Workflow content path
read_channel functionn can get channel from config.yaml
"""


def pull_app(args,version): 
    """
    pull CWL-software from Sixoclock repository
    """
    pipe_id = args.app

    pull_api = Api(Config["channel"], oauth_token=Config["token"]) # fix: url要读取配置文件里的channel，（为什么要设置channel？参考conda配置文件~/.condarc里的channel）

    if not pipe_id:
        Unauthorized_log()
        sys.exit()
    else:
        try: 
            # TODO: 整合为一个api，不要调用2次
            pipes = pull_api.apps.get_pipe(pipe_id)
            pull_api.apps.pull(pipes.pipe_id)
        except sixbox.backend.errors.Unauthorized:
            Unauthorized_log()
            sys.exit()
        except:
            log.info('Unable to find CWL app {} in www.sixoclock.net. '.format(pipe_id))
            sys.exit()

    if pipes.resource_id in os.listdir(libMaps["cwl_metadata"]) and not args.force:  # 判断cwldb中是否有重复的CWL
        log.warning("The CWL has already exists in CWLdb! If you want to pull force, please use command:\n\tsixbox pull pipe_id --force")
        sys.exit()
    else:
        # 写入db
        payload = {
            **pipes._meta,
            "content": pipes.content,
            "profile": pipes.profile,
        }
        AppWriter(payload)

        log.info('Pulled CWL {} as  {}/{}:{}'.format(pipe_id, 
                                                    pipes._meta["provider"],  
                                                    pipes._meta["name"],  
                                                    pipes._meta["version"]))

def pull_case(args, version): 
    """
    pull CWL-case from Sixoclock repository
    """
    pipe_id = args.case

    pull_api = Api(Config["channel"], oauth_token=Config["token"]) # fix: url要读取配置文件里的channel，（为什么要设置channel？参考conda配置文件~/.condarc里的channel）

    if not pipe_id:
        Unauthorized_log()
        sys.exit()
    else:
        try: 
            pipes = pull_api.cases.get_case(pipe_id)
 
        except sixbox.backend.errors.Unauthorized:
            Unauthorized_log()
            sys.exit()
        except:
            log.info('Unable to find case {} in www.sixoclock.net. '.format(pipe_id))
            sys.exit()

    if pipes.resource_id in os.listdir(libMaps["case_metadata"]) and not args.force:  # 判断cwldb中是否有重复的CWL
        log.warning("Case has already exists in CWLdb! If you want to pull force, please use command: \n\tsixbox pull case tag_or_id --force")
        sys.exit()
    else:
        # 写入db
        payload = {
            **pipes._meta,
            "content": pipes.content
        }
        CaseWriter(payload)
        
        log.info('Pulled case {} as  {}/{}'.format(pipe_id, 
                                                    pipes._meta["provider"],  
                                                    pipes._meta["name"]))