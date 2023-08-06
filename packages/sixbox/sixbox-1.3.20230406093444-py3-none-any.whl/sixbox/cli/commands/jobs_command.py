import os, sys,io
import yaml
import json
import shutil
from cwltool import main

import psutil
import logging
from multiprocessing import Process, Lock

import time
import logging
import logging.handlers
import subprocess

from lockfile.pidlockfile import read_pid_from_pidfile, remove_existing_pidfile

from .utils import file_read, json2file, file2json, is_json, is_yaml
from .db_command import libMaps


################################
# 定义一些辅助函数
#####################################

def get_locations(process):
    """Get logging paths"""

    pid, stdout, stderr, log, metadata = setup_locations(process)

    return  [f if os.path.exists(f) else None for f in [pid, stdout, stderr, log, metadata ] ]


def setup_locations(process, pid=None, stdout=None, stderr=None, log=None, metadata=None):
    """Creates logging paths"""

    runtimes_home = libMaps["runtimes_home"]
    if not stderr:
        stderr = os.path.join(runtimes_home, process, f'CWLJob-{process}.err')
    if not stdout:
        stdout = os.path.join(runtimes_home, process, f'CWLJob-{process}.out')
    if not log:
        log = os.path.join(runtimes_home, process, f'CWLJob-{process}.log')
    if not metadata:
        metadata = os.path.join(runtimes_home, process, f'CWLJob-{process}.metadata')
    if not pid:
        pid = os.path.join(runtimes_home, f'CWLJob-{process}.pid')
    else:
        pid = os.path.abspath(pid)

    for dirs in [stderr, stdout, metadata]:
        dir = os.path.dirname(dirs)
        if not os.path.exists(dir):
            os.makedirs(dir)

    return pid, stdout, stderr, log, metadata


