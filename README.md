# Django AWS S3 File Manager (django-s3files)

## Description

Django AWS S3 File Manager enables you to manage files directly from the Django admin interface, allowing you to read,
upload, and delete files without directly accessing AWS.  
It seamlessly integrates with [django-storages](https://github.com/jschneier/django-storages.git).

## Installation

Installing from PyPI is as easy as doing:
```bash
pip install django-s3files
```

## Settings
1. Add `django-s3files` to your `INSTALLED_APPS` in `settings.py`.

2. Add include url above your admin url.
    ```python
    urlpatterns = [
        path('admin/s3files/', include('s3files.urls')),
        path('admin/', admin.site.urls),
    ]
    ```

## Authentication Settings
- `AWS_ACCESS_KEY_ID` (required)
- `AWS_SECRET_ACCESS_KEY` (required)
- `AWS_S3_REGION_NAME` (required)
- `AWS_STORAGE_BUCKET_NAME` (required)
- `AWS_STORAGE_BASE_DIR` (default: '/')

## Dependencies

The package works with any version of Python 3, tested with Django==4.2, and requires boto3==1.37.38.
Other versions have not been tested.

## Features
- Highlight key features of the application.
- Example: User authentication, API integrations, or other specific functionalities.

## Contributing

1. Check for open issues at [the project issue page](https://github.com/runbykim/django-s3files/issues) or open a new issue 
to start a discussion about a feature or bug.
2. Fork the [django-storages repository on GitHub](https://github.com/runbykim/django-s3files.git) to start making changes.
3. Make sure the bug is fixed or the feature is implemented correctly.
4. Wait for me to merge the pull request.
