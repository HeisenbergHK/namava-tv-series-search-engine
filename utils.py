import math

import pandas as pd

df = pd.read_csv("data.csv")


def sort_key(item):
    # If imdbs is not a number (nan), use hit instead
    if math.isnan(item["imdb"]) or item["imdb"] == 0:
        return (
            item["hit"] / 10
        )  # Instead of 0-100, it should be between 0-10, so we divide by 10
    return item["imdb"]


def search_top_5(prefix_keyword):
    result = []
    seen = set()

    while True:
        if len(result) >= 5 or not prefix_keyword:
            break

        filtered_df = df[df["series_name"].str.startswith(prefix_keyword)]
        temp = filtered_df.to_dict(orient="records")

        sorted_list = sorted(temp, key=sort_key, reverse=True)

        # Only add unique items
        for item in sorted_list:
            title = item["series_name"]
            if title not in seen:

                # if a cell in imdb is empty, it becomes NaN (a Python float('nan'))
                # So Changing imdb value to null instead of Nan for a valid json response in the front
                if isinstance(item["imdb"], float):
                    item["imdb"] = None

                seen.add(title)
                result.append(item)

        prefix_keyword = prefix_keyword[:-1]

    return result[:5]
