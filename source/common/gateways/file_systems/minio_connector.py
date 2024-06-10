from minio import Minio

from source.common.gateways.file_systems.base import FileSystemInterface


class MinIOConnector(FileSystemInterface):
    def __init__(self): #TODO config class
        self.client = Minio(
            access_key="admin",
            secret_key="admin_admin",
            endpoint="localhost:9000",
            secure=False
        )

        print(self.client .list_buckets())

