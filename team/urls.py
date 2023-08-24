from django.urls import path

from team.views import get_team_members

urlpatterns = [
    path('get_team_member/', get_team_members.get_team_member, name='get_team_member'),
]