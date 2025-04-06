from my_celery.main import app
from luffyapi.libs.yuntongxun.sms import CCP
from luffyapi.settings import constants
import logging

log = logging.getLogger("django")

@app.task(name="send_sms")
def send_sms(mobile, sms_code):
    """发送短信"""
    try:
        ccp = CCP()
        ret = ccp.send_template_sms(mobile, [sms_code, constants.SMS_EXPIRE_TIME//60], constants.SMS_TEMPLATE_ID)
        if not ret:
            log.error("用户注册短信发送失败！手机号：%s" % mobile)
    except Exception as e:
        log.error("用户注册短信发送失败！手机号：%s" % mobile)
        log.error(e)