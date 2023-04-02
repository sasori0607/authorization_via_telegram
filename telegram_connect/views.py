from uuid import uuid4
import requests
from django.core.files.base import ContentFile
from .models import Profile
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()


def check_login(request):
    if request.method == 'GET':
        login = request.GET.get('login')
        print(login)
        if User.objects.filter(username=login).exists():
            return HttpResponse(json.dumps({'is_unique': False}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'is_unique': True}), content_type='application/json')
    else:
        return HttpResponse(status=405)


def check_email(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        print(email)
        if User.objects.filter(email=email).exists():
            return HttpResponse(json.dumps({'is_unique': False}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'is_unique': True}), content_type='application/json')
    else:
        return HttpResponse(status=405)


@ensure_csrf_cookie
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        login = data.get('login')
        email = data.get('email')
        password = data.get('password')
        #
        name = data.get('name')
        avatar_url = data.get('avatar_url')
        tg_id = data.get('tg_id')
        if not (login and email and password and name and id):
            return JsonResponse({'error': 'Missing required data'}, status=400)
        user = User.objects.create_user(username=login, email=email, password=password, is_superuser=True,
                                        is_staff=True)
        user.save()
        profile = Profile(user=user, name=name, tg_id=tg_id)
        if avatar_url:
            response = requests.get(avatar_url)
            if response.status_code == 200:
                file_name = f'{uuid4().hex}.jpg'
                file_content = ContentFile(response.content)
                path = default_storage.save(file_name, file_content)
                profile.avatar = path
        profile.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
