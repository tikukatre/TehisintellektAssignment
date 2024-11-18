# Tehisintellekt Backend arendaja proovitöö

## Rakenduse käivitamine

### Eeltingimused

- Docker ja Docker Compose peavad olema installitud. (Kui Dockeri kaudu käivitada)
- OpenAI API võti peab olema saadaval.

### Keskkonnamuutujate seadistamine

1. Loo `.env` fail sarnaselt `.env-example` failile.
2. Lisa oma OpenAI API võti `.env` faili

### Docker compose abil rakenduse käivitamine

```sh
docker-compose up --build
```
Rakendus on saadaval http://127.0.0.1:8000

### Dockeri abil ühiktestide käivitamine

```sh
docker-compose run --rm test
```

### Rakenduse käivitamine lokaalselt
Peab olema olemas Python 
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Rakendus on saadaval http://127.0.0.1:8000

### API endpointid
* GET /source_info: Tagastab tehisintellekt.ee ja selle alamlehtedelt kraabitud andmed.
* GET /scrape/?url={url}: Kraabib andmed antud URL-ilt ja tema alamlehtedelt
* POST /ask/: Kasutab OpenAI API-t, et vastata kasutaja küsimusele. Requestiga kaasa tuleb anda JSON, kus on väli "question" täidetud.
```json
{
  "question": "Kes on Tehisintellekt võtmeisikud?"
}
```
### Rakenduse tööpõhimõte
Rakendus alustamisel eraldab **scrape_site("https://tehisintellekt.ee")** funktsioon tekst info tehisintellekt.ee veebilehelt ja selle alamlehtedel. Peale seda saab kasutada **GET /source_info** endpointi, et näha kogu saadud infot ning samuti saab ka kasutada **POST /ask** enpointi, mille kaudu saab kasutaja oma küsimuse esitada formaadis:
```json
{
  "question": "Kasutaja küsimus"
}
```
Endpoint kasutab **openAI_query("Kasutaja küsimus")** , kus antakse globaalse **scrape_data** muutuja abil edasi rakenduse käivitamisel eraldatud info ja antakse see edasi OpenAI mudelile koos juhendiga, kuidas ja mille põhjal peab see küsimusele vastama. Kasutajale tagastatakse siis vastus formaadis: 
```json
{
    "user_question": "Kes on andmeteadus OÜ tegevjuht?",
    "answer": "Andmeteadus OÜ tegevjuht on Kristjan Eljand.",
    "usage": [
        {
            "inputTokens": 8,
            "outputTokens": 11
        }
    ],
    "sources": "['https://tehisintellekt.ee']"
}
```
Kui edastatud infos pole infot küsimusele vastamiseks, siis vastuse väljas vastuseks antakse, et "Andmed puuduvad"

Rakendusel on ka Endpoint **GET /scrape/?url={url}**, mille kaudu saab eraldada antud URL-iga lehelt ja selle alamlehtedelt info. See Endpoint on pigem mõeldud, testimiseks, kas tekst info eraldamine töötab. 

### Kasutatud package-id

* fastapi - Rakenduse loomine, see on kiire ja lihtne veebiraamisik, mis võimaldab luua RESTful API-sid, mida oli ka Endpointide loomiseks vaja. 

* beautifulsoup4 - HTML lehekülje parimiseks ja töötlemiseks. Selle package abil sain eraldada veebilehtedelt, tekst info ning kuna sellega on töö tehtud üsna lihtsaks, siis ei pidanud ka väga teksti puhastamisega vaeva nägema.

* requests - HTTP päringute tegemine. Sellega saime kätte näiteks veebilehe, et siis seda BeautifulSoup abil töödelda.

* pydantic - Andme mudelite loomine. Kasutasin seda OpenAI mudeli vastuse kuju loomiseks. Kuid see on hea ka andmete valideerimiseks ja kasulik FastAPI Enpointide puhul kasutamiseks, et määrata ja valideerida päringute ja vastuste mudelid. 

* OpenAI - OpenAI API kasutamine. See on kasutusel tehisintellekti abil vastuse genereerimiseks.

* python-dotenv - Keskkonnamuutujate laadimine .env failis. Kuna meil on vaja OpenAI API võtit, siis lisasime selle  .env faili, kuna pole ohutu, selliseid andmeid lihtsalt jätta koodi sisse. 

* uvicorn - ASGI serveri (asünkroone serveri) käivitamine, mida kasutatakse FastAPI rakenduste käivitamiseks.

* pytest - Ühiktestide loomine ja käivitamine


### Mis täiendusi teeksin, et rakendus oleks tootmiskõlbulik?

