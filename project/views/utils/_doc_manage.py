# ------- Litang Save The World! -------
#
# @Time    : 2023/8/30 11:34
# @Author  : Lynx
# @File    : _doc_manage.py.py
#
from django.core.exceptions import ObjectDoesNotExist

from project.models import Project, DocumentDir
from project.serializers import ProjectSerializer


def _init_doc_struction(project: Project):
    try:
        if not DocumentDir.objects.filter(name=f'root_{project.id}').exists():
            return DocumentDir.objects.create(name=f'root_{project.id}', project=project)

    except Exception as e:
        raise ObjectDoesNotExist

