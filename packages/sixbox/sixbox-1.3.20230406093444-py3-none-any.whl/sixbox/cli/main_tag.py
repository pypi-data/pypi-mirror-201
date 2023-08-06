

from .commands import modifyApps, modifyCases, ValidateTag, ValidateCaseTag, modifyDatasets
import sys


"""
This file contains the code that can be used to modify the cwl tag information
"""



def tag_app(args, version):
    """
    change tag for App
    """
    raw_tag_ID = args.raw_tag_ID
    new_tag = args.new_tag
    if not ValidateTag(new_tag):
        print("""WARN: your tag format is INCORRECT.The tag format must be $(provider)/$(CWLname):$(version).
            See Sixoclock Help document for for details on all the command.""")
        sys.exit()

    payload ={
        "provider": new_tag.split('/')[0],
        "name": new_tag.split('/')[1].split(":")[0],
        "version": new_tag.split('/')[1].split(":")[1]
    }
    if modifyApps(raw_tag_ID, payload):
        print("INFO: tag is modified successfully!")
    else:
        print('WARN: unable to find CWL  {} !'.format(raw_tag_ID))

def tag_case(args, version):
    """
    change tag for case
    """
    raw_tag_ID = args.raw_tag_ID
    new_tag = args.new_tag
    if not ValidateCaseTag(new_tag):
        print("""WARN: your tag format is INCORRECT.The tag format must be $(provider)/$(CWLname).
            See Sixoclock Help document for for details on all the command.""")
        sys.exit()

    payload ={
        "provider": new_tag.split('/')[0],
        "name": new_tag.split('/')[1].split(":")[0],
        "version": new_tag.split('/')[1].split(":")[1]
    }
    if modifyCases(raw_tag_ID, payload):
        print("INFO: tag is modified successfully!")
    else:
        print('WARN: unable to find CWL  {} !'.format(raw_tag_ID))

def tag_dataset(args, version):
    """
    change tag for dataset
    """
    raw_tag_ID = args.raw_tag_ID
    new_tag = args.new_tag
    if not ValidateCaseTag(new_tag):
        print("""WARN: your tag format is INCORRECT.The tag format must be $(provider)/$(CWLname).
            See Sixoclock Help document for for details on all the command.""")
        sys.exit()

    payload ={
        "provider": new_tag.split('/')[0],
        "name": new_tag.split('/')[1].split(":")[0],
        "version": new_tag.split('/')[1].split(":")[1]
    }
    if modifyDatasets(raw_tag_ID, payload):
        print("INFO: tag is modified successfully!")
    else:
        print('WARN: unable to find dataset  {} !'.format(raw_tag_ID))