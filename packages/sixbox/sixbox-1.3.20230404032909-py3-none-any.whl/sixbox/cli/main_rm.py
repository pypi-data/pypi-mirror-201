
from .commands import (queryApp, removeApps, removeCases, queryCase, queryJob, 
                            CWLJob, removeJobs, log, queryDatasets,removeDatasets)
import sys


"""
This file contains the code that can be used to remove the CWL from CWLdb
"""


def rm_app(args, version):
    """
    remove CWL from CWLdb
    """
    for tag_ID in args.tag_ID:

        query = queryApp(tag_ID)
        if query: # 如果存在
            removeApps(tag_ID)
            log.info("App {} is removed successfully!".format(tag_ID))
        else:
            log.warning('Unable to find CWL App {} !'.format(tag_ID))

def rm_case(args, version):
    """
    remove case from db
    """
    for tag_ID in args.tag_ID:

        query = queryCase(tag_ID)
        if query: # 如果存在
            removeCases(tag_ID)
            log.info("Case {} is removed successfully!".format(tag_ID))
        else:
            log.warning('Unable to find case {} !'.format(tag_ID))

def rm_job(args, version):
    """
    remove job from db
    """
    

    for jobName in args.jobName:
        query = queryJob(jobName)
        if query: # 如果存在
            if query["status"] == "running" or query["status"] == "not-ready":
                if args.force: # 强制删除
                    job = CWLJob()
                    job.stop_worker(jobName)
                else:
                    log.warning('Unable to delete job {}, job is running !'.format(jobName))
                    sys.exit()
            removeJobs(jobName)
            log.info("Job {} is removed successfully!".format(jobName))
        else:
            log.warning('Unable to find job {} !'.format(jobName))

def rm_dataset(args, version):
    """
    remove dataset from db
    """
    

    for tag_ID in args.tag_ID:

        query = queryDatasets(tag_ID)
        if query: # 如果存在
            removeDatasets(tag_ID)
            log.info("Dataset {} is removed successfully!".format(tag_ID))
        else:
            log.warning('Unable to find dataset {} !'.format(tag_ID))