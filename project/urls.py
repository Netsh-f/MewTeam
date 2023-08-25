# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 18:19
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path
from project.views import curd
urlpatterns = [
    path('create/<int:team_id>/', curd.create_project, name='create_project'),
    path('update/<int:team_id>/<int:pro_id>/', curd.update_project, name='update_project'),
    path('delete/<int:team_id>/<int:pro_id>/', curd.delete_project, name='delete_project')

]