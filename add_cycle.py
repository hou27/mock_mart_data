import pandas as pd
import random
import datetime


# 재고량 감소 함수
def decrease_stock(
    sales_data: list,
    remaining_stock: int,
    timestamp: datetime,
    item_id: int,
    trend_prob: float,
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

    if random.random() < trend_prob:
        sales_qty = random.randint(1, 5)
        add_sale(sales_qty)

    return sales_data, remaining_stock


# remaining_stock이 0인 데이터를 찾아, 다시 mocking하는 코드
def add_sequence(item_id: int, trend_prob: list, start_date: str):
    remaining_stock = [100, 110, 120, 130, 140, 150][
        (item_id - 1) % 5
    ]  # random.choice([100, 110, 120, 130, 140, 150])
    # start_date으로부터 이틀 후 07시부터 시작(이 때 재고량이 채워진다고 가정)
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    timestamp = start_date + datetime.timedelta(days=2)
    timestamp = timestamp.replace(hour=7, minute=0, second=0)

    # 재고가 채워진 시점의 데이터
    sales_data = [
        {
            "item_id": item_id,
            "remaining_stock": remaining_stock,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
    ]

    while remaining_stock > 0:
        # 간격을 최소 30분으로 두고 이벤트 생성
        minutes_offset = random.randint(30, 300)
        timestamp += datetime.timedelta(minutes=minutes_offset)

        sales_data, remaining_stock = decrease_stock(
            sales_data=sales_data,
            remaining_stock=remaining_stock,
            timestamp=timestamp,
            item_id=item_id,
            trend_prob=trend_prob[timestamp.hour // 2],
        )

        # 재고가 30개 이하인 경우, 50% 확률로 사이클 종료
        if remaining_stock <= 30 and random.random() < 0.5:
            break

    return sales_data


# # 재고량이 0이 된 가장 최근 시점을 찾아내 해당 item_id와 함께 list로 반환하는 method
# def find_zero_stock_date(df):
#     zero_stock_date = []
#     for i in df["item_id"].unique():
#         temp_df = df[df["item_id"] == i]
#         if temp_df["remaining_stock"].min() == 0:
#             zero_stock_date.append(
#                 [i, temp_df[temp_df["remaining_stock"] == 0]["timestamp"].max()]
#             )
#     return zero_stock_date


# 이전 사이클의 마지막 시점을 찾아내 해당 item_id와 함께 list로 반환하는 method
def find_last_stock_date(df):
    last_event_of_prev_cycle = []
    for i in df["item_id"].unique():
        temp_df = df[df["item_id"] == i]
        last_event_of_prev_cycle.append([i, temp_df["timestamp"].max()])

    return last_event_of_prev_cycle


# 한 사이클을 더 추가하는 method
def add_cycle(origin_df: pd.DataFrame, trend_probs: list) -> pd.DataFrame:
    addition_sales_data = []
    # trend_probs = calc_prob(first_cycle_ver6)
    for item_id, end_date in find_last_stock_date(origin_df):
        addition_sales_data += add_sequence(item_id, trend_probs[item_id], end_date)

    addition_sales_df = pd.DataFrame(addition_sales_data)

    new_df = pd.concat([origin_df, addition_sales_df], axis=0)[
        ["item_id", "remaining_stock", "timestamp"]
    ]

    return new_df
