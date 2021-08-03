import re
import json
from operator import attrgetter
from utils import AthleteScore


class IFSCResultParser:

    rounds = ["qualification", "semis", "finals"]

    def __init__(self, json_results):
        self.json_results = json_results
        self.ranking = self.json_results["ranking"]
        self.score_regex = re.compile(r"\d+")

    def who_qualified(self, round="finals"):

        qualifiers = []

        # lookup a threshold which tells us how many rounds they got through
        # based on the name of the round we want
        # why doesn't python have built in enums
        threshold = self.rounds.index(round)

        for athlete in self.ranking:
            if len(athlete["rounds"]) > threshold:
                qualifiers.append(athlete)

        return qualifiers

    def get_rank_after_qualification(self, qualifiers):

        ranking_after_qualification = []

        for athlete in qualifiers:

            id, first_name, last_name = (
                athlete["athlete_id"],
                athlete["firstname"],
                athlete["lastname"],
            )

            qualification_score = athlete["rounds"][0]["score"]
            qualification_score = qualification_score.replace("\xa0", " ")

            # e.g. '4T5z 14 9',
            score_string, top_attempts, zone_attempts = qualification_score.split(" ")

            tops, zones = self.score_regex.findall(score_string)

            athlete_score = AthleteScore(
                id, first_name, last_name, tops, zones, top_attempts, zone_attempts
            )

            ranking_after_qualification.append(athlete_score)

        ranking_after_qualification = sorted(
            ranking_after_qualification,
            key=attrgetter("tops", "zones", "top_attempts", "zone_attempts"),
            reverse=True,
        )

        return [athlete.athlete_id for athlete in ranking_after_qualification]

    def get_rank_after_finals(self, qualifiers):

        ranking_after_finals = []

        for athlete in qualifiers:
            athlete_id, athlete_rank = athlete["athlete_id"], athlete["rank"]
            ranking_after_finals.append((athlete_id, athlete_rank))

        return [
            id
            for (id, _) in sorted(
                ranking_after_finals, key=lambda x: x[1], reverse=True
            )
        ]

    def save(self):

        with open(f"outputs/{self.json_results['event']}.json", "w+") as f:
            json.dump(self.json_results, f)
