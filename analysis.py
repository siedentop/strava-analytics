import json
import fire
from pprint import pprint
import plotly.express as px
import pandas
from itertools import count


def analyze(fname: str):
    """Print the top 60 rides by length and their rank."""
    with open(fname, "r") as fh:
        data = json.load(fh)
    distances = [ride["distance"] for ride in data]
    distances.sort(reverse=True)

    ranked = [(i, d / 1000) for i, d in enumerate(distances, start=1)]

    pprint(ranked[0:60])


def speed(fname: str):
    """Print the top 10 rides by avg speed."""
    with open(fname, "r") as fh:
        data = json.load(fh)

    def div(num, den):
        if den != 0:
            return num / den
        print(f"{num} / {den}")
        return 0

    def url(id):
        return f"https://www.strava.com/activities/{id}"

    # 5383195734

    data = [r for r in data if r["type"] == "Ride"]
    data = [r for r in data if r["trainer"] == False]
    distances = [
        (
            ride["average_speed"] * 3.6,
            div(ride["distance"], ride["elapsed_time"]) * 3.6,
            div(ride["distance"], ride["moving_time"]) * 3.6,
            ride["name"],
            ride["distance"] / 1000,
            url(ride["id"]),
        )
        for ride in data
    ]

    # elapsed_time, average_speed, average_watts, moving_time, type=Ride,
    # flagged = true???
    # kudos_count
    distances.sort(reverse=True)

    ranked = [(i, *d) for i, d in enumerate(distances, start=1)]

    pprint(ranked[0:10])


def plot(fname: str):
    with open(fname, "r") as fh:
        df = pandas.read_json(fh)
    df["distance"] = df["distance"] / 1000
    df["rank"] = df["distance"].rank(method="min", ascending=False)

    df.sort_values("rank", ascending=False, inplace=True)
    fig = px.line(df, x="rank", y="distance", title="Distance Distribution")
    fig.show()


def target(fname: str, target: int):
    with open(fname, "r") as fh:
        data = json.load(fh)
    distances = [ride["distance"] for ride in data]
    distances.sort(reverse=True)

    ranked = [(i, d / 1000) for i, d in enumerate(distances, start=1)]

    above_target = len([d for d in distances if d >= target * 1000])  # Inefficient
    needed = target - above_target
    print(f"Need {needed} rides above {target} to reach E-number of {target}.")


if __name__ == "__main__":
    fire.Fire()
