import os
import gzip
from django.shortcuts import HttpResponse,render
from django.core.files.storage import FileSystemStorage
from .forms import FileUploadForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def receive_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Path where the files will be saved
        save_directory = 'media/uploads/'  # Replace this with your desired directory

        # Check if the directory exists, create it if not
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Save the uploaded file to the specified location
        file_path = os.path.join(save_directory, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return JsonResponse({'message': 'File uploaded & save to server successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'})



#<-------------------UPLOAD FILE BY WEBSITE--------------------->
# def upload_file(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = request.FILES['file']
#             fs = FileSystemStorage(location='media/uploads/')
#             saved_file = fs.save(uploaded_file.name, uploaded_file)
#             file_path = fs.path(saved_file)
            
#             compressed_file_path = compress_file(file_path, uploaded_file.name)
            
#             if compressed_file_path:
#                 response = provide_download(compressed_file_path, uploaded_file.name)
#                 # remove_files(file_path, compressed_file_path)
#                 if response:
#                     return response
#                 else:
#                     return render(request, 'error.html')
#             else:
#                 return render(request, 'error.html')
#     else:
#         form = FileUploadForm()
#     return render(request, 'upload.html', {'form': form})


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

