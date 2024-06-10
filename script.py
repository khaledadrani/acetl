# Example usage:
from minio import Minio

from source.common.gateways.file_systems.base import LocalFileSystem

local_fs = LocalFileSystem("D:\\Books\\")

# MINIO_ACCESS_KEY: 12345678
# MINIO_SECRET_KEY: password

client = Minio(
    access_key="admin",
    secret_key="admin_admin",
    endpoint="localhost:9000",
    secure=False
)

print(client.list_buckets())

first_file_path = list(local_fs.get_list(pattern="*numpy*"))[0]

# The file to upload, change this path if needed
source_file = first_file_path

bucket_name = "test-bucket"
destination_file = "my-test-file.pdf"

# Make the bucket if it doesn't exist.
found = client.bucket_exists(bucket_name)
if not found:
    client.make_bucket(bucket_name)
    print("Created bucket", bucket_name)
else:
    print("Bucket", bucket_name, "already exists")
