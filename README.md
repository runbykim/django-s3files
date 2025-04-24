# Django AWS S3 File Manager (django-s3files)

## Description

Django AWS S3 File Manager enables you to manage files directly from the Django admin interface, allowing you to read,
upload, and delete files without directly accessing AWS.  
It seamlessly integrates with [django-storages](https://github.com/jschneier/django-storages.git).

**Documents**
- PyPI https://pypi.org/project/django-s3files/
- Github https://github.com/runbykim/django-s3files

## Installation

Installing from PyPI is as easy as doing:
```bash
pip install django-s3files
```

## Settings
1. Add `django-s3files` to your `INSTALLED_APPS` in `settings.py`.

2. Add include url above your admin url. You can change the url as you wish.
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
- `AWS_STORAGE_BASE_DIR` (str: '')
- `PER_PAGE` (int: 25)
- `SHOW_THUMBNAILS` (bool: False)

## URL

Your file manager URL will be the `include` URL defined in step 2 of the settings, followed by `/browse`.  
For example: `https://example.com/admin/s3files/browse`.

## Dependencies

The package works with any version of Python 3, tested with Django==4.2, and requires boto3==1.37.38.
Other versions have not been tested.

## Contributing

1. Check for open issues at [the project issue page](https://github.com/runbykim/django-s3files/issues) or open a new issue 
to start a discussion about a feature or bug.
2. Fork the [django-storages repository on GitHub](https://github.com/runbykim/django-s3files.git) to start making changes.
3. Make sure the bug is fixed or the feature is implemented correctly.
4. Wait for me to merge the pull request.
