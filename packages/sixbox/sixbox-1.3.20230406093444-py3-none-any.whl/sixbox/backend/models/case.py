import logging
import re

from sixbox.backend.meta.fields import (
    DictField,
    HrefField,
    StringField,
    IntegerField,
)
from sixbox.backend.errors import SbgError
from sixbox.backend.meta.resource import Resource
from sixbox.backend.meta.transformer import Transform
from sixbox.backend.models.enums import AppRawFormat, AppCopyStrategy

logger = logging.getLogger(__name__)


class Case(Resource):
    """
    Central resource for managing apps.
    """
    _URL = {
        'query': '/v1/cases',
        'search': '/v1/search/case?term={term}&page={page}&size={size}',
        'get': '/v1/case/{id}',
        'create': '/v1/case',
        'update': '/v1/case/{id}',
        'delete': '/v1/case/{id}',
        'copy': '/apps/{id}/actions/copy',
        'sync': '/apps/{id}/actions/sync',
    }

    _CONTENT_TYPE = {
        AppRawFormat.JSON: 'application/json',
        AppRawFormat.YAML: 'application/yaml'
    }

    name = StringField(read_only=True)

    resource_id = StringField(read_only=True, name='resource_id')
   
    type = IntegerField(read_only=True)
    updated_at = StringField(read_only=True)
    provider = StringField(read_only=True)
    description = StringField(read_only=True)
    instruction = StringField(read_only=True)
    readme = StringField(read_only=True)
    content = StringField(read_only=True)


    @property
    def _meta(self):
        meta_cols = ["resource_id","name","provider", "type", "updated_at", "description"]
        return {
            i: getattr(self, i) 
            for i in meta_cols 
        }
    @classmethod
    def query(cls, project=None, visibility=None, q=None, id=None, offset=None,
              limit=None, api=None):
        """
        Query (List) apps.
        :param project: Source project.
        :param visibility: private|public for private or public apps.
        :param q: List containing search terms.
        :param id: List contains app ids. Fetch apps with specific ids.
        :param offset: Pagination offset.
        :param limit: Pagination limit.
        :param api: Api instance.
        :return: collection object
        """
        if project:
            project = Transform.to_project(project)
        api = api or cls._API
        return super()._query(url=cls._URL['query'], project=project,
                              visibility=visibility, q=q, id=id,
                              offset=offset, limit=limit, api=api)
    @classmethod
    def search(cls, term, page=1, size=50, api=None):
        """
        Get app revision.
        :param id: App identifier.
        :param revision: App revision
        :param api: Api instance.
        :return: App object.
        """
        api = api if api else cls._API
        extra = {'resource': cls.__name__, 'query': {
            'term': term
        }}
        logger.info('Get apps', extra=extra)
        app = api.get(url=cls._URL['search'].format(
            term=term, page=page, size=size )).json()
        
        return app


    @classmethod
    def get_case(cls, id, api=None):
        """
        Get app revision.
        :param id: App identifier.
        :param revision: App revision
        :param api: Api instance.
        :return: App object.
        """
        api = api if api else cls._API
        extra = {'resource': cls.__name__, 'query': {
            'id': id
        }}
        logger.info('Get pipe', extra=extra)
        app = api.get(url=cls._URL['get'].format(
            id=id)).json()
        return Case(api=api, **app)


    @classmethod
    def create_case(cls, raw, api=None):
        """
        Create a new app.
        :param raw: Raw cwl object.
        :param api: Api instance.
        :return: App object.
        """

        api = api if api else cls._API
        extra = {'resource': cls.__name__, 'query': {
            'data': raw["name"]
        }}
        logger.info('Creating case', extra=extra)
        app = api.post(url=cls._URL['create'], data=raw).json()
        app_wrapper = api.get(
            url=cls._URL['get'].format(id=app['data']["id"])).json()
      
        return Case(api=api, **app_wrapper)

    @classmethod
    def update_case(cls, id, raw, api=None):
        """
        修改case.
        :param id: App identifier.
        :param revision: App revision
        :param api: Api instance.
        :return: App object.
        """
        api = api if api else cls._API
        extra = {'resource': cls.__name__, 'query': {
            'id': id
        }}
        logger.info('update case', extra=extra)
        app = api.put(url=cls._URL['update'].format(
            id=id), data=raw).json()
        return Case(api=api, **app)

    def copy(self, project, name=None, strategy=None, use_revision=False,
             api=None):
        """
        Copies the current app.
        :param project: Destination project.
        :param name: Destination app name.
        :param strategy: App copy strategy.
        :param use_revision: Copy from set app revision.
        :param api: Api instance.
        :return: Copied App object.

        :Copy strategies:
        clone         copy all revisions and continue getting updates form the
                      original app (default method when the key is omitted)

        direct        copy only the latest revision and get the updates from
                      this point on

        clone_direct  copy the app like the direct strategy, but keep all
                      revisions

        transient     copy only the latest revision and continue getting
                      updates from the original app
        """
        api = api or self._API
        app_id = self._id if use_revision else self.id
        strategy = strategy or AppCopyStrategy.CLONE

        project = Transform.to_project(project)
        data = {
            'project': project,
            'strategy': strategy
        }
        if name:
            data['name'] = name
        extra = {
            'resource': type(self).__name__,
            'query': {
                'id': app_id,
                'data': data
            }
        }
        logger.info('Copying app', extra=extra)
        app = api.post(
            url=self._URL['copy'].format(id=app_id), data=data
        ).json()
        return Case(api=api, **app)

    def sync(self):
        """
        Syncs the parent app changes with the current app instance.
        :return: Synced App object.
        """
        app = self._api.post(url=self._URL['sync'].format(id=self.id)).json()
        return Case(api=self._api, **app)
