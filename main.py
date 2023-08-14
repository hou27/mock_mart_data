import sys

from add_cycle import add_cycle
from detect_trend import (
    calc_prob,
    detect_decrease_stock,
)
from generate_excel import generate_excel
from init import clean_first_cycle, init


if __name__ == "__main__":
    # 초기 사이클 생성 및 정리(정렬)
    df = clean_first_cycle(init())

    # 판매량 감소 추세 탐지 및 확률 생성
    trend_probs = calc_prob(df, detect_decrease_stock(df))

    n = 1
    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    # 추가 사이클 n번 생성
    for _ in range(n):
        df = add_cycle(df, trend_probs)
        print(f"사이클 추가: {len(df)}개")

    # 엑셀 파일로 저장
    generate_excel(df)
