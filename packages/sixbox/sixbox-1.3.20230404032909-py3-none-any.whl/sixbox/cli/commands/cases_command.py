
import os, sys
import json
import yaml
from cwltool import main
from multiprocessing import Process, Lock


from .utils import check_uuid4, ValidateCaseTag, file_read, json2file, file2json, rand_string, is_json, is_yaml
from .db_command import libMaps
from .config_command import Config


################################
## CWL 读写相关
#########################################

def queryCase(URI):
    """
    查询并返回APP id
    """
    with open(libMaps["case_repositories"], 'r') as f:
        apps = json.load(f)

    # 指定查找
    if URI:
        querys = None
        # URI 为uuid4格式的CWL id
        if check_uuid4(URI):
            for case in apps.values():
                if case["resource_id"] == URI:
                    querys = case

        # URI 为tag
        if ValidateCaseTag(URI):
            try:
                querys = apps[URI]
            except:
                querys = None
    return querys


def getCases(URI=None):
    """
    从repositories.json中读取CWL Case信息
    """
    if URI:
        querys = queryCase(URI)
        if querys:
            with open(os.path.join(libMaps["case_metadata"], querys["resource_id"]), "r") as json_file: # 根据tag获取
                app= json.load(json_file)
            app['content'] = file_read(os.path.join(libMaps["case_content"], querys["resource_id"]))
            return app
        else:
            return None
    else:
        # 默认返回所有app
        with open(libMaps["case_repositories"], 'r') as f:
            apps = json.load(f)
        return apps.values()


def removeCases(URI=None):
    """
    删除
    """
    with open(libMaps["case_repositories"], 'r') as f:
        apps = json.load(f)
 
    querys = queryCase(URI) # 先查后删除
    if querys:
        os.remove(os.path.join(libMaps["case_metadata"], querys["resource_id"]))
        os.remove(os.path.join(libMaps["case_content"], querys["resource_id"]))
        # 更新case_repositories
        app_uri = '{}/{}'.format(
                            querys["provider"],  
                            querys["name"])
        apps = file2json(libMaps["case_repositories"])
        apps.pop(app_uri)
        json2file(libMaps["case_repositories"], apps)
        return True
    else:
        return False
 
def modifyCases(URI, payload):
    """
    修改标签
    """
 
    querys = queryCase(URI) # 先查后修改
    if querys:
        r_app_uri = '{}/{}'.format(
                    querys["provider"],  
                    querys["name"])
        q_app_uri ='{}/{}'.format(
                    payload["provider"],  
                    payload["name"])
        # 先读取内容
        with open(os.path.join(libMaps["case_metadata"], querys["resource_id"]), "r") as json_file: # 根据tag获取
                app= json.load(json_file)
        app.update(payload)

        # 更新仓库
        if q_app_uri != r_app_uri:
            # 当标签修改后，同步修改更新repositories
            CaseManifestWriter(app, old_uri=r_app_uri)
        else:
            CaseManifestWriter(app)

        
        # 修改 content
        isContent = True
        try:
            app['content']
        except:
            isContent = False
        CaseWriter(app, isMeta=True, isContent=isContent, isRepositories=False)

        return True
    else:
        return False



def CaseWriter(payload, isMeta=True, isContent=True, isRepositories=True):
    """
    CWL 写入db
    """
    if isContent:
        with open(os.path.join(libMaps["case_content"], payload["resource_id"]), 'w', encoding='utf-8') as f:
            f.write(payload["content"])
    if isMeta:
        with open(os.path.join(libMaps["case_metadata"], payload["resource_id"]), 'w', encoding='utf-8') as f:
            f.write(json.dumps(payload))

    if isRepositories:
        CaseManifestWriter(payload)


def CaseManifestWriter(payload, old_uri=None):
    """
    修改app 仓库文件
    """
    colFileds = ["provider", "name",  "resource_id", "type", "updated_at", "description"]
    app_uri = '{}/{}'.format(
                                    payload["provider"],  
                                    payload["name"])

    # 更新case_repositories
    apps = file2json(libMaps["case_repositories"])
    if old_uri:
        apps.pop(old_uri) # 删除旧数据

    apps[app_uri] = {k:payload[k] for k in payload.keys() if k in colFileds}
    json2file(libMaps["case_repositories"], apps)


def run_val(lock, cmd):
    """
    casetool main函数子进程函数
    """
    lock.acquire()
    main.run(cmd)
    lock.release()


def CWLcParser(case_fn):
    """
    解析cwlc，获取cwl与yml内容，接收文件路径或字符串或者字典
    """
  
    case_payload = file_read(case_fn)
 
    if is_json(case_payload):
        caseJson = file2json(case_fn)
    elif is_yaml(case_payload):
        caseJson = yaml.load(case_payload, Loader=yaml.FullLoader)
    if isCWLc(caseJson):
        return caseJson["workflow"], caseJson["input"]

    return None, None


def isCWLc(case:dict):
    """
    校验cwlc格式是否合法
    """

    keys = ["workflow", "input"]
    if set(keys).issubset(set(case.keys())):
        return True
    
    return False


def ValidateCWLc(case_path):
    """
    校验给定的CWL文件是否存在以及语法是否正确
    返回：ture，false
    """
    is_valid = False
    is_YMLvalid = False
    if case_path and os.path.exists(case_path): # 验证CWL文件是否有效
        # # 判断是否CWLc
        workflow, input = CWLcParser(case_path)
        casename = 'case-validate-' + rand_string()
        if workflow and input:
            cwl = os.path.join(libMaps["runtimes_tmp"], '{}.cwl'.format(casename))
            # 写入文件
            json2file(cwl, workflow)
            # json2file(yml, input)
        else:
            return False

        # 校验cwl
        cmd = ['--validate', cwl]
        lock = Lock()
        proc = Process(target=run_val, args=(lock, cmd,))
        proc.start()
        proc.join()
        if proc.exitcode == 0:
            is_CWLvalid = True
            os.remove(cwl)
        else:
            print('ERRO: The specified case\'s workflow contains error syntax, please check your case file in workflow field...')
            sys.exit()
        # 校验YML
        if isinstance(input, dict):
            is_YMLvalid = True
    else:
        print('ERRO: The case you specified does not exist, please specify a valid case address. ')
        sys.exit()

    if is_CWLvalid and is_YMLvalid:
        is_valid = True
    return is_valid
