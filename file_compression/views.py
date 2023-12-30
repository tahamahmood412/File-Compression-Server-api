import os
import gzip
from django.shortcuts import HttpResponse,render
from django.core.files.storage import FileSystemStorage
from .forms import FileUploadForm


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage(location='media/uploads/')
            saved_file = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(saved_file)
            
            compressed_file_path = compress_file(file_path, uploaded_file.name)
            
            if compressed_file_path:
                response = provide_download(compressed_file_path, uploaded_file.name)
                # remove_files(file_path, compressed_file_path)
                if response:
                    return response
                else:
                    return render(request, 'error.html')
            else:
                return render(request, 'error.html')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})


def compress_file(file_path, file_name):
    try:
        if os.path.exists(file_path):
            compressed_file_path = file_path + '.gz'
            with open(file_path, 'rb') as file:
                with gzip.open(compressed_file_path, 'wb') as compressed_file:
                    compressed_file.writelines(file)
            print(f"File '{file_name}' compressed successfully as '{file_name}.gz'")
            return compressed_file_path
            
        else:
            print("File not found.")
    except Exception as e:
        print(f"An error occurred during compression: {e}")
    return None


def provide_download(compressed_file_path, file_name):
    try:
        if os.path.exists(compressed_file_path):
            with open(compressed_file_path, 'rb') as compressed_file:
                response = HttpResponse(compressed_file, content_type='application/x-gzip')
                response['Content-Disposition'] = f'attachment; filename="{file_name}.gz"'
                return response
        else:
            print("Compressed file not found.")
    except Exception as e:
        print(f"An error occurred during download: {e}")
    return None

