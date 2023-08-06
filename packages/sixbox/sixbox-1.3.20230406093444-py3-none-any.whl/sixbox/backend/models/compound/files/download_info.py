from sixbox.backend.meta.resource import Resource
from sixbox.backend.meta.fields import HrefField


class DownloadInfo(Resource):
    """
    Download info resource contains download url for the file.
    """
    url = HrefField(read_only=True)

    def __str__(self):
        return f'<DownloadInfo: url={self.url}>'
