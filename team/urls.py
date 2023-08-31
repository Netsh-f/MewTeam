from django.urls import path

from team.views import teams, members, invitation

urlpatterns = [
    path('teams/<int:team_id>/users/', members.get_team_user_list),
    path('teams/', teams.create_team),
    path('teams/<int:team_id>/users/<int:user_id>/promote/', members.promote_user_to_admin),
    path('teams/<int:team_id>/users/<int:user_id>/deomote/', members.demote_admin_to_user),
    path('teams/<int:team_id>/invitations/send/', invitation.generate_invitation),
    path('user/teams/', teams.get_team_list),
    path('teams/join/', invitation.join_team_with_invitation),
    path('teams/<int:team_id>', teams.disband_team),
    path('teams/<int:team_id>/users/<int:user_id>/', members.remove_team_user),
    path('teams/<int:team_id>/users/<int:user_id>/join/', invitation.join_team),
    path('teams/<int:team_id>/avatar/', teams.update_team_avatar),
]
