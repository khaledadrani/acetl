import io

from minio import Minio, S3Error

from source.common.gateways.file_systems.base import FileSystemInterface


class MinioFileSystem(FileSystemInterface):
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
        self.bucket_name = bucket_name
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def store(self, key, data, content_type: str = 'application/octet-stream'):
        if isinstance(data, str):
            data = io.BytesIO(data.encode())
        elif isinstance(data, bytes):
            data = io.BytesIO(data)
        self.client.put_object(self.bucket_name, key, data, len(data.getvalue()), content_type=content_type)

    def get(self, key, mode: str = 'rb'):
        try:
            response = self.client.get_object(self.bucket_name, key)
            return response.read()
        except S3Error as e:
            if e.code == 'NoSuchKey':
                return None
            else:
                raise

    def get_list(self, prefix: str = '', recursive: bool = False) -> Generator[str, None, None]:
        objects = self.client.list_objects(self.bucket_name, prefix=prefix, recursive=recursive)
        for obj in objects:
            yield obj.object_name
