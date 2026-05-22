import urllib.parse


def recommend_videos(
    skill
):

    queries = [

        f"{skill} tutorial",

        f"best {skill} playlist",

        f"{skill} crash course"
    ]

    videos = []

    for q in queries:

        url = (
            "https://www.youtube.com/results?"
            f"search_query="
            f"{urllib.parse.quote(q)}"
        )

        videos.append({
            "title": q,
            "url": url
        })

    return videos