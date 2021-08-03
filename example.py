import os
import json
from scraper import IFSCScraper
from parser import IFSCResultParser
from scipy import stats


boulder_events_in_2019 = [
    "https://www.ifsc-climbing.org/index.php/world-competition/calendar/?task=resultathletes&event=1112&result=3",
    "https://www.ifsc-climbing.org/index.php/world-competition/calendar/?task=resultathletes&event=1113&result=3",
    "https://www.ifsc-climbing.org/index.php/world-competition/calendar/?task=resultathletes&event=1114&result=3",
    "https://www.ifsc-climbing.org/index.php/world-competition/calendar/?task=resultathletes&event=1115&result=3",
    "https://www.ifsc-climbing.org/index.php/world-competition/calendar/?task=resultathletes&event=1116&result=3",
    "https://www.ifsc-climbing.org/index.php/world-competition/calendar/?task=resultathletes&event=1117&result=3",
    "https://www.ifsc-climbing.org/index.php/world-competition/calendar/?task=resultathletes&event=1121&result=3",
]


def get_parsers_from_internet(event_list):
    scraper = IFSCScraper()

    parsers = []

    for event in event_list:

        parser = IFSCResultParser(scraper.get_json_data_from_event_url(event))
        parser.save()
        parsers.append(parser)

    return parsers


# scrape_events(boulder_events_in_2019)


def get_parsers_from_saved_json_files():
    parsers = []

    for event_file in os.listdir("outputs/"):

        with open(f"outputs/{event_file}", "r") as json_file:

            json_data = json.load(json_file)

        parsers.append(IFSCResultParser(json_data))

    return parsers


parsers = get_parsers_from_saved_json_files()

# examine relationship between qualification and final rank

rank_after_qualifiers = []
rank_after_finals = []

for event_parser in parsers:
    qualifiers = event_parser.who_qualified()

    rank_after_qualifiers.append(event_parser.get_rank_after_qualification(qualifiers))

    rank_after_finals.append(event_parser.get_rank_after_finals(qualifiers))


"""
Question 1: rank correlation between qualifications and finals
"""

tau, p = stats.kendalltau(rank_after_qualifiers, rank_after_finals)

print(tau, p)

"""
Question 2: if you're in top 3 after qualification, what's the likelihood you make podium?
"""
