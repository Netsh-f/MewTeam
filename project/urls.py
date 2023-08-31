# ------- Litang Save The World! -------
#
# @Time    : 2023/8/25 18:19
# @Author  : Lynx
# @File    : urls.py
#
from django.urls import path
from project.views import pro_manage, document, prototype, guest, doc_manage

urlpatterns = {
    path('teams/<int:team_id>/create/', pro_manage.create_project, name='create_project'),
    path('teams/<int:team_id>/search/', pro_manage.search_project, name='search_project'),
    path('teams/<int:team_id>/destroy/', pro_manage.destroy_all_project, name='destroy_all'),
    path('teams/<int:team_id>/list/', pro_manage.list_project, name='list_project'),

    path('projects/<int:pro_id>/update/', pro_manage.update_project, name='update_project'),
    path('projects/<int:pro_id>/delete/', pro_manage.delete_project, name='delete_project'),
    path('projects/<int:pro_id>/recover/', pro_manage.recover_project, name="recover_project"),
    path('projects/<int:pro_id>/destroy/', pro_manage.destroy_project, name='destroy_project'),
    path('projects/<int:pro_id>/copy/', pro_manage.copy_project, name='copy_project'),

    path('projects/<int:pro_id>/documents/', doc_manage.create_document),
    path('projects/<int:pro_id>/directories/', doc_manage.create_dir),
    path('projects/<int:pro_id>/documents/get/', doc_manage.get_documents),

    path('documents/<int:document_id>/', document.save_document),
    path('documents/<int:document_id>/latest/', document.get_latest_document),
    path('documents/<int:document_id>/history/', document.get_history_document_list),
    path('documents/contents/<int:document_content_id>/', document.get_document_content_by_id),

    path('projects/<int:pro_id>/prototypes/', prototype.create_prototype),
    path('projects/<int:pro_id>/prototypes/list/', prototype.list_prototype),
    path('prototypes/<int:ptt_id>/save/', prototype.save_prototype),
    path('prototypes/<int:ptt_id>/update/', prototype.update_prototype),
    path('prototypes/<int:ptt_id>/delete/', prototype.delete_prototype),
    path('prototypes/<int:ptt_id>/latest/', prototype.get_latest_prototype),

    path('documents/<int:document_id>/guests/tokens/', guest.generate_guest_token),
    path('guests/tokens/validate/', guest.validate_guest_token),
    path('documents/<int:document_id>/delete/', document.delete_document),
    path('documents/<int:document_id>/restore/', document.restore_document),
    path('documents/<int:document_id>/destroy/', document.destroy_document),
}

