import pandas as pd


def generate_excel(df):
    info_df = pd.read_excel("product_info.xlsx")
    # df의 NO feature를 1부터 순차적으로 증가하도록 변경
    info_df["NO"] = info_df.index + 1

    full_df = df.merge(info_df, left_on="item_id", right_on="NO", how="left")
    full_df.drop(["매장", "시간", "NO"], axis=1, inplace=True)

    full_df.to_excel("명지마트_재고.xlsx", index=False)
