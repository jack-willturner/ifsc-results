import requests
from urllib.parse import urlparse, parse_qs


class IFSCScraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_api_url = "https://components.ifsc-climbing.org/results-api.php?api=overall_r_result_complete"

    def get_api_url_from_event_url(self, event_url):

        # parse query and get attributes
        query = urlparse(event_url).query
        query_attribs_as_dict = parse_qs(query)

        # we need to grab the event number and the result ID
        event_id = query_attribs_as_dict["event"][0]
        result_id = query_attribs_as_dict["result"][0]

        # now we just need to append them to the api address
        # for some reason, result becomes category here (afaict speed = 1, lead = 2, boulder = 3)
        return self.base_api_url + f"&event_id={event_id}&category_id={result_id}"

    def make_api_request_and_return_json(self, api_request_url):

        api_request_result = self.session.get(api_request_url)
        return api_request_result.json()

    def get_json_data_from_event_url(self, event_url):

        api_request_url = self.get_api_url_from_event_url(event_url)
        json_data = self.make_api_request_and_return_json(api_request_url)

        return json_data
