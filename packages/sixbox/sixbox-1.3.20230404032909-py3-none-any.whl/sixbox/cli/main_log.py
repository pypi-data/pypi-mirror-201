
from .commands import queryJob, getJobs, log_Printer



"""
打印CWL job 日志
"""



def log_job(args, version):
    """
    print logs of job 
    """
    jobName = args.jobName
    follow = args.follow
    query = queryJob(jobName)
    if query: # 如果存在
        log_Printer(query["jobName"], follow)
       
    else:
        print('WARN: unable to find Job {} !'.format(jobName))
