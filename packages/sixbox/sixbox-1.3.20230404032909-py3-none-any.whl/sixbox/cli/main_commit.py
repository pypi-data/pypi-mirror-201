import os, sys
import uuid
import yaml
from .commands import  ( ValidateTag, ValidateCWL, askToUser, 
                        queryApp, removeApps, AppWriter, 
                        queryCase, removeCases, CaseWriter, 
                        ValidateCWLc, ValidateCaseTag, log,file_read, 
                        jsonstr2yamlstr, yamlstr2jsonstr, is_json )

from .commands.dataset_command import commit

"""
提交本地文件到仓库
"""


def commit_app(args, version):
    """
    CWL app以 yaml格式存储，依照惯例
    commit cwl app into local CWLdb
    """
    cwl_path = args.cwl_path
    cwl_info = args.cwl_info
    file_format = 0

    if cwl_path and os.path.exists(cwl_path): # 验证CWL文件是否有效
        if ValidateCWL(cwl_path):
            file_format = 1
        else:
            log.error('Syntax erro: The specified CWL contains error syntax, please check your CWL file ...')
            sys.exit()
    else:
        log.error('The CWL file you specified does not exist, please specify a valid path. ')
        sys.exit()

    if file_format == 1 and ValidateTag(cwl_info): # 如果cwl文件有效同时tag符合规定格式
        
        lst1 = cwl_info.split("/")
        lst2 = lst1[1].split(":")
        payload = {
            'name': lst2[0],
            'provider': lst1[0],
            'version': lst2[1],
            'resource_id': str(uuid.uuid4()),
            "type":0,
            # "profile": ''
        }
        app_uri = '{}/{}:{}'.format(
                    payload["provider"],  
                    payload["name"],  
                    payload["version"])
        # CWL 应用源码
        app = file_read(cwl_path)
        if is_json(app):
            app = jsonstr2yamlstr(app)
        
        app_dict = yaml.load(eval(repr(app)), Loader=yaml.FullLoader)
        
        payload["type"] = 0 if "class" in app_dict.keys() and app_dict["class"]=='CommandLineTool' else 1
        payload["content"] = app
  
        # # CWL 应用示例
        # if args.demo:
        #     payload["profile"] = file_read(args.demo)

        query = queryApp(app_uri)
        if query: # 如果存在，则替换
            log.warning('A CWL APP with the same name already exists. PLEASE confirm whether to replace it.')
            if askToUser(notes='Do you want to overwrite? Please input y/N: '):
                removeApps(app_uri)
                AppWriter(payload)
                
        else:
            AppWriter(payload)
         
        log.info("Successfully submit CWL file {} to CWLdb under the tag {} . ".format(cwl_path, app_uri))
        sys.exit()
    else:
        log.error('APP name is illegal, format must like `author/cwlname:version` ...')
        sys.exit()


def commit_case(args, version):
    """
    case 以json格式存储，对应的workflow和input字段都使用json格式。
    commit cwl case into local CWLdb
    """
    cwl_path = args.case_path
    cwl_info = args.case_info
    file_format = 0

    if cwl_path and os.path.exists(cwl_path): # 验证case 文件是否有效
        if ValidateCWLc(cwl_path):
            file_format = 1
        else:
            log.warning('Syntax erro: The specified case file contains error syntax, please check your case file ...')
            sys.exit()
    else:
        log.error('The case you specified does not exist, please specify a valid case address. ')
        sys.exit()

    if file_format == 1 and ValidateCaseTag(cwl_info): # 如果cwl文件有效同时tag符合规定格式
        
        payload = {
            'name': cwl_info.split("/")[1],
            'provider': cwl_info.split("/")[0],
            'resource_id': str(uuid.uuid4())
        }
        app_uri = '{}/{}'.format(
                    payload["provider"],  
                    payload["name"])

        case = file_read(cwl_path)
        if not is_json(case):
            try:
                case = yamlstr2jsonstr(case)
            except:
                log.error("Invalid format for {}, must be a json or yaml file".format(cwl_path))
        payload["content"] = case
        
        # 先查后改
        query = queryCase(app_uri)
        if query: # 如果存在，则替换
            log.warning('A case  with the same name already exists. PLEASE confirm whether to replace it.')
            if askToUser(notes='Do you want to overwrite? Please input y/N: '):
                removeCases(app_uri)
                CaseWriter(payload) 
        else:
            CaseWriter(payload)
         
        log.info("Successfully submit case file {} to local casedb under the tag {} . ".format(cwl_path, app_uri))
        sys.exit()
    else:
        log.error('The specified Case name is illegal, format must like `author/casename` ...')
        sys.exit()


def commit_dataset(args, version):
    """
    dataset 以json格式存储。
    commit dataset into local DATASETdb
    """
    # print("args: ", args)
    tg_dir = args.dir_path
    tag = args.dataset_info
    from_file = args.from_file
    secondaryFiles = args.secondaryFiles
    listFiles = args.listFiles

    commit(tag, tg_dir=tg_dir, from_file=from_file, secondaryFiles=secondaryFiles, listFiles=listFiles, sync=False)



