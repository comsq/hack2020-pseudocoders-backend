from json import loads

from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .models import User


@csrf_exempt
def login(req: HttpRequest):
    if req.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    req_data = loads(req.body)
    login = req_data.get('login')
    password = req_data.get('password')

    user = User.objects.filter(login=login, password=password).first()
    if user is None:
        return HttpResponse(status=401)

    return JsonResponse({
        'id': user.id,
        'login': user.login,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'email': user.email,
        'type': user.user_type,
    })
