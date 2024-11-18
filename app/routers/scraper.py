from fastapi import APIRouter, HTTPException, Request
from app.scraper import scrape_site, openAI_query

router = APIRouter()

# Endpoint, mis kraabib ühelt veebilehelt andmed ja tagastab need JSON formaadis
@router.get("/scrape/")
def scrape(url: str):
    try:
        url = url.strip()
        result = scrape_site(url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint, mis kasutab OpenAI API gpt-4o-mini mudelit, et vastata kasutaja küsimusele ja tagastab vastuse JSON formaadis
@router.post("/ask/")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question")
    if not question:
        raise HTTPException(
            status_code=400, 
            detail="Question field is required and needs to be filled"
        )
    try:
        result = openAI_query(question.strip())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
