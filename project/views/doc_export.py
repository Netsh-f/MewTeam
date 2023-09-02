# ------- Litang Save The World! -------
#
# @Time    : 2023/8/31 21:58
# @Author  : Lynx
# @File    : doc_export.py
#
import os

import pypandoc
from rest_framework.decorators import api_view

from MewTeam.settings import DOCUMENT_URL
from project.models import Document, DocumentContent
from shared.error import Error
from shared.permission import is_team_member
from shared.res_temp import ResponseTemplate
from shared.token import check_token


@api_view(['GET'])
def export_document(request, document_id):
    try:
        response, user_id = check_token(request)
        if user_id == -1:
            return response
        document = Document.objects.get(id=document_id)
        if not is_team_member(user_id, document.project.team_id):
            return ResponseTemplate(Error.PERMISSION_DENIED, 'You are not one member of this team')
        doc_cont = DocumentContent.objects.filter(document=document).order_by('-timestamp').first()
        doc_path = os.path.join(DOCUMENT_URL, f"{document.id}.docx")
        os.makedirs(os.path.dirname(doc_path), exist_ok=True)
        error:str = pypandoc.convert_text(doc_cont.content, 'docx', 'html', outputfile=doc_path)
        if error != '':
            return ResponseTemplate(Error.DOC_EXPORT_FAILED, f'Export failed, error message:{error}')
        return ResponseTemplate(Error.SUCCESS, 'Export document successfully', data={
            'url': doc_path
        })
    except Document.DoesNotExist as e:
        return ResponseTemplate(Error.DATA_NOT_FOUND, str(e))
    except Exception as e:
        return ResponseTemplate(Error.FAILED, str(e))