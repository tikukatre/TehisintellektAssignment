from app.routers import scraper
from app.scraper import scrape_site
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.state import scraped_data 

#Rakenduse elutsükli haldamine
@asynccontextmanager
async def lifespan(app: FastAPI):
    #Seab globaalse muutuja scraped_data ja uuendab seda
    global scraped_data 
    scraped_data.update(scrape_site("https://tehisintellekt.ee"))
    yield
    #Puhastab scraped_data muutuja
    scraped_data.clear()

#Rakenduse loomine
app = FastAPI(lifespan=lifespan)

#Lisab scraper.py endpointid
app.include_router(scraper.router)

#Endpoint, mis tagastab tehisintellekt.ee ja selle alamlehtedelt kraabitud andmed
@app.get("/source_info")
def get_scraped_data():
    return scraped_data