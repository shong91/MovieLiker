from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail.message import EmailMessage
from MovieLiker.settings import local
FROM_EMAIL = local.EMAIL_HOST_USER


# @shared_task : celery로 따로 작업할 코드라고 선언하는 부분입니다.
@shared_task
def send_email():
    subject = '[MovieLiker] email test'
    to = ['hhhongso@gmail.com']
    message = 'email test is successfully ended. '
    EmailMessage(subject=subject,
                 body=message,
                 to=to,
                 from_email=FROM_EMAIL).send()
    return True


#
# 참고: https://velog.io/@lemontech119/DRF%EB%A1%9C-api-%EC%84%9C%EB%B2%84-%EA%B0%9C%EB%B0%9C6-celery
# 1. Redis server 가동 (D:\redis-server.exe)
#    redis-server /usr/local/etc/redis.conf
# 2. Django 프로젝트 위치에서 터미널을 하나 더 켜서 celery worker를 작동시킴.
#    celery -A {djangoproject} worker -l info
# 3. Django 프로젝트 서버 가동
#    python manage.py runserver