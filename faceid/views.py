import io
import datetime
import face_recognition
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.base import ContentFile
from .models import UserPhoto
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout



def index(request):
    return render(request, 'accounts/signup.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        photo = request.FILES.get('photo')

        if name and photo:
            photo_content = photo.read()

            user_photo = UserPhoto(name=name, photo=photo_content)
            user_photo.save()

            return JsonResponse({'success': True, 'name': name})

    return JsonResponse({'success': False})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')

        if photo:
            login_image_content = photo.read()
            login_image = face_recognition.load_image_file(io.BytesIO(login_image_content))
            login_face_encodings = face_recognition.face_encodings(login_image)

            if not login_face_encodings:
                return JsonResponse({'success': False})

            users = UserPhoto.objects.all()
            for user in users:
                registered_image_content = user.photo

                try:
                    registered_image = face_recognition.load_image_file(io.BytesIO(registered_image_content))
                    registered_face_encodings = face_recognition.face_encodings(registered_image)

                    if len(registered_face_encodings) > 0 and \
                            face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])[0]:
                        return JsonResponse({'success': True, 'name': user.name})
                except Exception as e:
                    print(f"Error processing image: {e}")
                    continue

    return JsonResponse({'success': False})


def success(request):
    user_name = request.GET.get('user_name')
    return render(request, 'accounts/login.html', {'user_name': user_name})

def user_logout(request):
    logout(request)
    return redirect('home:index')
