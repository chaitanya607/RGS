from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            file_path = default_storage.save(f"uploads/{file.name}", ContentFile(file.read()))
            file_url = default_storage.url(file_path)
            return JsonResponse({'location': file_url})
    return JsonResponse({'error': 'Failed to upload image'}, status=400)


def home_page(request):
    """
    Renders the index.html template.
    """
    context = {
    }
    return render(request, 'emailmarketing/home.html', context)
