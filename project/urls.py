# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 18:19
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path
from project.views import curd, document, prototype, guest

urlpatterns = {
    path('teams/<int:team_id>/create/', curd.create_project, name='create_project'),
    path('teams/<int:team_id>/projects/<int:pro_id>/update/', curd.update_project, name='update_project'),
    path('teams/<int:team_id>/projects/<int:pro_id>/delete/', curd.delete_project, name='delete_project'),
    path('teams/<int:team_id>/projects/<int:pro_id>/recover/', curd.recover_project, name="recover_project"),
    path('teams/<int:team_id>/list/', curd.list_project, name='list_project'),
    path('projects/<int:pro_id>/documents/', document.create_document),
    path('projects/<int:pro_id>/documents/get/', document.get_documents_by_project_id),
    path('documents/<int:document_id>/', document.save_document),
    path('documents/<int:document_id>/latest/', document.get_latest_document),
    path('documents/<int:document_id>/history/', document.get_history_document_list),
    path('documents/contents/<int:document_content_id>/', document.get_document_content_by_id),
    path('projects/<int:pro_id>/prototypes/', prototype.save_prototype),
    path('projects/<int:pro_id>/prototypes/latest/', prototype.get_latest_prototype),
    path('teams/<int:team_id>/projects/<int:pro_id>/destroy/', curd.destroy_project, name='destroy_project'),
    path('teams/<int:team_id>/destroy/', curd.destroy_all_project, name='destroy_all'),
    path('documents/<int:document_id>/guests/tokens/', guest.generate_guest_token),
    path('guests/tokens/validate/', guest.validate_guest_token),
    path('documents/<int:document_id>/delete/', document.delete_document),
    path('documents/<int:document_id>/restore/', document.restore_document),
    path('documents/<int:document_id>/destroy/', document.destroy_document),
}
