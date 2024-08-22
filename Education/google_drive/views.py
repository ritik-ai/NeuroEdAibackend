# views.py
from django.shortcuts import render
from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def google_drive_files(request):
    # Load credentials (you need to store these securely)
    credentials = Credentials.from_authorized_user_file('D:\project\Backendeducation\Education\Secret')

    # Build the Drive service
    drive_service = build('drive', 'v3', credentials=credentials)

    # Fetch file metadata (you may need to adjust this)
    results = drive_service.files().list(pageSize=10, fields="files(id, name)").execute()
    files = results.get('files', [])

    # Render a template with the file links
    return render(request, 'google_drive_files.html', {'files': files})

def download_file(request, file_id):
    # Load credentials (you need to store these securely)
    credentials = Credentials.from_authorized_user_file('D:\project\Backendeducation\Education\Secret')

    # Build the Drive service
    drive_service = build('drive', 'v3', credentials=credentials)

    # Download the file content
    file_data = drive_service.files().get_media(fileId=file_id).execute()

    # Serve the file as a download
    response = HttpResponse(file_data, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="file.pdf"'  # Adjust filename as needed
    return response
    