from .install_packages import install_packages

def update(args,version):
    """
    Updates sixbox package to the latest compatible version
    """
    install_packages(args, command='update')