def serve_logs(log_f, skip_serve_logs: bool = False):
    """Starts serve_logs """

    logs = logging.getLogger('Sixbox')
    logs.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(
        log_f,maxBytes=10000000,backupCount=5)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(u'%(asctime)s [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    logs.addHandler(fh) 
    return logs, fh



def runCWLUnit(lock, cmd, stdout, stderr, versionfunc, metadata):
    """
    cwltool main函数子进程函数
    """
    from cwltool import main
    lock.acquire()
    metadata["status"] = "running"
    metadata_writer(metadata)
    # time.sleep(1000)

    main.run(cmd, stdout=stdout, stderr=stderr, versionfunc=versionfunc)

    lock.release()


def queryJob(URI):
    """
    查询并返回APP id
    """
    with open(libMaps["job_repositories"], 'r') as f:
        jobs = json.load(f)

    try:
        querys = jobs[URI]
    except:
        querys = None
    return querys


def getJobs(URI=None):
    """
    从repositories.json中读取job信息
    """
    if URI:
        querys = queryJob(URI)
        if querys:
            pid, stdout, stderr, log, metadata_path = get_locations(querys["jobName"])
            querys.update(file2json(metadata_path))
            querys["jobLog"] = file_read(stderr)
            querys["output"] = file_read(stdout)
            return querys
        else:
            return None
    else:
        # 默认返回所有app
        with open(libMaps["job_repositories"], 'r') as f:
            apps = json.load(f)
        return apps.values()

def removeJobs(URI=None):
    """
    删除
    """
    with open(libMaps["job_repositories"], 'r') as f:
        apps = json.load(f)
 
    querys = queryJob(URI) # 先查后删除
    if querys:
        try:
            # 清理tmp临时文件与job lib记录
            shutil.rmtree(os.path.join(libMaps["runtimes_home"], URI))
            os.remove(os.path.join(libMaps["runtimes_tmp"], URI+ '.cwl'))
            os.remove(os.path.join(libMaps["runtimes_tmp"], URI+ '.yaml'))
        except:
            pass
        # 更新case_repositories
        apps = file2json(libMaps["job_repositories"])
        apps.pop(URI)
        json2file(libMaps["job_repositories"], apps)

        
        return True
    else:
        return False


def metadata_writer(metadata):
    """
    写入metadata
    """
    json2file(metadata["path"], metadata)
    
    JobManifestWriter(metadata)
    

def JobManifestWriter(payload, old_uri=None):
    """
    修改job仓库文件
    """
    colFileds = ["jobName", "status",  "created", "lastUpdated", "path"]

    # 更新case_repositories
    apps = file2json(libMaps["job_repositories"])
    if old_uri:
        apps.pop(old_uri) # 删除旧数据

    apps[payload["jobName"]] = {k:payload[k] for k in payload.keys() if k in colFileds}

    json2file(libMaps["job_repositories"], apps)


def versionstring() -> str:
    """Version of CWLtool used to execute the workflow."""
    return "{} {}".format("sixbox-engine", "1.0")


class CWLJob():
    
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '~/sixbox-job.pid'
        self.pidfile_timeout = 5

    def run(self, cmd, stdout, stderr, versionfunc, metadata):
        """
        运行 job
        """
        # 先写入初始化日志
        metadata_writer(metadata)
        
        try:
            # 执行进程
            lock = Lock()
            proc = Process(target=runCWLUnit, args=(lock, cmd, stdout, stderr, versionfunc, metadata))
            proc.start()
            proc.join()

            exitcode = proc.exitcode
        except KeyboardInterrupt:
            exitcode = -1
            # signal.signal(signal.SIGINT)

        # 更新状态
        if exitcode == 0:
            metadata['status'] = "completed"
        elif exitcode == 1:
            metadata['status'] = "failed"
        elif exitcode == None:
            metadata['status'] = "unknow"
        elif exitcode == -1:
            metadata['status'] = "killed"
        else:
            metadata['status'] = "failed"

        metadata["lastUpdated"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 更新日志
        metadata_writer(metadata)
        sys.exit()

    def test(self, ):
        f = open("/home/sixbox-linux/test1.log",'w')
        while True:
            f.write('''
                Library to implement a well-behaved Unix  process.

                ''')
            f.write("{0}\n".format(time.ctime(time.time())))
            time.sleep(1)

    def subprocess_exec(cmd, stdout=None, stderr=None, background=True, exit_on_fail: bool = True):
        
        
        subp = subprocess.Popen(main.run(cmd), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8") # 使用管道
        # subp = subprocess.Popen(cmd, shell=False, stdout=stdout, stderr=stderr, encoding="utf-8")
        if subp.poll() == 0:
            print(subp.communicate()[1])
        subp.wait()
        print('\nok\n')
        if subp.returncode != 0:
            log.error(
                "Couldn't run job! `sixbox-engine' exited with %s.\n%s\n%s",
                subp.returncode,
                "\n".join(subp.stdout.readlines() if subp.stdout else []),
                "\n".join(subp.stderr.readlines() if subp.stderr else []),
            )
            if exit_on_fail:
                sys.exit(subp.returncode)
            else:
                return subp.returncode
        if background==False:
            try:
                outs, errs = subp.communicate(timeout=15)
                output = subp.stdout.read()
                log = subp.stderr.read()
                print(log, output)
            except:
                subp.kill()
                outs, errs = subp.communicate()
        else:
            output = subp.stdout.read()
            log = subp.stderr.read()
            print(log, output)

    def inactivate_exec(self, cmd, request = None, prefix="CWLJob", name=None):
        """
        以交互进程运行CWL job
        """
        # 初始化日志
        metadata = {
            "jobName": name if name !=None else prefix,
            "status": "not-ready",
            "created": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "lastUpdated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "request": request
        }

        pid, stdout, stderr, log, metadata_path = setup_locations(
                metadata["jobName"]
            )
        metadata.update({"path" : metadata_path})
        working_directory = os.getcwd()
        _, fh = serve_logs(log)

        metadata_writer(metadata)

        # 运行并写入日志
        with open(stdout, 'w') as stdout_fn,  open(stderr, 'w') as stderr_fn:
            self.run(cmd, stdout=Logger(stdout_fn), stderr=Logger(stderr_fn), versionfunc=versionstring,metadata= metadata)

        # log_Printer(metadata["jobName"], follow=True)


    def _exec(self, cmd, request = None, prefix="CWLJob", name=None):
        """
          以守护进程运行CWL job, 只在linux下有效
        """
        import daemon
        from daemon.pidfile import TimeoutPIDLockFile

        # 初始化日志
        metadata = {
            "jobName": name if name !=None else prefix,
            "status": "not-ready",
            "created": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "lastUpdated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "request": request
        }

        pid, stdout, stderr, log, metadata_path = setup_locations(
                metadata["jobName"]
            )
        metadata.update({"path" : metadata_path})
        working_directory = os.getcwd()
        _, fh = serve_logs(log)

        # 启动守护进程
        with open(stdout, 'w+') as stdout_handle, open(stderr, 'w+') as stderr_handle:
            from cwltool import main
            ctx = daemon.DaemonContext(
                pidfile=TimeoutPIDLockFile(pid, -1),
                stdout=stdout_handle,
                stderr=stderr_handle,
                working_directory = working_directory,
                files_preserve=[fh.stream],
            )
           
            with ctx:
                # self.run(cmd, metadata)
                self.run(cmd, stdout=stdout_handle, stderr=stderr_handle, versionfunc=versionstring,metadata= metadata)
                
    def stop_worker(self, pid):
        """Sends SIGTERM to CWL worker"""
        # Read PID from file
        pid_file_path, _, _, _, metadata_path = setup_locations(process=pid)
        pid = read_pid_from_pidfile(pid_file_path)

        # Send SIGTERM
        if pid:
            worker_process = psutil.Process(pid)
            worker_process.terminate()

        # Remove pid file
        remove_existing_pidfile(pid_file_path)
        #  # 更新日志
        metadata = file2json(metadata_path)
        metadata["status"] = "cancelled"
        metadata["lastUpdated"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        metadata_writer(metadata)

    def worker_info(self, WORKER_PROCESS_NAME):
        """
        打印日志信息
        """

        pid_file_path, stdout, stderr, _, _ = get_locations(process=WORKER_PROCESS_NAME)
        # 读取日志
        if pid_file_path:
            
            pid = read_pid_from_pidfile(pid_file_path)
            worker_process = psutil.Process(pid)
            status = worker_process.status()
        elif stderr == None:
            return "job {} not found".format(WORKER_PROCESS_NAME)

        with open(stdout, encoding='utf-8') as stdout_handle, open(stderr, encoding='utf-8') as stderr_handle:
            log = stdout_handle.read() + stderr_handle.read()
            return  log

class __redirection__:
    
    def __init__(self, fileN):
        self.fileN =fileN
        self.buff=''
        self.__console__=sys.stdout
        
    def write(self, output_stream):
        self.buff+=output_stream
        self.to_file(self.fileN)

        self.to_console()

    def to_console(self):
        sys.stdout=self.__console__
        print(self.buff)
    
    def to_file(self, fileN):
        f=open(fileN,'w')
        sys.stdout=f
        print(self.buff)
        f.close()
    
    def flush(self):
        self.buff=''
        
    def reset(self):
        sys.stdout=self.__console__


class Logger(object):
    """
    自定义stdout
    """
    def __init__(self, fileN):
        self.terminal = sys.stdout
        # self.log = open(fileN,"a+")
        self.log = fileN

    def write(self, message):

        self.log.write(message)
        self.terminal.write(message)
        
    def read(self):
        return self.messages


    def flush(self):
        pass
 

def build_request(app, input):
    """
    依据给定的app，input 文件构建job request
    """
    app = eval(repr(app))
    input = eval(repr(input))
    if is_json(app):
        app_payload = json.loads(app)
    elif is_yaml(app):
        app_payload = yaml.load(app, Loader=yaml.FullLoader)
    else:
        app_payload = app

    if is_json(input):
        input_payload = json.loads(input)
    elif is_yaml(input):
        input_payload = yaml.load(input, Loader=yaml.FullLoader)
    else:
        input_payload = input
    
    return {
        "app": app_payload,
        "input": input_payload
    }


def log_Printer(jobName,  follow=False):
    """
    实时打印日志
    """

    
    pid, stdout, stderr, log, metadata_path = get_locations(jobName)
    with open(stderr, mode='r', encoding='utf8') as f1, open(stdout, mode='r', encoding='utf8') as f2:
        try:
            if follow:
                read_line(f1, follow=True)
                # read_line(f2, follow=True)
            else: # 一次读取
                for line in f1.readlines():
                    print(line.strip())
                for line in f2.readlines():
                    print(line.strip())
        except KeyboardInterrupt:
            pass

def read_line(fn, follow=False):
    """
    
    """
    count = 0
    position = 0
    if follow: # 实时读取
        while True:
            line = fn.readline().strip()
            if line:
                count += 1
                print(" %s" % ( line))

            cur_position = fn.tell() # 记录上次读取文件的位置

            if cur_position == position:
                time.sleep(0.01)
                continue
            else:
                position = cur_position
                time.sleep(0.01)


