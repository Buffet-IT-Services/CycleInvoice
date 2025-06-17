"""Settings for storage backends."""
import os
import sys

STORAGES = {
    "default": {
        # Use S3Storage only if not running in GitHub Actions (CI) or pytest
        "BACKEND": (
            "storages.backends.s3.S3Storage"
            if not (os.getenv("GITHUB_ACTIONS") == "true" or "pytest" in sys.modules)
            else "django.core.files.storage.FileSystemStorage"
        ),
        "OPTIONS": (
            {
                "access_key": os.getenv("S3_ACCESS_KEY"),
                "secret_key": os.getenv("S3_SECRET_KEY"),
                "bucket_name": "cycleinvoice",
                "endpoint_url": "https://minio.buffetitcloud.ch",
                "addressing_style": "path",
                "use_ssl": True,
                "default_acl": None,
                "signature_version": "s3v4",
            }
            if not (os.getenv("GITHUB_ACTIONS") == "true" or "pytest" in sys.modules)
            else {}
        ),
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
