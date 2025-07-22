from my_celery.main import app
from luffyapi.settings import constants   
from order.models import Order
from datetime import datetime
@app.task(name="check_order")
def check_order():
    """超时取消过期订单"""
    # 超时条件： 当前时间 > (订单生成时间 + 超时时间)   =====>>>>  (当前时间 - 超时时间) > 订单生成时间
    now_timestamp = datetime.now().timestamp()
    timeout_number = now_timestamp - constants.ORDER_OUTTIME
    timeout_date_string = datetime.fromtimestamp(timeout_number)

    order_outtime_list = Order.objects.filter(order_status=0, create_time__lte=timeout_date_string)
    for order in order_outtime_list:
        order.order_status = 3
        order.save()
    
    