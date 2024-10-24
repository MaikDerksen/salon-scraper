class ServiceExtractor:
    def __init__(self, soup):
        self.soup = soup

    def extract_services(self):
        service_list = []
        service_items = self.soup.find_all('div', class_='MenuItem-module--menu-item--ddf3a1')

        for item in service_items:
            service_title = item.find('span', class_='Text-module_body__2lxF8 MenuItem-module--title--b45b8e')
            price_element = item.find("div", class_="PriceView-module--priceLabel--8a6d8e")
            strike_element = item.find("div", class_="PriceView-module--strikethroughPrice--f1ec60")
            strike_price = strike_element.find("s", class_="Text-module_body__2lxF8") if strike_element else None
            duration_element = item.find('span', class_='Text-module_body__2lxF8 MenuItem-module--durationRange--36a300')
            discount_element = item.find('span', class_='Text-module_body__2lxF8 PriceView-module--discountText--d6c0cd')

            if service_title:
                service_list.append({
                    'title': service_title.text.strip(),
                    'price': price_element.text.strip() if price_element else "No price found",
                    'strike': strike_price.text.strip() if strike_price else "N/A",
                    'duration': duration_element.text.strip() if duration_element else "No duration found",
                    'discount': discount_element.text.strip() if discount_element else "No discount"
                })

        return service_list
