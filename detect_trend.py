import pandas as pd


# 재고량이 줄어들던 추세를 탐지하는 함수
def detect_decrease_stock(df: pd.DataFrame) -> list:
    # 추세
    trend = [[0 for _ in range(12)] for _ in range(302)]

    for i in range(1, 302):
        df_for_single_product = df.loc[df["item_id"] == i].reset_index(drop=True)
        # 날짜 상관없이 시간대별로 정렬

        ## 날짜 제거
        df_for_single_product["timestamp"] = df_for_single_product["timestamp"].apply(
            lambda x: x.split(" ")[1]
        )
        ## 시간대별로 정렬
        df_for_single_product = df_for_single_product.sort_values(
            by=["timestamp"]
        ).reset_index(drop=True)

        # 추세 탐지
        k = 0
        idx = 0
        while k < 23 and idx < len(df_for_single_product):
            if int(df_for_single_product.iloc[idx]["timestamp"].split(":")[0]) <= k + 1:
                trend[i][k // 2] += 1
            else:
                k += 2
            idx += 1

    return trend


# 각 시간대별 확률을 계산하는 함수
def calc_prob(df: pd.DataFrame, trend: list) -> list:
    trend = detect_decrease_stock(df)
    decrease_prob = []
    for t in trend:
        event_counts = t

        # 중복 제거 후 정렬
        sorted_event_counts = list(set(event_counts))
        sorted_event_counts.sort(reverse=True)

        # 각 시간대별 확률을 계산
        probabilities = [
            round(1.0 - (i * 0.1), 1) for i in range(len(sorted_event_counts))
        ]

        # 각 시간대별 확률을 시간대별 이벤트 개수에 맞게 배분
        prob_dict = {}
        for i in range(len(sorted_event_counts)):
            prob_dict[sorted_event_counts[i]] = probabilities[i]

        original_prob = [prob_dict[i] for i in event_counts]

        decrease_prob.append(original_prob)

    return decrease_prob
