
from minio import Minio
from minio.error import S3Error
import os

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False,
)

BUCKET = os.getenv("MINIO_BUCKET", "ztb")

def ensure_bucket() -> None:
    """Create bucket if not exists."""
    try:
        if not client.bucket_exists(BUCKET):
            client.make_bucket(BUCKET)
    except S3Error:
        # If a race condition occurs, ignore bucket already exists errors.
        pass
