
from .commands import queryJob, CWLJob



"""
This file contains the code that can be used to remove the CWL from CWLdb
"""



def stop_job(args, version):
    """
    stop job
    """
    for jobName in args.jobName:
        
        query = queryJob(jobName)
        if query: # 如果存在
            if query["status"] == "running" or query["status"] == "not-ready":
                job = CWLJob()
                job.stop_worker(jobName)
                print("INFO: Job {} is stopped successfully!".format(jobName))
            else:
                print("INFO: Job {} is not running!".format(jobName))
            
        else:
            print('WARN: unable to find Job {} !'.format(jobName))

