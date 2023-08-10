import pandas as pd
import random
import datetime

from generate_special_event import generate_special_event


# 재고량 감소 함수
def decrease_stock_init(
    sales_data: list, remaining_stock: int, timestamp: datetime, item_id: int
) -> tuple:
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

    if random.random() < prob:
        sales_qty = random.randint(*sale_range)
        remaining_stock = generate_special_event(
            hour, remaining_stock
        )  # 일반적이지 않은 재고 감소 이벤트
        add_sale(sales_qty)

    return sales_data, remaining_stock


# 임의의 초기 데이터프레임 생성
def init() -> pd.DataFrame:
    # remaining_stock: 100, 110, 120, 130, 140, 150 중 하나의 정수
    data = {
        "item_id": range(1, 303),
        "remaining_stock": [[100, 110, 120, 130, 140, 150][i % 5] for i in range(302)],
        "timestamp": ["2023-05-24 00:00:00" for _ in range(302)],
    }
    initial_df = pd.DataFrame(data)

    # 판매 데이터 mocking
    sales_data = []
    for _, row in initial_df.iterrows():
        # 특정 품목에 대한 판매 이벤트 만들기
        remaining_stock = row["remaining_stock"]
        timestamp_sales = datetime.datetime.strptime(
            row["timestamp"], "%Y-%m-%d %H:%M:%S"
        )

        while remaining_stock > 0:
            # 간격을 최소 30분으로 두고 이벤트 생성
            minutes_offset = random.randint(30, 300)
            timestamp_sales += datetime.timedelta(minutes=minutes_offset)
            sales_data, remaining_stock = decrease_stock_init(
                sales_data=sales_data,
                remaining_stock=remaining_stock,
                timestamp=timestamp_sales,
                item_id=row["item_id"],
            )

    # Mocked 판매 데이터를 포함하는 전체 데이터프레임 생성
    sales_df = pd.DataFrame(sales_data)
    df = pd.concat([initial_df, sales_df], ignore_index=True)

    return df


# 첫 사이클 정리
def clean_first_cycle(df: pd.DataFrame) -> pd.DataFrame:
    df.sort_values(by=["timestamp"], inplace=True)
    # 초기 시간인 것은 id 순으로 정렬
    sorted_inital_time_data = df.loc[
        df["timestamp"] == "2023-05-24 00:00:00"
    ].sort_values(by=["item_id"])
    # sorted_inital_time_data를 full_df_ver3의 0 ~ 301번째 행에 대입
    df.iloc[0:302] = sorted_inital_time_data

    # index 재부여
    df.reset_index(drop=True, inplace=True)

    return df