* Käiksin üle turvalisuse:
  * Keskonnamuutujad nagu OpenAI API võti turvaliselt hallatud
  * HTTPS kasutamine, et andmete edastamine oleks turvalisem
  * Kuna hetkel on tegemist avaliku info kasutamisega, siis autentimist ja autoriseerimist pole vaja, kuid kui "klient" peaks tahtma kasutada tundlike andmeid, siis tuleks need lisada.

* Tuleks lisada rakanduse töö logimine, et oleks kergem jälgida rakenduse tööd ja leida probleemi kohti või vigu.

* Tuleks implementeerida kõigile endpointidele pydanticu abil andme mudelid, et paremini valideerida päringuid. Samuti ka täiustada veakäsitlust, et tagada kasutajale rohkemate vigade puhul informatiivsed veateated.

* Lisada rohkem ühikteste ja integreerimisteste, et ka kontrollide komponentide omavahelist koostööd. 

* Tuleks luua CI/CD pipeline ja mille kaudu toimuks ka automatiseeritud testimine koodi muudatuste korral.

* Luua põhjalikum API dokumentatsioon, kas käsitsi või kasutades FastAPI docs võimalust.

* Võimalusel veel parandada koodi kvaliteeti.

* Täiustaksin "tehisintellekt.ee" lehelt info eraldamist ning otsiks veel üles mõned mure kohad ja parandaks ka teksti eraldamist vastavalt kliendi vajadusele. Hetkel võtsin BeautifulSoup abil lehtedelt kogu teksti ja mitte ainult <p> ehk paragraafi tähistuse sees oleva. Eemaldasin küll klassid, mille teksti ei tahtnud nagu menüü jne, aga näiteks igal leheküljel on kuskil peidus üks tekstiplokk tekstiga, mille klassi ei õnnestunud mul tuvastada: "IIZI kindlustusmaakleri vestlusrobot klienditeenindajatele Mure IIZI kindlustusmaakler vahendab paljude kindlustusfirmade pakkumisi. Kliendid helistavad ja kirjutavad pidevalt, et uurida kindlustustingimuste kohta. Sageli on tingimused pikad ja keerukad, mistõttu kulub klienditeenindajatel vajalike vastuste leidmiseks palju aega. IIZI kindlustusmaakleris töötab 30-40 klienditeenindajat. Lahendus Lõime vestlusroboti, mis analüüsib ja võrdleb kindlustusfirmade tingimusi ja leiab neist vajalikud punktid. Väärtus Klienditeenindajad ei pea enam pikki kindlustustingimusi rida-realt läbi töötama ja kliendid saavad kiiremini vastused." Oleks hea see koht leida ning seda tekstis mitte kaasa anda. Samuti täiendaksin ka alamlehtde läbimist vastavalt sellele, millised alamlehed tuleks ikkagi läbi käia. 




### Kuidas ehitaksin üles rakenduse CI/CD pipeline?

* Tuleks luua kaust *.github/workflows*  ja sinna luua *ci_cd_pipeline.yml* fail

* Fail näeks välja midagi sellist:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
      - test

jobs:
  build:
    runs-on: ubuntu-latest

    services:
      docker:
        image: docker:19.03.12
        options: --privileged
        ports:
          - 8000:8000

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10

      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          source venv/bin/activate
          pytest --maxfail=1 --disable-warnings

      - name: Build and run Docker container
        run: |
          docker-compose up --build -d

      - name: Deploy to Docker Hub
        if: github.ref == 'refs/heads/main'
        env:
          DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
          DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
        run: |
          echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
          docker-compose push

```
* GitHub repo sees tuleks minna Settings ning sealt Secrets and variables, et lisada Dockeri kasutajanimi ja parool.

* Tuleks üle käia ka docker_compose.yml ja vajadusel seda täiustada


### Kuidas püstitaksin rakenduse Azure keskkonnas?

Eeldades, et on olemas Azure kasutaja ja sisse logitud. 
* Tuleks kasutada Azure CLI-id ja luua uus Resource Group, App Service Plan ja siis Web App
* Saab üles seadistada Githubi kaudu rakenduse püstitamise.
* Tuleks seada ka keskkonnamuutujad.
* Teha kindlaks, et Dockerfile on sobiv 
* Muutes näiteks CI/CD pipeline ja lisades osad nagu:

```yaml
- name: Log in to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

- name: Deploy to Azure Web App
        run: |
          az webapp config container set --name myFastAPIApp --resource-group myResourceGroup --docker-custom-image-name mycontainerregistry.azurecr.io/myfastapiapp:latest
          az webapp config appsettings set --resource-group myResourceGroup --name myFastAPIApp --settings OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}

```
* Rakendus püstitatakse Azure pilvekeskkonda GitHub Actions abil CI/CD pipeline kaudu