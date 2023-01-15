import os
from prefect.filesystems import RemoteFileSystem

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')

if S3_ENDPOINT_URL is None or MINIO_ACCESS_KEY is None or MINIO_SECRET_KEY is None or MINIO_BUCKET_NAME is None:
    print("failed to read environment variables")
    exit(1)

if os.path.exists("/root/.prefect/block_configured.lock"):
    exit(0)
else:
    with open("/root/.prefect/block_configured.lock", "w") as f:
        f.write("1")

minio_block = RemoteFileSystem(
    basepath="s3://{}".format(MINIO_BUCKET_NAME),
    settings={
        "key": MINIO_ACCESS_KEY,
        "secret": MINIO_SECRET_KEY,
        "client_kwargs": {"endpoint_url": S3_ENDPOINT_URL},
    },
)
minio_block.save("minio", overwrite=True)
print("Block storage set.")
