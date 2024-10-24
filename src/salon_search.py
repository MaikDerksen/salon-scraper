import requests
from bs4 import BeautifulSoup
from service_extractor import ServiceExtractor


class SalonSearch:
    def __init__(self, salon_name: str):
        self.salon_name = salon_name
        self.salon_details = None

    def format_salon_name(self):
        return self.salon_name.lower().replace(' ', '-').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')

    def fetch_salon_page(self):
        formatted_salon_name = self.format_salon_name()
        search_url = f"https://www.treatwell.de/ort/{formatted_salon_name}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'
        }
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            print(f"Request successful for salon: {self.salon_name}")
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    def extract_salon_details(self, soup):
        salon_title = soup.find('h1')
        salon_address = soup.find_all("span", class_="Text-module_smHeader__3mR_U style-module--addressPart--484b23")
        address_parts = [part.text.strip() for part in salon_address if part]

        salon_full_address = ' '.join(address_parts)
        salon_rating = soup.find('span', class_='Text-module_smHero__2uXfi Rating-module_label__1wOHw')
        salon_rating_count = soup.find("span", class_="Text-module_smHeader__3mR_U style-module--reviewCount--e5a80c")

        service_extractor = ServiceExtractor(soup)
        services = service_extractor.extract_services()

        self.salon_details = {
            'name': salon_title.text.strip() if salon_title else "No title found",
            'address': salon_full_address if salon_full_address else "No address found",
            'rating': salon_rating.text.strip() if salon_rating else "No rating found",
            'rating_count': salon_rating_count.text.strip() if salon_rating_count else "No rating count",
            'services': services
        }

    def get_salon_details(self):
        return self.salon_details
