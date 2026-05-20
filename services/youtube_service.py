import webbrowser


def recommend_videos(skill):

    print("\n===== RECOMMENDED YOUTUBE VIDEOS =====\n")

    queries = [
        f"{skill} tutorial for beginners",
        f"best {skill} playlist",
        f"{skill} crash course"
    ]

    for i, query in enumerate(queries, start=1):

        youtube_link = (
            f"https://www.youtube.com/results?search_query={query}"
        )

        print(f"{i}. {query}")
        print(youtube_link)
        print()

    open_video = input(
        "\nDo you want to open YouTube recommendations? (yes/no): "
    )

    if open_video.lower() == "yes":
        webbrowser.open(
            f"https://www.youtube.com/results?search_query={skill}+tutorial"
        )