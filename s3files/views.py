# @login_required
from urllib.parse import quote, unquote

from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.views.main import PAGE_VAR, ALL_VAR
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from .settings import AWS_STORAGE_BASE_DIR, PER_PAGE, SHOW_THUMBNAILS
from .utils import get_s3_client


@csrf_protect
@staff_member_required
def list_s3_files(request):
    s3_client = get_s3_client()
    base_prefix = AWS_STORAGE_BASE_DIR

    # Get current directory from query parameter or use base prefix
    current_path = unquote(request.GET.get('path', base_prefix))
    if current_path and not current_path.endswith('/'):
        current_path += '/'

    # Ensure we don't go above base directory
    if not current_path.startswith(base_prefix):
        current_path = base_prefix

    # Get search query
    search_query = request.GET.get('search', '').lower()

    # Handle file upload
    if request.method == 'POST' and 'upload' in request.FILES:
        file = request.FILES['upload']
        try:
            key = f"{current_path}{file.name}"
            s3_client.upload_fileobj(
                file,
                settings.AWS_STORAGE_BUCKET_NAME,
                key,
                ExtraArgs={'ContentType': file.content_type}
            )
            messages.success(request, f'Successfully uploaded {file.name}')
            return redirect(f'?path={quote(current_path)}')
        except ClientError as e:
            messages.error(request, f'Error uploading file: {str(e)}')

    files = []
    directories = []

    try:
        # List all objects with the current prefix
        s3paginator = s3_client.get_paginator('list_objects_v2')
        s3page_iterator = s3paginator.paginate(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Prefix=current_path,
            Delimiter='/'
        )

        for s3page in s3page_iterator:
            # Handle directories
            if 'CommonPrefixes' in s3page:
                for prefix in s3page['CommonPrefixes']:
                    dir_path = prefix['Prefix']
                    dir_name = dir_path[len(current_path):-1]  # Remove current path prefix and trailing slash
                    if not search_query or search_query in dir_name.lower():
                        directories.append({
                            'name': dir_name,
                            'path': dir_path,
                            'type': 'directory'
                        })

            # Handle files
            if 'Contents' in s3page:
                for item in s3page['Contents']:
                    # print_debug(item)
                    file_path = item['Key']
                    # Skip if it's the current directory marker
                    if file_path == current_path:
                        continue

                    file_name = file_path[len(current_path):]
                    # Skip if it's not in current directory (prevents listing nested files)
                    if '/' in file_name:
                        continue

                    file_type = (
                        'image' if file_name.split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'] else
                        'document' if file_name.split('.')[-1].lower() in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt',
                                                                           'pptx', 'txt'] else
                        'audio' if file_name.split('.')[-1].lower() in ['mp3', 'wav', 'aac', 'flac', 'ogg'] else
                        'video' if file_name.split('.')[-1].lower() in ['mp4', 'mkv', 'avi', 'mov', 'wmv'] else
                        'archive' if file_name.split('.')[-1].lower() in ['zip', 'rar', 'tar', 'gz', '7z'] else
                        'file'
                    )

                    if not search_query or search_query in file_name.lower():
                        url = s3_client.generate_presigned_url(
                            'get_object',
                            Params={
                                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                'Key': file_path
                            },
                            ExpiresIn=3600
                        )

                        files.append({
                            'name': file_name,
                            'path': file_path,
                            'size': item['Size'],
                            'last_modified': item['LastModified'],
                            'url': url,
                            'type': file_type
                        })

    except ClientError as e:
        messages.error(request, str(e))

    # Build breadcrumbs
    breadcrumbs = []
    path_parts = current_path.rstrip('/').split('/')
    current_breadcrumb = ''
    for part in path_parts:
        if part:
            current_breadcrumb += part + '/'
            breadcrumbs.append({
                'name': part,
                'path': current_breadcrumb
            })

    all_items = directories + files
    all_items.sort(key=lambda x: (x['type'] != 'directory', x['name'].lower()))

    # Add pagination
    paginator = Paginator(all_items, PER_PAGE)
    page_num = request.GET.get(PAGE_VAR, 1)
    pagination_required = paginator.num_pages > 1
    page_range = paginator.get_elided_page_range(page_num) if pagination_required else []
    page_obj = paginator.get_page(page_num)

    return render(request, 's3_files.html', {
        'title': 'Django AWS S3 File Manager',
        'current_path': current_path,
        'breadcrumbs': breadcrumbs,
        'search_query': search_query,
        'base_prefix': base_prefix,
        'show_result_count': bool(search_query),
        'show_thumbnails': SHOW_THUMBNAILS,
        'items': page_obj.object_list,
        'pagination_required': pagination_required,
        'paginator': paginator,
        'result_count': len(all_items),
        'page_range': page_range,
        'page_num': page_num,
        'ALL_VAR': ALL_VAR,
        'per_page': PER_PAGE,
    })


# @login_required  # Optional: Add if you want to require login
@csrf_protect
@require_POST
@staff_member_required
def delete_file(request, delete_path=None):
    if not delete_path:
        return JsonResponse({'error': 'No file path provided'}, status=400)

    s3_client = get_s3_client()
    try:
        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=delete_path
        )

        # Extracting file name and directory path
        file_name = delete_path.split('/')[-1]  # Ambassador.csv
        # directory_path = '/'.join(delete_path.split('/')[:-1]) + '/'  # media/downloads/

        messages.success(request, f'Successfully deleted {file_name}.')
        return JsonResponse({'success': True})
    except ClientError as e:
        # print(e)
        messages.error(request, f'Error deleting file: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)