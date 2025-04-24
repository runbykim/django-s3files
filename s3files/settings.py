from django.conf import settings

# Define your default settings
DEFAULTS = {
    'AWS_ACCESS_KEY_ID': None,
    'AWS_SECRET_ACCESS_KEY': None,
    'AWS_S3_REGION_NAME': None,
    'AWS_STORAGE_BUCKET_NAME': None,
    'AWS_STORAGE_BASE_DIR': '',
    'PER_PAGE': 25,
    'SHOW_THUMBNAILS': False
}


# Function to get settings with defaults
def get_setting(setting_name):
    """
    Get a setting value from Django settings, or raise an error if not provided.
    """
    value = getattr(settings, setting_name, DEFAULTS[setting_name])
    if value is None:
        raise ValueError(f"Missing required setting: {setting_name}")
    return value


# Create properties for easy access to settings
AWS_ACCESS_KEY_ID = get_setting('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_setting('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = get_setting('AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = get_setting('AWS_STORAGE_BUCKET_NAME')
AWS_STORAGE_BASE_DIR = get_setting('AWS_STORAGE_BASE_DIR')
PER_PAGE = get_setting('PER_PAGE')
SHOW_THUMBNAILS = get_setting('SHOW_THUMBNAILS')