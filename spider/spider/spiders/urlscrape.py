# ausführen mit: scrapy runspider urlscrape.py

import scrapy
import re
import os  # Stelle sicher, dass os importiert wird

class HomegateNumbersSpider(scrapy.Spider):
    name = 'homegate_numbers'
    allowed_domains = ['homegate.ch']
    start_page = 1
    max_pages = 10  # Maximalanzahl der zu durchlaufenden Seiten
    seen_urls = set()  # Set für bereits gesehene URLs

    def start_requests(self):
        yield scrapy.Request(url=f'https://www.homegate.ch/rent/real-estate/city-zurich/matching-list?page={self.start_page}', callback=self.parse)

    def parse(self, response):
        all_text = response.xpath('//body//text()').getall()
        combined_text = ' '.join(all_text)
        numbers = re.findall(r'\b4000\d{5,6}\b', combined_text)

        # Pfad zum aktuellen Skriptverzeichnis
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # Navigiere zwei Ebenen nach oben und dann in das Zielverzeichnis 'spider'
        target_dir = os.path.join(current_dir, '..', '..', 'homegate_numbers.txt')

        # Öffne die Datei am korrigierten Pfad zum Anhängen neuer URLs
        with open(target_dir, 'a') as file:  # Verwende hier target_dir statt 'homegate_numbers.txt'
            for number in numbers:
                url = f"https://www.homegate.ch/rent/{number}"
                if url not in self.seen_urls:
                    self.seen_urls.add(url)
                    file.write(url + '\n')
                    self.logger.info(f'Saved URL: {url}')

        current_page = int(response.url.split('page=')[-1])
        next_page = current_page + 1
        if next_page <= self.max_pages:
            next_page_url = f'https://www.homegate.ch/rent/real-estate/city-zurich/matching-list?page={next_page}'
            yield response.follow(next_page_url, self.parse)
