# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 16:29
# @Author  : Lynx
# @File    : curd.py
#
from django.shortcuts import render
from rest_framework.decorators import api_view

from shared.token import check_token


# Create your views here.

@api_view(['POST'])
def create_team(request, team_id):
    response, user_id = check_token(request)
    if user_id == -1:
        return response
    data = request.data
    name = data['name']