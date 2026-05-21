import webbrowser
import urllib.parse


def recommend_videos(
    query
):

    search_queries = [

        f"{query} tutorial "
        f"for beginners",

        f"best {query} "
        f"playlist",

        f"{query} crash "
        f"course"
    ]

    videos = []

    for q in search_queries:

        encoded_query = (
            urllib.parse.quote(
                q
            )
        )

        url = (
            "https://www.youtube.com/"
            "results?search_query="
            f"{encoded_query}"
        )

        videos.append(
            {
                "title":
                q.title(),

                "url":
                url
            }
        )

    return videos