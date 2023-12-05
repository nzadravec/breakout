import json


def load() -> list[tuple[str, int]]:
    with open("scores.json", "r") as fp:
        return json.load(fp)


def save(scores: list[tuple[str, int]]):
    with open("scores.json", "w") as fp:
        json.dump(scores, fp)
