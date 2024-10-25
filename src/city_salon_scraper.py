import requests
from bs4 import BeautifulSoup
import os

class SalonNameExtractor:
    def __init__(self, soup):
        self.soup = soup

    def extract_salon_names(self):
        salon_names = []
        salon_items = self.soup.find_all('div', class_='BrowseResultSummary-module--name--04416f')
        
        for item in salon_items:
            salon_name = item.find('h2')
            if salon_name:
                salon_names.append(salon_name.text.strip())
        
        return salon_names

class SalonScraper:
    def __init__(self, city: str):
        self.city = city.lower().replace(' ', '-')
        self.base_url = f"https://www.treatwell.de/orte/behandlung-gruppe-friseur/angebot-typ-lokal/in-{self.city}-de/?view=list"
        self.salon_names = []

    def fetch_page(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"Request successful for URL: {url}")
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Request failed with status code {response.status_code} for URL: {url}")
            return None

    def scrape_salons(self):
        page = 1
        while True:
            url = self.base_url if page == 1 else f"https://www.treatwell.de/orte/behandlung-gruppe-friseur/angebot-typ-lokal/in-{self.city}-de/seite-{page}/?view=list"
            soup = self.fetch_page(url)
            if soup:
                extractor = SalonNameExtractor(soup)
                salon_names = extractor.extract_salon_names()
                if salon_names:
                    self.salon_names.extend(salon_names)
                    print(f"Found {len(salon_names)} salons on page {page}.")
                    page += 1  # Move to the next page
                else:
                    print(f"No more salons found on page {page}. Stopping.")
                    break
            else:
                print("Failed to fetch the page or encountered an error. Stopping.")
                break

    def save_to_txt(self):
        folder_path = 'salon_names'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        filename = f"{self.city}_salons.txt"
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'w', encoding='utf-8') as txt_file:
            for name in self.salon_names:
                txt_file.write(name + '\n')
        print(f"Salon names saved to {file_path}")

# if __name__ == "__main__":
#     city_input = input("Enter the city (e.g., Berlin): ")
#     scraper = SalonScraper(city_input)
#     scraper.scrape_salons()
#     scraper.save_to_txt()
