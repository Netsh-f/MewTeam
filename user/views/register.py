from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def register(request):
    params = request.data
    email = params['email']
    message = ''
    if not email:
        message = 'email not found'
        return Response({'msg':message}, status=status.HTTP_400_BAD_REQUEST)