import asyncio
import os

import aiofiles
import aiohttp

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}


async def get_detail(session, url, sem):
    async with sem:
        async with session.get(url) as response:
            return await response.json()


async def main():
    print("Start to Collect data...")
    ps = 30
    pi = 1
    sem = asyncio.Semaphore(30)

    file_name = "data.csv"
    file_exist = os.path.exists(file_name)
    mode = "w" if file_exist else "a"

    async with aiohttp.ClientSession(headers=headers) as session:
        async with aiofiles.open(
            file_name, mode, newline="", encoding="utf-8"
        ) as async_file:
            # if not file_exist:
            await async_file.write("series_id,series_name,hit,imdb\n")

            while True:
                url = f"https://www.namava.ir/api/v1.0/medias/latest-series?pi={pi}&ps={ps}"

                async with session.get(url) as response:
                    if response.status != 200:
                        break

                    response_json = await response.json()
                    result = response_json["result"]
                    if not result:
                        break

                    tasks = []
                    meta = []

                    for res in result:
                        series_id = res["id"]
                        series_name = res["caption"]
                        url_for_rating = f"https://www.namava.ir/api/v1.0/medias/{series_id}/brief-preview"

                        tasks.append(
                            asyncio.create_task(
                                get_detail(session, url_for_rating, sem)
                            )
                        )
                        meta.append((series_id, series_name))

                    responses = await asyncio.gather(*tasks)

                    for (series_id, series_name), res in zip(meta, responses):
                        hit = res["result"]["hit"]
                        imdb = res["result"]["imdb"]
                        await async_file.write(
                            f"{series_id},{series_name},{hit},{imdb}\n"
                        )

                    # Forces Python to write everything in the buffer to disk immediately.
                    await async_file.flush()

                    # A brief moment before initiating new requests
                    await asyncio.sleep(0.3)

                # Logs in the terminal
                print(f"Data Collected for: {pi}")
                print("-" * 12)
                pi += 1

                # Uncomment this if you want limited data
                # if pi == 10:
                #     break
    print("Data Collection Ended.")


asyncio.run(main())
