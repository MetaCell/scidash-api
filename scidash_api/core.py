from __future__ import unicode_literals, print_function
import json

import requests


class ScidashApiUploader(object):

    """
    Main uploader class which is used by CLI script and API function
    """

    def __init__(self, server_url, upload_endpoint_url, filename):
        """
        :server_url: Root Scidash server URL
        :upload_endpoint_url: Endpoint of upload method

        """
        self._server_url = server_url
        self._upload_endpoint_url = upload_endpoint_url
        self._filename = filename

    def _upload(self, data):
        files = {
                'file': ('data.json', data)
                }

        full_url = '{0}{1}'.format(self._server_url,
                self._upload_endpoint_url)

        full_url = full_url.format(filename=self._filename)

        return requests.post(full_url, files=files)

    def upload_json(self, data):
        """
        Upload method for JSON

        :param data: JSON string
        """
        self._upload(data)

    def upload_object(self, _object):
        """
        :param _object: Serializable object
        """
        serialized_object = json.dumps(_object)

        self._upload(serialized_object)
