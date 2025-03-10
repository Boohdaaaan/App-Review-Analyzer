from google_play_scraper import search


if __name__ == "__main__":
    query = "" # add query here

    result = search(
        query=query,
        lang="en",
        country="us",
        n_hits=5,
    )

    for app in result:
        print(f"{app['title']}\nID: {app['appId']}\n")
