"""
sixbox.backend.python
~~~~~~~~~~~~~~~~~~~
:copyright: 2020 Seven Bridges Genomics Inc.
:license: Apache 2.0
"""
import ssl
import logging

# Read and set version globally
# needs to be imported before other modules
from sixbox.backend.version import __version__

from sixbox.backend.api import Api
from sixbox.backend.config import Config

from sixbox.backend.models.invoice import Invoice
from sixbox.backend.models.billing_group import (
    BillingGroup, BillingGroupBreakdown
)
from sixbox.backend.models.user import User
from sixbox.backend.models.endpoints import Endpoints
from sixbox.backend.models.project import Project
from sixbox.backend.models.task import Task
from sixbox.backend.models.app import App
from sixbox.backend.models.dataset import Dataset
from sixbox.backend.models.bulk import BulkRecord
from sixbox.backend.models.team import Team, TeamMember
from sixbox.backend.models.member import Member, Permissions
from sixbox.backend.models.file import File
from sixbox.backend.models.storage_export import Export
from sixbox.backend.models.storage_import import Import
from sixbox.backend.models.volume import Volume
from sixbox.backend.models.marker import Marker
from sixbox.backend.models.division import Division
from sixbox.backend.models.automation import (
    Automation, AutomationRun, AutomationPackage, AutomationMember
)
from sixbox.backend.models.async_jobs import AsyncJob
from sixbox.backend.models.compound.volumes.volume_object import VolumeObject

from sixbox.backend.models.enums import (
    AppCopyStrategy, AppRawFormat, AsyncFileOperations, AsyncJobStates,
    AutomationRunActions, DivisionRole, FileStorageType, ImportExportState,
    TaskStatus, TransferState, VolumeAccessMode, VolumeType, PartSize,
    AutomationStatus,
)
from sixbox.backend.errors import (
    SbgError, ResourceNotModified, ReadOnlyPropertyError, ValidationError,
    TaskValidationError, PaginationError, BadRequest, Unauthorized, Forbidden,
    NotFound, Conflict, TooManyRequests, ServerError, ServiceUnavailable,
    MethodNotAllowed, RequestTimeout, LocalFileAlreadyExists,
    ExecutionDetailsInvalidTaskType
)
# from sixbox.backend.main import(
#     install_packages, main_commit, main_config, main_cwls, main_install, 
#     main_pull, main_remove, main_run, main_search, main_update, sixbox_parsers,
#     version
# )

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    # Models
    'Api', 'AsyncJob', 'Automation', 'AutomationRun', 'AutomationMember',
    'AutomationPackage',  'Config', 'Invoice', 'BillingGroup',
    'BillingGroupBreakdown', 'User', 'Endpoints', 'Project', 'Task', 'App',
    'Member', 'Permissions', 'File', 'Export', 'Import', 'Volume',
    'VolumeObject', 'Marker', 'Division', 'Team', 'TeamMember', 'Dataset',
    'BulkRecord',
    # Enums
    'AppCopyStrategy', 'AppRawFormat', 'AppCopyStrategy',
    'AsyncFileOperations', 'AsyncJobStates', 'AutomationRunActions',
    'DivisionRole', 'FileStorageType', 'ImportExportState', 'TaskStatus',
    'TransferState', 'VolumeAccessMode', 'VolumeType', 'PartSize',
    'AutomationStatus',
    # Errors
    'SbgError', 'ResourceNotModified', 'ReadOnlyPropertyError',
    'ValidationError', 'TaskValidationError', 'PaginationError', 'BadRequest',
    'Unauthorized', 'Forbidden', 'NotFound', 'Conflict', 'TooManyRequests',
    'ServerError', 'ServiceUnavailable', 'MethodNotAllowed', 'RequestTimeout',
    'LocalFileAlreadyExists', 'ExecutionDetailsInvalidTaskType',
    # Version
    '__version__',
    # main
    'install_packages', 'main_commit', 'main_config', 'main_cwls', 'main_install', 
    'main_pull', 'main_remove', 'main_run', 'main_search', 'main_update', 'sixbox_parsers',
    'version',
]

required_ssl_version = (1, 0, 1)
if ssl.OPENSSL_VERSION_INFO < required_ssl_version:
    raise SbgError(
        'OpenSSL version included in this python version must be '
        'at least 1.0.1 or greater. Please update your environment build.'
    )
