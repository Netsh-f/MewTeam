# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 18:19
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path
from project.views import curd
urlpatterns = [
    path('teams/<int:team_id>/create/', curd.create_project, name='create_project'),
    path('teams/<int:team_id>/projects/<int:pro_id>/update/', curd.update_project, name='update_project'),
    path('teams/<int:team_id>/projects/<int:pro_id>/delete/', curd.delete_project, name='delete_project'),
    path('teams/<int:team_id>/projects/<int:pro_id>/recover/', curd.recover_project, name="recover_project"),
    path('teams/<int:team_id>/projects/<int:pro_id>/list/', curd.list_project, name='list_project')
]