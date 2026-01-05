"""Settings for storage backends."""
import os
import sys

STORAGES = {
    "default": {
        # Use S3Storage only if not running in GitHub Actions (CI) or pytest
        "BACKEND": (
            "storages.backends.s3.S3Storage"
            if not (os.getenv("GITHUB_ACTIONS") == "true" or "pytest" in sys.modules or "test" in sys.argv)
            else "django.core.files.storage.FileSystemStorage"
        ),
        "OPTIONS": (
            {
                "access_key": os.getenv("S3_ACCESS_KEY"),
                "secret_key": os.getenv("S3_SECRET_KEY"),
                "bucket_name": os.getenv("S3_BUCKET_NAME"),
                "endpoint_url": os.getenv("S3_ENDPOINT_URL"),
                "addressing_style": "path",
                "use_ssl": True,
                "default_acl": None,
                "signature_version": "s3v4",
            }
            if not (os.getenv("GITHUB_ACTIONS") == "true" or "pytest" in sys.modules or "test" in sys.argv)
            else {}
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
