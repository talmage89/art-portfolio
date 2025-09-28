from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting


class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    bucket_name = setting("GS_BUCKET_NAME")
    file_overwrite = False
    max_memory_size = 1024 * 1024 * 10  # 10MB
    default_acl = None
    querystring_auth = False
