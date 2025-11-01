import csv
import os

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}

file_name = "data.csv"
file_exist = os.path.exists(file_name)

ps = 30  # Max is 30
pi = 1  # Starting index

print("Start to Collect data...")

with open(file_name, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_exist:
        writer.writerow(["series_id", "series_name", "hit", "imdb"])

    while True:
        url = f"https://www.namava.ir/api/v1.0/medias/latest-series?pi={pi}&ps={ps}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response = response.json()

            # If there is no more result this would be empty and the loop beaks
            result = response["result"]
            if result == []:
                break

            for res in result:
                # Logs in the terminal
                series_name = res["caption"]
                series_id = res["id"]

                url_for_rating = (
                    f"https://www.namava.ir/api/v1.0/medias/{series_id}/brief-preview"
                )

                review_response = requests.get(url_for_rating, headers=headers)

                if review_response.status_code == 200:
                    print(f"res: {res["id"]}")
                    print("-" * 12)

                    review_response = review_response.json()
                    hit = review_response["result"]["hit"]
                    imdb = review_response["result"]["imdb"]

                    # Inserting a new record to the data.csv
                    writer.writerow([series_id, series_name, hit, imdb])
                else:
                    print(f"Error {response.status_code} res: {res["id"]}")
        else:
            print(f"Error {response.status_code} for page {pi}")

        # Logs in the terminal
        print(f"Data Collected for: {pi}")
        print("-" * 12)

        pi += 1

        if pi == 3:
            break
print("Start to Collect data...")

# print(data)
