"""这里存放一些默认常量，统一管理"""

# 设置效果常量，增加可读性
BANNER_LENGTH = 5  # 轮播图数量

HEADER_NAV_LENGTH = 8  # 头部导航数量

FOOTER_NAV_LENGTH = 8  # 底部导航数量

# 短信的有效期[单位：秒]
SMS_EXPIRE_TIME = 60 * 4

# 短信的时间间隔[单位：秒]
SMS_INTERVAL_TIME = 60

# 短信的模版id，测试开发时使用 1
SMS_TEMPLATE_ID = 1

# 后端的富文本编辑器中的图片存储域名
SERVER_IMAGE_DOMAIN = 'http://8.149.245.93:8000'

# 积分和现金的兑换比例[兑换1元的积分数量]
CREDIT_MONEY = 10

# 设置订单的超时取消时间
ORDER_OUTTIME = 12 * 60 * 60
