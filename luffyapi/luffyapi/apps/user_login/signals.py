from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User, Credit


@receiver(pre_save, sender=User)
def record_credit_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # 新建用户不记录变化

    try:
        old_instance = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return  # 如果不存在旧记录，不记录变化

    old_credit = old_instance.credit
    new_credit = instance.credit

    if old_credit != new_credit:
        credit_diff = new_credit - old_credit

        # 使用更安全的方式获取操作类型
        opera = 0 if credit_diff > 0 else 1  # 0=赚取, 1=消费

        Credit.objects.create(
            user=instance,
            opera=opera,
            number=abs(credit_diff)
        )
