# ausführen mit: scrapy crawl homegate -o file.jl
import scrapy
import subprocess
import os

class HomegateSpider(scrapy.Spider):
    name = 'homegate'
    
    def start_requests(self):
        with open('homegate_numbers.txt', 'r') as file:
            urls = [url.strip() for url in file.readlines()]
        self.logger.info(f"Total URLs read from file: {len(urls)}")
    
        for url in urls:
            self.logger.info(f"Requesting URL: {url}")
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        # Extrahiere die Miete, Anzahl Zimmer, Stock und Wohnfläche
        rent = response.css('div.SpotlightAttributesPrice_value_TqKGz span:nth-child(2)::text').get()
        rooms = response.css('div.SpotlightAttributesNumberOfRooms_value_TUMrd::text').get()
        floor = response.css('div.CoreAttributes_coreAttributes_e2NAm dd::text')[3].get()
        living_space = response.css('div.SpotlightAttributesUsableSpace_value_cpfrh::text').get()
        
        # Überprüfe, ob alle relevanten Daten vorhanden sind
        if rent and rooms and floor and living_space:
            yield {
                'title': response.css('h1.ListingTitle_spotlightTitle_ENVSi::text').get().strip(),
                'rent': rent.strip(),
                'rooms': rooms.strip(),
                'floor': floor.strip(),
                'living_space': living_space.strip(),
                'address': response.css('address.AddressDetails_address_i3koO span::text').getall(),
                'available_from': response.css('div.CoreAttributes_coreAttributes_e2NAm dd::text').getall()[0].strip(),
                'type': response.css('div.CoreAttributes_coreAttributes_e2NAm dd::text').getall()[1].strip(),
                'year_built': response.css('div.CoreAttributes_coreAttributes_e2NAm dd::text').getall()[5].strip(),
                'listing_id': response.css('dl.ListingTechReferences_techReferencesList_jlZwL dd::text').getall()[0].strip(),
                'object_ref': response.css('dl.ListingTechReferences_techReferencesList_jlZwL dd::text').getall()[1].strip(),
                'description': response.css('div.Description_descriptionBody_AYyuy p::text').getall(),
            }
            
    def closed(self, reason):
        # Dies wird aufgerufen, wenn der Spider beendet ist
        self.cleanup()

    def cleanup(self):
        current_directory = os.path.dirname(__file__)
        cleanup_script_path = os.path.join(current_directory, "..", "cleanup.py")
        subprocess.run(["python", cleanup_script_path])
