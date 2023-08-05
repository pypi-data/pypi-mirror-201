import sys

from .commands import getApps, getCases, askToUser, Config,log

from sixbox.backend import Api
import sixbox.backend.errors

"""
实现push 本地CWLdb内CWL 到sixoclock仓库的功能
先检查校验CWL，然后提交
"""




def push_app(args, version):
    """
    push cwl file into online CWLdb
    """
    URI = args.pipes

    source = getApps(URI)

    pull_api = Api(Config["channel"], oauth_token=Config["token"])

    json_cols = ["name", "type", "website", "description", "category", "readme", "version", "profile", "content"]
    revision_cols = [ "version","content", "profile", "instruction"]
    if source != None:
        source = {item:source[item] for item in json_cols if item in source}

        # 现尝试创建，再尝试更新
        try:
            pipe = pull_api.apps.create_pipe(source)
            print("App {} pushed".format(URI))
            
        except sixbox.backend.errors.Unauthorized as err:
            log.warning('You are not login or login is expired  !')
        except sixbox.backend.errors.SbgError as err:
            if err.code == 204:
                if askToUser(notes='Do you want to overwrite the file? Please input Y/N: '):
            
                    pipe = pull_api.apps.get_pipe(err.data["id"])
                    CWL_revision = {item:source[item] for item in revision_cols if item in source}
                    revision = pull_api.apps.update_revision(pipe.pipe_id, pipe.resource_id, CWL_revision)
                    print("App {} pushed".format(URI))
                    sys.exit()
                    
                else:
                    # print(err)
                    sys.exit()
        except Exception as err:
            print(err)
    else:
        log.warning('Unable to find app  {} !'.format(URI))


def push_case(args, version):
    """
    push case into online
    """
    URI = args.cases

    source = getCases(URI)

    pull_api = Api(Config["channel"], oauth_token=Config["token"])

    json_cols = ["name", "type", "description", "category", "readme", "instruction", "content"]

    if source != None:
        source = {item:source[item] for item in json_cols if item in source}

        try:
            pipe = pull_api.cases.create_case(source)
            print("Case {} pushed".format(URI))
        except sixbox.backend.errors.Unauthorized as err:
            log.warning('you are not login or login is expired  !')
        except sixbox.backend.errors.SbgError as err:
            
            if err.code == 204:
                if askToUser(notes='Do you want to overwrite? Please input Y/N: '):
                    pipe = pull_api.cases.get_case(err.data["id"])
                    revision = pull_api.cases.update_case(pipe.resource_id, source)
                    print("case {} pushed".format(URI))
                    sys.exit()
                    
                else:
                    sys.exit()
            else:
                print(err)
    else:
        log.warning('Unable to find case  {} !'.format(URI))