import requests
from bs4 import BeautifulSoup
import re
import openai
from dotenv import load_dotenv
import os
from app.models.response import Response
from app.state import scraped_data

# Funktsioon, kus asuvad teksti puhastamise meetodid
def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Funktsioon, mis eraldab teksti veebilehelt
def scrape_page(url):
    # Laeb veebilehe ja seab selle kodeeringu
    response = requests.get(url)
    response.encoding = 'utf-8'
    # Veebilehe ümbertöötlemine
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

    # HTML elementide klassid, mida ei soovi tekstis. Peamiselt menüü ja muude nupude pealkirjad. Need elemendid eemaldatakse.
    exclude_classes = ["elementor-button-text", "menu-link", "ai-booking-button", "screen-reader-text", 
                       "wpcf7-list-item-label","ast-footer-copyright", "ai-booking-overlay"]
    for exclude_class in exclude_classes:
        for element in soup.find_all(class_=exclude_class):
            element.decompose()

    # Eraldab teksti veebilehelt
    content = soup.get_text(separator=" ").strip()
    # Puhastab teksti
    content = clean_text(content)
    
    return content

# Funktsioon, mis kogub veebilehelt lingid, mis on seotud antud URL-iga
def crawl_links(url):
    # Laeb veebilehe ja seab selle kodeeringu
    response = requests.get(url)
    response.encoding = 'utf-8'
    # Veebilehe ümbertöötlemine
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Leiab kõik lingid, mis on seotud antud URL-iga
    links = []
    for link in soup.find_all('a', href=True):
        if str(link['href']).startswith(str(url)):
            links.append(link['href'])
    return links

# Funktsioon, mis kogub veebilehelt andmed, kasutades scrape_page ja crawl_links funktsioone
def scrape_site(url):
    results = {} # Lehtedelt kogutud andmed
    visited_pages = set() # Külastatud lehed

    # Rekursiivne funktsioon, mis kogub andmeid ja käib läbi lehtedel olevad lingid, mis on seotud antud URL-iga
    def scrape_and_crawl(current_url):
        if current_url in visited_pages: # Kontrollib, kas lehte  on juba külastatud lehtede hulgas
            return
        visited_pages.add(current_url) # Lisab lehe külastatud lehtede hulka
        page_data = scrape_page(current_url) # Eraldab info praeguselt lehelt
        results[current_url] = page_data # Lisab info tulemuste hulka

        # Otsib alamlehtede URL-e ja käib neid läbi
        subpage_urls = crawl_links(current_url)
        for subpage_url in subpage_urls:
            scrape_and_crawl(subpage_url)

    # Pealehel oleva info kogumine ja alamlehtede läbimine
    scrape_and_crawl(url)
    
    return results

# Funktsioon, mis kasutab OpenAI API gpt-4o-mini mudelit, et vastata kasutaja küsimusele
def openAI_query(question):
    load_dotenv() # Laeb .env failist keskkonnamuutujad, kus on salvestatud OpenAI API võti
    data = scraped_data # Veebilehelt kogutud andmed, mis on salvestatud globaalsesse muutujasse scraped_data

    # Süsteemi sõnum, mis antakse OpenAI API-le koos kasutaja küsimusega, mis seab, kuidas mudel peaks vastama.
    system_message = ("Oled assistent, kes analüüsib veebilehelt kogutuid andmeid, mis on ette antud ja vastab küsimustele ainult nende andmete põhjal." 
                      "Andmed on formaadis {'url1': 'lehe info', 'url2:'lehe info'} ning vastuse leidmisel, lisa sellega seotud URL-id 'sources' väljale."
                      "Kui andmed puuduvad, siis vastad 'Andmed puuduvad' ja jäta 'sources' väli tühjaks."
                      "'usage' välja lisa 'inputTokens' ja 'outputTokens' väärtused, mis näitavad vastavalt vastuse genereerimiseks kulunud sisendtokenite ja väljundtokenite hulka.")

    client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Veebilehelt kogutud andmed:\n{data}\n\nKüsimus: {question}"}],
            response_format=Response, # Vastuse formaat, mis on määratud Response klassis
            max_tokens=16384 #Maksimum tokenite arv. 1 token on umbes 4 tähemärki ja gpt-4o-mini puhul on maksimaalne tokenite arv 16384, samas kui 200 000 tähemärgi puhul oleks see umbes 50 000 tokenit
            
    )
    return response.choices[0].message.parsed