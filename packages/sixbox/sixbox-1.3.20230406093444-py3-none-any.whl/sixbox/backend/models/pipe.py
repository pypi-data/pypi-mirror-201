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


class App(Resource):
    """
    Central resource for managing apps.
    """
    _URL = {
        'query': '/v1/search/pipe',
        'search': '/v1/search/pipe?term={term}&page={page}&size={size}',
        'get': '/pipe/{id}',
        'get_pipe': '/v2/pipe/{id}',
        'create_pipe': '/v2/pipe',
        'get_revision': '/v2/pipe/repository/{id}/revision/{revision}',
        'update_revision': '/v2/pipe/repository/{id}/revision/{revision}',
        'create_revision': '/v2/pipe/repository/{id}/{revision}',
        'pull': '/v2/pipe/repository/{id}/pulls',
        'copy': '/apps/{id}/actions/copy',
        'sync': '/apps/{id}/actions/sync',
        'raw': '/apps/{id}/raw'
    }

    _CONTENT_TYPE = {
        AppRawFormat.JSON: 'application/json',
        AppRawFormat.YAML: 'application/yaml'
    }

    name = StringField(read_only=True)

    # href = HrefField(read_only=True)
    pipe_id = StringField(read_only=True)
    resource_id = StringField(read_only=True, name='resource_id')
    profile = StringField(read_only=True)
    content = StringField(read_only=True)
    type = IntegerField(read_only=True)
    version = StringField(read_only=True)
    updated_at = StringField(read_only=True)
    provider = StringField(read_only=True)
    description = StringField(read_only=True)
    # raw = DictField(read_only=False)

    # @property
    # def id(self):
    #     _id, _rev = self._id.rsplit('/', 1)
    #     if re.match(r'^\d*$', _rev):
    #         return _id
    #     else:
    #         return self._id

    # def __eq__(self, other):
    #     if type(other) is not type(self):
    #         return False
    #     return self is other or self.id == other.id

    # def __str__(self):
    #     revision = self.field('revision')
    #     if revision:
    #         return f'<App: id={self.id} rev={self.revision}>'
    #     return f'<App: id={self.id}'
    @property
    def _meta(self):
        meta_cols = ["resource_id","name","provider", "version", "type", "updated_at", "description"]
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
        return super()._query(url=cls._URL['query'],
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
    def get_revision(cls, id, revision, api=None):
        """
        Get app revision.
        :param id: App identifier.
        :param revision: App revision
        :param api: Api instance.
        :return: App object.
        """
        api = api if api else cls._API
        extra = {'resource': cls.__name__, 'query': {
            'id': id,
            'revision': revision
        }}
        logger.info('Get revision', extra=extra)
        app = api.get(url=cls._URL['get_revision'].format(
            id=id, revision=revision)).json()
        return App(api=api, **app)
    
    @classmethod
    def pull(cls, id, api=None):
        """
        Get app revision.
        :param id: App identifier.
        :param revision: App revision
        :param api: Api instance.
        :return: App object.
        """
        api = api if api else cls._API
        extra = {'resource': cls.__name__, 'query': {
            'id': id,
        }}
        logger.info('pull ', extra=extra)
        app = api.post(url=cls._URL['pull'].format(
            id=id))
        return App(api=api)
    @classmethod
    def create_revision(cls, id, revision, raw, api=None):
        """
        Create a new app revision.
        :param id:  App identifier.
        :param revision: App revision.
        :param raw: Raw cwl object.
        :param api: Api instance.
        :return: App object.
        """

        api = api if api else cls._API
        extra = {'resource': cls.__name__, 'query': {
            'id': id,
            'data': raw
        }}
        logger.info('Creating app revision', extra=extra)
        app = api.post(url=cls._URL['create_revision'].format(
            id=id, revision=revision), data=raw).json()
        app_wrapper = api.get(
            url=cls._URL['get'].format(id=app['sbg:id'])).json()
        return App(api=api, **app_wrapper)

    @classmethod
    def update_revision(cls, id, revision, raw, api=None):
        """
        Get app revision.
        :param id: App identifier.
        :param revision: App revision
        :param api: Api instance.
        :return: App object.
        """
        api = api if api else cls._API
        extra = {'resource': cls.__name__, 'query': {
            'id': id,
            'revision': revision
        }}
       
        logger.info('update revision', extra=extra)
        app = api.put(url=cls._URL['update_revision'].format(
            id=id, revision=revision), data=raw).json()
        app_wrapper = api.get(
            url=cls._URL['get_pipe'].format(id=app['data']["id"])).json()
        return App(api=api, **app_wrapper)

    @classmethod
    def get_pipe(cls, id, api=None):
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
        app = api.get(url=cls._URL['get_pipe'].format(
            id=id)).json()
        return App(api=api, **app)


    @classmethod
    def create_pipe(cls, raw, api=None):
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
        logger.info('Creating app', extra=extra)
        app = api.post(url=cls._URL['create_pipe'], data=raw).json()
        app_wrapper = api.get(
            url=cls._URL['get_pipe'].format(id=app['data']["id"])).json()
      
        return App(api=api, **app_wrapper)


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
        return App(api=api, **app)

    def sync(self):
        """
        Syncs the parent app changes with the current app instance.
        :return: Synced App object.
        """
        app = self._api.post(url=self._URL['sync'].format(id=self.id)).json()
        return App(api=self._api, **app)
