import setuptools
from setuptools import setup, find_packages

setup(
    name             = 'django-s3files',
    version          = '0.0.3',
    description      = 'Django AWS S3 File Manager enables you to manage files directly from the Django admin '
                       'interface, allowing you to read, upload, and delete files without directly accessing AWS.',
    author           = 'RunByKim',
    author_email     = 'runbykim@gmail.com',
    url              = 'https://github.com/runbykim/django-s3files.git',
    download_url     = 'https://github.com/runbykim/django-s3files.git',
    install_requires = ['boto3>=1.37.38'],
	include_package_data=True,
	packages         = find_packages(include=['s3files', 's3files.*']),
    package_data     = {'s3files': ['templates/*.html']},
    keywords         = ['django', 'aws', 's3', 'media', 'file', 'manager', 'django-storage'],
    python_requires  = '>=3',
    zip_safe         = False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)