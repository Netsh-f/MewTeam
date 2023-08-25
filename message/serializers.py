from rest_framework import serializers

from message.models import Message
from team.serializers import TeamSerializer
from user.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender_user = UserSerializer()
    receiver_user = UserSerializer()
    team = TeamSerializer()

    class Meta:
        model = Message
        fields = '__all__'
