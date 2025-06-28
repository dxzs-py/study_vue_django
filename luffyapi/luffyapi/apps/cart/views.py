from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from course.models import Course, CourseExpire  # 因为在INSTALLED_APPS注册了course，所以没有问题
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
from luffyapi.settings import constants
import logging

log = logging.getLogger("django")


class CartAPIview(ViewSet):  # 使用视图集可以写多个同样的http请求，会比使用视图类（APIView）更简洁
    """购物车的视图类"""
    permission_classes = [IsAuthenticated]  # 登录后才能访问

    def add(self, request):
        """添加商品到购物车中"""
        # 接受客户端提交参数[用户ID,课程ID,勾选状态,有效期选项]
        course_id = request.data.get("course_id")
        user_id = request.user.id
        selected = request.data.get("selected", True)
        expire = request.data.get("expire", 0)

        # 校验参数
        try:
            course = Course.objects.get(is_show=True, id=course_id, is_deleted=False)  # 用于检查是否存在
        except:
            return Response({"message": "课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取redis连接对象
        redis_conn = get_redis_connection('cart')

        # 保存数据到redis
        try:
            with redis_conn.pipeline() as pipe:
                pipe.multi()
                pipe.hset('cart_%s' % user_id, course_id, expire)
                if selected:  # 根据 selected 值决定是否加入选中集合
                    pipe.sadd("selected_%s" % user_id, course_id)
                pipe.execute()

                # 查询购物车中商品总数
                course_len = redis_conn.hlen("cart_%s" % user_id)
        except:
            # log.error("购物车数据库存储错误！")  # utils下的exceptions.py也有记录错误日志的函数，所以可以不写
            return Response({"message": "参数有误！购物车添加商品失败！"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        # 返回结果
        return Response({"message": "添加购物车成功！", "cart_length": course_len}, status=status.HTTP_201_CREATED)

    def list(self, request):
        """查询购物车中商品"""
        user_id = request.user.id
        # 从redis中读取数据
        redis_conn = get_redis_connection('cart')
        cart_bytes_dict = redis_conn.hgetall('cart_%s' % user_id)
        selected_bytes_list = redis_conn.smembers('selected_%s' % user_id)
        # 使用循环从mysql中根据课程ID提前对应商品信息[商品ID,商品封面图,商品标签,商品原价]
        course_list = []
        for course_id_bytes, expire_id_bytes in cart_bytes_dict.items():
            course_id = int(course_id_bytes.decode())  # bytes转str,再从str转int
            expire = int(expire_id_bytes.decode())
            try:
                course = Course.objects.only("id", "course_img", "price", "name").get(id=course_id, is_show=True,
                                                                                      is_deleted=False)
            except Course.DoesNotExist:
                continue

            course_list.append({
                "selected": True if course_id_bytes in selected_bytes_list else False,
                "course_img": constants.SERVER_IMAGE_DOMAIN + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "expired_id": expire,
                "expire_list": course.expire_list,
                "price": float(course.real_price(expire)),
            })
        return Response(course_list, status=status.HTTP_200_OK)

    def change_selected(self, request):
        """切换购物车商品的勾选状态"""
        user_id = request.user.id
        selected = request.data.get("selected")
        course_id = request.data.get("course_id")
        try:
            Course.objects.get(id=course_id, is_show=True, is_deleted=False)
        except Course.DoesNotExist:
            return Response({"message": "课程不存在"}, status=status.HTTP_400_BAD_REQUEST)
        redis_conn = get_redis_connection('cart')
        if selected:
            redis_conn.sadd("selected_%s" % user_id, course_id)
        else:
            redis_conn.srem("selected_%s" % user_id, course_id)

        return Response({"message": "切换成功"}, status=status.HTTP_200_OK)

    def change_expire(self, request):
        """切换购物车商品的有效期状态"""
        user_id = request.user.id
        expire_id = request.data.get("expire_id")
        course_id = request.data.get("course_id")
        try:
            # 判断课程是否存在
            course = Course.objects.get(is_show=True, is_deleted=False, id=course_id)
            # 判断课程的有效期选项是0还是其他的数值，如果是其他数值，还要判断是否存在于有效期选项表中
            if expire_id > 0:
                epxire_item = CourseExpire.objects.filter(is_show=True, is_deleted=False, id=expire_id)
                if not epxire_item:
                    raise Course.DoesNotExist()
        except Course.DoesNotExist:
            return Response({"message": "参数有误！当前商品课程不存在或者不能存在的有效期！"},
                            status=status.HTTP_400_BAD_REQUEST)

        redis_conn = get_redis_connection("cart")
        redis_conn.hset("cart_%s" % user_id, course_id, expire_id)
        # 在切换有效期选项以后，重新获取真实价格
        real_price = course.real_price(expire_id)
        return Response({"message": "切换课程有效期成功！", "real_price": float(real_price)}, status=status.HTTP_200_OK)

    def del_cart(self, request):
        """删除购物车商品"""
        user_id = request.user.id
        course_id = request.query_params.get("course_id")  # deleted 方法得通过？参数传值
        try:
            Course.objects.get(id=course_id, is_show=True, is_deleted=False)
        except Course.DoesNotExist:
            return Response({"message": "课程不存在"}, status=status.HTTP_400_BAD_REQUEST)
        redis_conn = get_redis_connection('cart')
        try:
            with redis_conn.pipeline() as pipe:
                pipe.multi()
                pipe.hdel("cart_%s" % user_id, course_id)
                pipe.srem("selected_%s" % user_id, course_id)
                pipe.execute()
        except:
            return Response({"message": "删除失败！"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        return Response({"message": "删除成功！"}, status=status.HTTP_200_OK)

    def get_selected_course(self, request):
        """获取购物车中勾选的商品数据"""
        #  获取用户ID
        user_id = request.user.id

        # 获取redis连接
        redis_conn = get_redis_connection('cart')
        cart_bytes_dict = redis_conn.hgetall('cart_%s' % user_id)
        selected_bytes_list = redis_conn.smembers('selected_%s' % user_id)

        # 获取勾选的商品
        data = []  # 商品列表
        total_price = 0  # 勾选的商品总价
        for course_id_bytes, expire_id_bytes in cart_bytes_dict.items():
            course_id = int(course_id_bytes.decode())  # bytes转str,再从str转int
            expire_id = int(expire_id_bytes.decode())
            # 判断当前商品id是否在勾选集合中
            if course_id_bytes in selected_bytes_list:
                try:
                    course = Course.objects.get(id=course_id, is_show=True, is_deleted=False)
                except Course.DoesNotExist:
                    continue
                # 判断课程，获取课程原价
                expire_text = "永久有效"
                original_price = course.price
                try:
                    if expire_id > 0:
                        course_expire = CourseExpire.objects.get(id=expire_id)
                        original_price = course_expire.price
                        expire_text = course_expire.expire_text
                except CourseExpire.DoesNotExist:
                    pass
                real_price = float(course.real_price(expire_id))
                data.append({
                    "course_img": constants.SERVER_IMAGE_DOMAIN + course.course_img.url,
                    "name": course.name,
                    "id": course.id,
                    "expired_text": expire_text,
                    "discount_name": course.discount_name,
                    "real_price": real_price,
                    "original_price": float(original_price),
                })
                total_price += real_price
        # 返回结果
        return Response({"course_list":data,"total_price":total_price}, status=status.HTTP_200_OK)
