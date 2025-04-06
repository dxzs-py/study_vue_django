from celery import shared_task
@shared_task(name='send_mail')
def send_mail(mobile):
    return "hello mail"