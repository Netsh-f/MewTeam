from django.core.mail import send_mail

from MewTeam import settings
from team.models import Invitations


def _send_email(subject, message, email_addr):
    send_mail(subject, message, settings.EMAIL_HOST_USER, email_addr, fail_silently=False)


def send_invitation(invitation: Invitations):
    _send_email('MewTeam团队邀请',
                '你收到了一个邀请，登录主页输入邀请码即可加入团队。\n邀请码：' + invitation.invitation_code,
                invitation.receiver_email)
