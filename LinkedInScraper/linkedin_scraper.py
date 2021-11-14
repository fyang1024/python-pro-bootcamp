import os
import csv
import json
import time
import urllib.parse
from requests import Session
from bs4 import BeautifulSoup as bs


class LinkedInScraper:

    def __init__(self, search_terms, num_of_results):
        self.login_form = "https://www.linkedin.com/login?fromSignIn=true&trk" \
                          "=guest_homepage-basic_nav-header-signin"
        self.login_url = "https://www.linkedin.com/checkpoint/lg/login-submit"
        self.search_url = "https://www.linkedin.com/search/results/people" \
                          "/?keywords="
        self.search_terms = self.__split_and_trim(search_terms)
        self.num_of_results = int(num_of_results)

    def search_and_export(self):
        all_profiles = []
        with Session() as s:
            self.__login(s)
            for search_term in self.search_terms:
                all_profiles += self.__search(s, search_term)
        self.__export(all_profiles)

    def __search(self, session, search_term):
        count = 0
        page = 0
        has_more = True
        profiles = []
        while count < self.num_of_results and has_more:
            page += 1
            url = self.__get_search_url(page, search_term)
            print(url)
            search_result = session.get(url)
            soup = bs(search_result.content, "html.parser")
            search_result_tag = self.__find_search_result(soup)
            if search_result_tag is None:
                has_more = False
            else:
                json_data = json.loads(search_result_tag.getText())
                for key in json_data["included"]:
                    if "navigationUrl" in key:
                        url = key["navigationUrl"]
                        print(url)
                        time.sleep(1)  # sleep 1 second to avoid being blocked
                        profiles.append(self.__scrape_profile(session, url))
                        count += 1
                        if count >= self.num_of_results:
                            break
        return profiles

    def __scrape_profile(self, session, profile_url):
        profile = session.get(profile_url)
        profile_soup = bs(profile.content, "html.parser")
        profile_tag = self.__find_profile_data(profile_soup)
        if profile_tag is None:
            return None
        else:
            profile_data = {}
            json_data = json.loads(profile_tag.getText())
            for key in json_data["included"]:
                if "firstName" in key:
                    name = f"{key['firstName']} {key['lastName']}"
                    profile_data["name"] = name
                    headline_parts = key["headline"].split(" at ")
                    profile_data["title"] = headline_parts[0].strip()
                    if len(headline_parts) > 1:
                        profile_data["company"] = headline_parts[1].strip()
                    if "summary" in key:
                        profile_data["about"] = key["summary"]
                    else:
                        profile_data["about"] = ""
                elif "countryUrn" in key:
                    profile_data["location"] = key["defaultLocalizedName"]
                elif "companyName" in key and "dateRange" in key:
                    date_range = key["dateRange"]
                    if date_range is None or "end" not in date_range:
                        profile_data["company"] = key["companyName"]
            if "name" in profile_data:
                return profile_data
            else:
                return None

    def __get_search_url(self, page, search_term):
        url = f"{self.search_url}{urllib.parse.quote(search_term)}"
        if page > 1:
            url += f"&page={page}"
        return url

    def __login(self, session):
        login_page = session.get(self.login_form)
        login = bs(login_page.content, "html.parser")
        token = login.find("input", {"name": "csrfToken"})["value"]
        param = login.find('input', {'name': 'loginCsrfParam'})["value"]
        login_data = {
            "session_key": os.environ["LINKEDIN_USER"],
            "session_password": os.environ["LINKEDIN_PASS"],
            "csrfToken": token,
            "loginCsrfParam": param,
            "trk": "guest_homepage-basic_nav-header-signin",
            "controlId": "d_checkpoint_lg_consumerLogin-login_submit_button",
            "loginFlow": "REMEMBER_ME_OPTIN"
        }
        session.post(self.login_url, login_data)

    @staticmethod
    def __find_search_result(soup):
        tags = soup.find_all("code")
        for tag in tags:
            if "primaryResultType" in tag.getText():
                return tag
        return None

    @staticmethod
    def __find_profile_data(soup):
        tags = soup.find_all("code")
        for tag in tags:
            if "multiLocaleSummary" in tag.getText():
                return tag
        return None

    @staticmethod
    def __split_and_trim(search_terms):
        terms = search_terms.split(",")
        trimmed_terms = []
        for term in terms:
            trimmed_term = term.strip()
            if len(trimmed_term) > 0:
                trimmed_terms.append(trimmed_term)
        return trimmed_terms

    @staticmethod
    def __export(profiles):
        if len(profiles) == 0:
            print("No data to export")
        else:
            keys = profiles[0].keys()
            with open('people.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(profiles)
