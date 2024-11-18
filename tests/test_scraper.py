import pytest
from app.scraper import scrape_page, crawl_links, scrape_site
@pytest.fixture
def sample_url():
    return "https://tehisintellekt.ee/"

@pytest.fixture
def sample_content():
    return "Arendame generatiivse AI lahendusi, mis on integreeritud ettevõtte andmete ja tarkvaradega. Üle 14 aasta kogemust turvaliste ja usaldusväärsete AI-lahenduste loomisega."

def test_scrape_page(sample_url, sample_content):
    result = scrape_page(sample_url)
    assert sample_content in result

def test_crawl_links(sample_url):
    links = crawl_links(sample_url)
    expected_urls = [
        "https://tehisintellekt.ee/",
        "https://tehisintellekt.ee/tehisintellekt/",
        "https://tehisintellekt.ee/artiklid/",
        "https://tehisintellekt.ee/liitu-meiega/"
    ]
    for url in expected_urls:
        assert url in links

def test_scrape_site(sample_url, sample_content):
    results = scrape_site(sample_url)
    assert isinstance(results, dict)
    assert sample_url in results
    assert sample_content in results[sample_url]