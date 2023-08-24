from django.urls import path

from team.views import teams

urlpatterns = [
    path('teams/<int:team_id>/users/', teams.get_team_user_list),
    path('teams/', teams.create_team),
    path('teams/<int:team_id>/users/<int:user_id>/promote', teams.promote_user_to_admin),
]
