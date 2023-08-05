
from .install_packages import install_packages


def install(args,version):
    """
    Installs sixbox package
    """
    install_packages(args, command='install')
