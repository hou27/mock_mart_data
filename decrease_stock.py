import random
import datetime

from generate_special_event import generate_special_event

# 재고량 감소 함수
def decrease_stock(
    sales_data: list,
    remaining_stock: int,
    timestamp: datetime,
    item_id: int,
    trend_prob: float = 1.0,
):
    def add_sale(sales_qty: int):
        nonlocal remaining_stock
        # 재고 음수 방지
        remaining_stock = max(remaining_stock - sales_qty, 0)
        sale_row = {
            "item_id": item_id,
            "remaining_stock": remaining_stock,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        sales_data.append(sale_row)

    hour = timestamp.hour
    prob, sale_range = None, None

    # 새벽 시간인 경우, 30% 확률로 1~3개 판매, 70% 확률로 판매 없음
    if hour < 6:
        prob, sale_range = 0.3, (1, 3)
    # 06 ~ 09시 사이인 경우, 50% 확률로 1~5개 판매, 50% 확률로 판매 없음
    elif 6 <= hour < 9:
        prob, sale_range = 0.5, (1, 5)
    else:
        prob, sale_range = 1.0, (1, 5)

    if random.random() < prob and random.random() < trend_prob:
        sales_qty = random.randint(*sale_range)

        remaining_stock = generate_special_event(
            timestamp.hour, remaining_stock
        )  # 일반적이지 않은 재고 감소 이벤트
        add_sale(sales_qty)

    return sales_data, remaining_stock