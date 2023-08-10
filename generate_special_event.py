import random


def generate_special_event(hour: int, remaining_stock: int):
    prob, sale_range = None, None

    """
    갑작스런 대량 재고 감소
    """
    if hour < 9:
        prob = 0.0
    elif 9 <= hour < 12:
        prob, sale_range = 0.1, (20, 30)
    elif 12 <= hour < 15:
        prob, sale_range = 0.13, (20, 30)
    elif 15 <= hour < 18:
        prob, sale_range = 0.02, (20, 30)
    else:
        prob = 0.0

    if random.random() < prob:
        sales_qty = random.randint(*sale_range)
        print(f"대량 재고 감소: {sales_qty}")
        remaining_stock = max(remaining_stock - sales_qty, 0)

    return remaining_stock
