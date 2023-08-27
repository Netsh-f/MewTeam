from rest_framework import serializers

from team.models import Team, UserTeamShip, Invitations
from user.serializers import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class UserTeamShipSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserTeamShip
        fields = '__all__'


class InvitationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitations
        fields = '__all__'
