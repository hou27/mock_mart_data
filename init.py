import pandas as pd
import random
import datetime

from decrease_stock import decrease_stock


# 임의의 초기 데이터프레임 생성
def init() -> pd.DataFrame:
    # remaining_stock: 100, 110, 120, 130, 140 중 하나의 정수
    data = {
        "item_id": range(1, 302),
        "remaining_stock": [[100, 110, 120, 130, 140][i % 5] for i in range(301)],
        "timestamp": ["2023-05-24 00:00:00" for _ in range(301)],
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
            sales_data, remaining_stock = decrease_stock(
                sales_data=sales_data,
                remaining_stock=remaining_stock,
                timestamp=timestamp_sales,
                item_id=row["item_id"],
            )

            # 재고가 30개 이하인 경우, 50% 확률로 사이클 종료
            if remaining_stock <= 30 and random.random() < 0.5:
                break

    # Mocked 판매 데이터를 포함하는 전체 데이터프레임 생성
    sales_df = pd.DataFrame(sales_data)
    df = pd.concat([initial_df, sales_df], ignore_index=True)

    return df


# 첫 사이클 정리
def sort_cycle(df: pd.DataFrame) -> pd.DataFrame:
    df.sort_values(by=["timestamp"], inplace=True)
    # 초기 시간인 것은 id 순으로 정렬
    sorted_inital_time_data = df.loc[
        df["timestamp"] == "2023-05-24 00:00:00"
    ].sort_values(by=["item_id"])
    # sorted_inital_time_data를 full_df_ver3의 0 ~ 301번째 행에 대입
    df.iloc[0:301] = sorted_inital_time_data

    # index 재부여
    df.reset_index(drop=True, inplace=True)

    return df
