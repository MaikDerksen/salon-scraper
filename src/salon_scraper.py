import requests
from bs4 import BeautifulSoup
from service_extractor import ServiceExtractor
import os

class SalonSearch:
    def __init__(self, salon_name: str):
        self.salon_name = salon_name
        self.salon_details = None

    def format_name(self):
        return (self.salon_name.lower()
            .replace(' ', '-').replace("'", "-").replace('"', "-")
            .replace("+", "-").replace("|", "-").replace(",", "-")
            .replace("ß", "ss").replace('ä', 'ae').replace('ö', 'oe')
            .replace('ü', 'ue').replace("@", "-").replace("(", "-")
            .replace(")", "-").replace(".", "-").replace("&", "-")
            .replace("/", "-").replace(":", "-").replace(";", "-")
            .replace("?", "-").replace("!", "-").replace("#", "-")
            .replace("=", "-").replace("%", "-").replace("‘", "-")
            .replace("•", "-").replace("*", "-").replace("…", "-")
            .replace("©", "-").replace("$", "-").replace("€", "-")
            .replace("<", "-").replace(">", "-").replace("[", "-")
            .replace("]", "-").replace("{", "-").replace("}", "-")
            .replace("^", "-").replace("~", "-").replace("`", "-")
            .replace("\\", "-").replace("°", "-").replace("™", "-")
            .replace("®", "-").replace("√", "-").replace("—", "-")
            .replace("---", "-").replace("--", "-")
        
            # Replacements for 'a' variations
            .replace('á', 'a').replace('à', 'a').replace('â', 'a')
            .replace('ä', 'ae').replace('ã', 'a').replace('å', 'a')
            .replace('ā', 'a').replace('æ', 'ae').replace('ą', 'a')
            .replace('ā', 'a')
        
            # Replacements for 'e' variations
            .replace('é', 'e').replace('è', 'e').replace('ê', 'e')
            .replace('ë', 'e').replace('ē', 'e').replace('ę', 'e')
            .replace('ė', 'e').replace('ɛ', 'e').replace('ĕ', 'e')
            .replace('ě', 'e')

            # Replacements for 'i' variations
            .replace('í', 'i').replace('ì', 'i').replace('î', 'i')
            .replace('ï', 'i').replace('ī', 'i').replace('į', 'i')
            .replace('ı', 'i').replace('ĭ', 'i')

            # Replacements for 'o' variations
            .replace('ó', 'o').replace('ò', 'o').replace('ô', 'o')
            .replace('ö', 'oe').replace('õ', 'o').replace('ø', 'o')
            .replace('ō', 'o').replace('œ', 'oe').replace('ő', 'o')

            # Replacements for 'u' variations
            .replace('ú', 'u').replace('ù', 'u').replace('û', 'u')
            .replace('ü', 'ue').replace('ů', 'u').replace('ū', 'u')
            .replace('ű', 'u').replace('ų', 'u')

            .strip('-'))


    def fetch_salon_page(self):
        formatted_salon_name = self.format_name()
        search_url = f"https://www.treatwell.de/ort/{formatted_salon_name}"
        print(f"Searching for salon: {search_url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'
        }
    
        # First attempt
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            print(f"Request successful for salon: {self.salon_name}")
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Request failed with status code {response.status_code}")
            self.log_failed_request(search_url, response.status_code)  # Log the failed request
        
            # Second attempt
            second_search_url = f"https://www.treatwell.de/ort/{formatted_salon_name}-2"
            second_response = requests.get(second_search_url, headers=headers)
            print(f"Trying with URL: {second_search_url}")
            if second_response.status_code == 200:
                print(f"Request successful for salon: {self.salon_name}")
                return BeautifulSoup(second_response.text, 'html.parser')
            else:
                print(f"Request failed with status code {second_response.status_code}")
                self.log_failed_request(second_search_url, second_response.status_code)  # Log the second failed request

                # Third attempt
                third_search_url = f"https://www.treatwell.de/ort/{formatted_salon_name}-1"
                third_response = requests.get(third_search_url, headers=headers)
                print(f"Trying with URL: {third_search_url}")
                if third_response.status_code == 200:
                    print(f"Request successful for salon: {self.salon_name}")
                    return BeautifulSoup(third_response.text, 'html.parser')
                else:
                    print(f"Request failed with status code {third_response.status_code}")
                    self.log_failed_request(third_search_url, third_response.status_code)  # Log the third failed request

        return None


    def log_failed_request(self, url, status_code):
        # Ensure the failed_salon directory exists
        failed_folder_path = 'failed_salon'
        if not os.path.exists(failed_folder_path):
            os.makedirs(failed_folder_path)

        # Create a log entry
        filename = 'failed_requests.log'
        file_path = os.path.join(failed_folder_path, filename)
        
        with open(file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Failed URL: {url} | Status Code: {status_code} | Salon Name: {self.salon_name}\n")

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
