import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Define function to read parquet file and filter data by year
def get_df_year_filter(df, year1, year2):
    selected_dates = [f"{year1}-01-01", f"{year2}-01-01"]
    year_string = str(year1) + "-" + str(year2)
    df = df[df["date"].isin(selected_dates)]
    num_rows = df.shape[0]
    num_col = df.shape[1]
    i = 0 + 1
    # while i<num_rows-1:
    for i in range(1, num_rows):
        print(i)
        for j in range(1, num_col):
            # df.iloc[i,j] = (df.iloc[i+1,j] - df.iloc[i,j]) / abs (df.iloc[i,j])*100

            df.iloc[i, j] = (
                (df.iloc[i, j] - df.iloc[i - 1, j]) / abs(df.iloc[i - 1, j]) * 100
            )
        i += 1

    df.set_index("date", inplace=True)
    df_percentage_change = df.T.reset_index()
    df_percentage_change.reset_index(inplace=True)
    df_percentage_change.rename(columns={"index": "date"}, inplace=True)
    columns = df_percentage_change.columns.tolist()
    # columns[2] = '2022-2023'
    columns[3] = year_string
    columns[1] = "pairs"
    df_percentage_change.columns = columns
    print(df_percentage_change)
    return df_percentage_change


# Define function to plot pairs
def plot_pairs(df_percentage_change, year1, year2):
    plt.figure(figsize=(30, 15))
    year_string = str(year1) + "-" + str(year2)
    sns.barplot(x="pairs", y=year_string, data=df_percentage_change, hue="pairs")
    plt.title(
        f"Percentage Change of Currency Pairs with Respect to MYR in {year_string}"
    )
    plt.xlabel("Date")
    plt.ylabel("Percentage Change")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)


# Streamlit app
def main():
    st.title("Currency Pair Percentage Change")
    year1 = st.number_input(
        "Enter the first year:", min_value=2000, max_value=2024, value=2020
    )
    year2 = st.number_input(
        "Enter the second year:", min_value=2000, max_value=2024, value=2021
    )
    if st.button("Get Plot"):
        # Read data from parquet file
        df = pd.read_parquet("exchangerates.parquet")

        # Filter data and calculate percentage change
        df_percentage_change = get_df_year_filter(df, year1, year2)

        # Plot pairs
        plot_pairs(df_percentage_change, year1, year2)


if __name__ == "__main__":
    main()
