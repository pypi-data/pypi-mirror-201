import os, sys

from cwltool import main
from .commands import getApps, libMaps, CWLJob, rand_string, CWLcParser, json2file, file_read, build_request
from shutil import copyfile
from .commands import log


def run(args, version):

    """
    处理CWL 流程运行

    """
    # 初始化变量
    cmd = []
    isyml = False   

    # 检查用户系统中docker运行环境
    docker=1
    udocker=0
    singularity=0
    for dockerpath in os.environ['PATH'].split(':'): # check docker
        # if os.path.isdir(dockerpath) and 'docker' in os.listdir(dockerpath):
        #     docker=1
        # if os.system('docker ps > /dev/null 2>&1') ==0:
        #     docker=1
        if os.path.isdir(dockerpath) and 'udocker' in os.listdir(dockerpath):
            udocker=1
        if os.path.isdir(dockerpath) and 'singularity' in os.listdir(dockerpath):
            singularity=1
    
    if (not args.udocker or not args.singularity):
        cmd =cmd
    elif udocker and (os.system('udocker ps > /dev/null 2>&1') ==0 or args.udocker):
        cmd.insert(0,"--udocker")
    elif singularity and (os.system('singularity ps > /dev/null 2>&1') ==0 or args.singularity):
         cmd.insert(0,"--singularity")
    else:
        log.warning("Docker or udocker or singularity is requied but not ready, please check if docker/udocker/singularity is inistalled!!!")
        sys.exit()

    if args.template:
        cmd.insert(0, "--make-template")

 
    if args.outdir:
        outdir = os.path.abspath(args.outdir)
        if os.path.exists(outdir):
            log.info("Set workdir to {}".format(outdir))
        else:
            log.warning('{} does not exists!!!!'.format(outdir))
            sys.exit()
    else:
        outdir=os.getcwd()
        # log.info('set workdir to {}'.format(os.getcwd()))

    cmd.extend(["--outdir" , outdir])

    # 生成一个随机数备用
    uid_str = rand_string(6)
    # 解析CWL路径
    try:
        cwl = args.cwl[0]
        if os.path.exists(cwl):
            # 读取本地CWL file
            jobName = '{}-{}'.format(os.path.basename(cwl), uid_str)
             # # 判断是否CWLc
            workflow, input = CWLcParser(cwl)
            if workflow:
                cwl = os.path.join(libMaps["runtimes_tmp"], '{}.cwl'.format(jobName))
                log.info("Copy CWL app file to {} for running ..".format(cwl))
                # 写入文件
                json2file(cwl, workflow)
               
            if input:
                yml = os.path.join(libMaps["runtimes_tmp"], '{}.yaml'.format(jobName))
                log.info("Copy CWL input file to {} for running ..".format(yml))
                json2file(yml, input)
                isyml = True
        else:
            # 读取cwl db内的app
            app = getApps(cwl)
            if app:
                jobName = '{}-{}'.format(app["name"], uid_str)
                # copy到临时目录进行计算
                cwl = os.path.join(libMaps["runtimes_tmp"], '{}.cwl'.format(
                        jobName))
                copyfile(os.path.join(libMaps["cwl_content"], app["resource_id"]), cwl)
                log.info("Copy CWL app file to {} for running ..".format(cwl))
            else:
                log.error('Unable to find CWL app in local CWLdb or the path that you specified! \
                    \nYou can try to pull apps from www.sixoclock.net with command:\n\tsixbox pull app {}'.format(cwl))
                sys.exit()

        cmd.append(cwl)

    except:
        log.warning('CWL app is needed!')
        sys.exit()


    # 解析 CWL 配置文件
    try:
        yml = args.cwl[1]
        if os.path.exists(yml):
            cmd.append( yml)
        else:    
            log.warning(" CWL app input file is needed !")
            sys.exit()
    except:
        if isyml:
            yml = yml
            cmd.append( yml)
        else:
            yml = None
    
    # 处理动态参数
    cmd.extend([*args.cwl_args])

    app = CWLJob()
    if cwl and yml:

        request = build_request(file_read(cwl), file_read(yml))
        print("Run as job with name: {} \n".format(jobName))
        # 交互运行
        app.inactivate_exec(cmd = cmd, request= request, name=jobName)
        # main.run(cmd)
        # 后台运行
        # app._exec(cmd = cmd, request= request, name=jobName)
        
    else:
        # 交给cwltool
        main.run(cmd)

