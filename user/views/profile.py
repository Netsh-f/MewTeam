import logging
import os.path

from django.http import HttpResponse
from rest_framework.decorators import api_view

from MewTeam.settings import MEDIA_URL, MEDIA_ROOT, BASE_DIR, CONFIG
from shared.error import Error
from shared.res_temp import ResponseTemplate
from shared.token import check_token
from shared.validator import validate_image_name
from user.models import User

logger = logging.getLogger('__name__')


@api_view(['POST'])
def edit_user_avatar(request):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        file = request.FILES.get('file')
        if file is None:
            return ResponseTemplate(Error.FILE_MISSING, 'Missing image file')
        if not validate_image_name(file.name):
            return ResponseTemplate(Error.FILE_TYPE_INVALID, 'Invalid image file type')
        if file.size > CONFIG['MAX_AVATAR_FILE_SIZE']:
            return ResponseTemplate(Error.FILE_SIZE_ILLEGAL, 'Size of file is too large. It should be less than 4mb.')
        user = User.objects.get(id=user_id)
        avatar = f"{CONFIG['AVATAR_PATH']}{user.id}.{file.name.split('.')[-1]}"
        os.makedirs(os.path.dirname(avatar), exist_ok=True)

        # f = open(f"{CONFIG['PROJECT_PATH']}{avatar}", "wb+")
        f = open(avatar, "wb+")
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
        user.avatar = avatar
        user.save()
        return ResponseTemplate(Error.SUCCESS, 'Edit avatar successfully')
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))

@api_view(['GET'])
def view_user_avatar(request, user_id):
    user = User.objects.filter(id=user_id)
    if user:
        avatar_path = user.first().avatar
        if os.path.exists(avatar_path):
            with open(avatar_path, 'rb') as image:
                response = HttpResponse(image.read(), content_type='image/jpg')  # Adjust content type as needed
                return response
    else:
        return HttpResponse("Image not found", status=404)