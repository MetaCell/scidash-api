from scidash_api.core import ScidashApiUploader
import scidash_api.settings as settings

uploader = ScidashApiUploader(server_url=settings.SCIDASH_SERVER_URL,
        upload_endpoint_url=settings.UPLOAD_URL, filename=settings.FILE_NAME)

print(uploader.upload_json('{ \
        "id": 1 \
}'))
