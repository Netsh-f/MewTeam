from rest_framework import serializers

from message.models import Message, Mention, Room, MessageFile
from team.serializers import TeamSerializer
from user.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender_user = UserSerializer()

    class Meta:
        model = Message
        fields = '__all__'


class MentionSerializer(serializers.ModelSerializer):
    message = MessageSerializer()
    sender_user = UserSerializer()
    text = serializers.SerializerMethodField()

    class Meta:
        model = Mention
        fields = '__all__'

    def get_text(self, obj):
        return obj.text


class RoomSerializer(serializers.ModelSerializer):
    roomId = serializers.IntegerField(source='id')

    class Meta:
        model = Room
        fields = '__all__'


class MessageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageFile
        fields = '__all__'
