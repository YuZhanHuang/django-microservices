from django.core.management import BaseCommand
from core.models import Order
from django.db import connections


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 直接從old資料庫查orders會報錯
        # orders = Order.objects.using('old').all()
        # django.db.utils.OperationalError: (1054, "Unknown column 'core_order.total' in 'field list'")
        with connections['old'].cursor() as cursor:
            cursor.execute('SELECT * FROM core_order where complete = 1')
            orders = cursor.fetchall()

            for order in orders:

                cursor.execute(f'SELECT * FROM core_orderitem WHERE order_id = \'{order[0]}\'')
                order_items = cursor.fetchall()
                Order.objects.create(
                    id=order[0],
                    code=order[2],
                    user_id=order[14],
                    total=sum(item[5] for item in order_items)
                )
