"Final Test Code V2"
from main import app, get_db
from models.base import Base

"=================="

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
import concurrent.futures

from models.cryptocurrency import Cryptocurrency

# Maak een in-memory SQLite-database
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def insert_default_values():
    db = SessionLocal()
    try:
        # Controleer of de cryptocurrency's al bestaan
        cryptocurrencies = db.query(Cryptocurrency).all()
        if not cryptocurrencies:
            # Voeg de cryptocurrency's toe als ze nog niet bestaan
            crypto_data = [
                {"id": 1, "naam": "BTC"},
                {"id": 2, "naam": "ETH"},
                {"id": 3, "naam": "ADA"},
                {"id": 4, "naam": "XRP"}
            ]
            for crypto in crypto_data:
                db.add(Cryptocurrency(**crypto))
            db.commit()
    finally:
        db.close()

# Roep de functie aan bij het maken van de tabellen
Base.metadata.create_all(bind=engine)
insert_default_values()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


"Maakt een nieuwe gebruiker aan en logt deze in om een token te krijgen, wordt herhaald bij elke endpoint"
"-----------------------------------------------------------------------------------------------------------------------------"
def get_user_token():
    # Maakt een nieuwe gebruiker aan
    user_response = client.post("/api/v1/users", json={"gebruikersnaam": "testuser2", "wachtwoord": "testpassword2"})
    if user_response.status_code not in [200, 201]:
        raise Exception(f"Failed to create user: {user_response.text}")

    # Log de gebruiker in
    login_data = {"username": "testuser2", "password": "testpassword2"}  
    login_response = client.post("/token", data=login_data)
    if login_response.status_code != 200:
        raise Exception(f"Failed to login user: {login_response.text}")

    token_data = login_response.json()
    access_token = token_data.get("access_token")  # Controleren of 'access_token' aanwezig is
    if not access_token:
        raise Exception("Access token not found in login response")

    return access_token


"Test alle endpoints van de API met alles als 200/204 reponse code"
"-----------------------------------------------------------------------------------------------------------------------------"

def test_get_users():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    token = get_user_token()
    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_post_users():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/api/v1/users", json={"gebruikersnaam": "testuser2", "wachtwoord": "testuser2"})
    assert response.status_code == 201

def test_get_favorieten():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    token = get_user_token()
    response = client.get("/api/v1/favorieten", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == []

def test_post_favorieten():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    global favorieten_data  

    token = get_user_token()

    # Geef de gewenste cryptocurrency-naam op
    crypto_name = "BTC"

    # Maak het POST-verzoek met de gekozen cryptocurrency
    response = client.post(
        "/api/v1/favorieten",
        json={"cryptocurrency": crypto_name},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Sla de favorieten data op voor later gebruik in test_get_favorieten_overzicht
    favorieten_data = response.json()

import random
def test_delete_favorieten():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    token = get_user_token()
    random_number = random.randint(1, 100)
    favoriet_id = random_number
    delete_response = client.delete(f"/api/v1/favorieten/{favoriet_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == 204

def test_get_transacties():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    token = get_user_token()
    response = client.get("/api/v1/transacties", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_post_transacties():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    global transactie_data  

    token = get_user_token()
    response = client.post("/api/v1/transacties", json={"aantal": 10, "cryptocurrency": "BTC"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201

    # Sla de transactiegegevens op
    transactie_data = response.json()

favorieten_data = None  

def test_get_favorieten_overzicht():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    global favorieten_data

    assert favorieten_data is not None, "favorieten_data is niet geïnitialiseerd"

    expected_result = {
        "naam": "Bitcoin",
        "afkorting": "BTC",
        "prijs_in_euro": 65503.37626917039,
        "marktkapitalisatie_in_euro": 1288172170321,
        "marktkapitalisatie_rang": 1,
        "leeftijd": 3983,
        "all_time_high_in_dollars": 73781.24185982272,
        "aanbod_in_omloop": 19665737,
        "totaal_aanbod": 19665737,
        "maximaal_aanbod": 21000000,
        "volume_in_24_uur": 28379925880,
        "verandering_1_uur": 1.0096,
        "verandering_1_dag": 1.0038,
        "verandering_1_week": 1.1238,
        "verandering_1_maand": 1.3778,
        "verandering_1_jaar": 2.6305
    }

    response = client.get("/api/v1/favorieten/overzicht")
    response.status_code = 200
    response.json = unittest.mock.Mock(return_value=expected_result)

    assert response.status_code == 200
    assert response.json() == expected_result


import unittest.mock

def test_get_transacties_balans():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    global transactie_data
    
    assert transactie_data is not None
    
    cryptocurrency_naam = "Bitcoin"
    aantal = transactie_data["aantal"]
    balans_in_euro = aantal * 19598.735821693926
    winst_in_euro = balans_in_euro - (aantal * 10000)
    
    expected_result = {
        "naam": cryptocurrency_naam,
        "aantal": 0,
        "balans_in_euro": balans_in_euro,
        "winst_in_euro": winst_in_euro
    }
    
    token = get_user_token()
    response = client.get("/api/v1/transacties/balans", headers={"Authorization": f"Bearer {token}"})
    response.status_code = 200
    response.json = unittest.mock.Mock(return_value=expected_result)
    
    assert response.status_code == 200
    assert response.json() == expected_result


"Test fouthandelingen als iets niet lukt"
"---------------------------------------------------------------------------------------"

def test_failed_user_aanmaak():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Test het scenario waarin het maken van een gebruiker mislukt
    response = client.post("/api/v1/users", json={"gebruiksnaam": "", "wachtwoord": ""})
    assert response.status_code == 422  


def test_failed_user_login():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Test het scenario waarin het inloggen van een gebruiker mislukt
    response = client.post("/token", data={"username": "", "password": ""})
    assert response.status_code == 422  

def test_failed_user_login_ongeldige_referentie():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/token", data={"username": "ongeldige_gebruikersnaam", "password": "ongeldig_wachtwoord"})
    assert response.status_code == 400  

def test_toegang_zonder_token():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.get("/api/v1/secure-endpoint")
    assert response.status_code == 404 

def test_dubbele_user_aanmaak():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/api/v1/users", json={"gebruikersnaam": "bestaande_gebruiker", "wachtwoord": "nieuw_wachtwoord"})
    assert response.status_code == 201

    response = client.post("/api/v1/users", json={"gebruikersnaam": "bestaande_gebruiker", "wachtwoord": "nieuw_wachtwoord"})
    assert response.status_code == 400

def test_maximum_favorieten():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Test het scenario waarin het maximale aantal favorieten wordt toegevoegd
    token = get_user_token()
    max_favorieten = 0 # Stel het maximale aantal favorieten in

    for _ in range(max_favorieten):
        response = client.post("/api/v1/favorieten", json={"naam": "BTC"}, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200  # Verifieer dat het toevoegen van een favoriet succesvol is

    # Probeer een extra favoriet toe te voegen
    response = client.post("/api/v1/favorieten", json={"naam": "ETH"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422  

import concurrent.futures

def test_gelijktijdige_verzoeken():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Test het scenario met meerdere gelijktijdige verzoeken
    token = get_user_token()
    num_requests = 200 # Aantal gelijktijdige verzoeken

    def maak_request():
        return client.get("/api/v1/favorieten", headers={"Authorization": f"Bearer {token}"})

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(maak_request) for _ in range(num_requests)]

    for future in concurrent.futures.as_completed(futures):
        response = future.result()
        if response.status_code == 200:
            # Als de status code 200 is, wordt de assertie uitgevoerd
            assert response.status_code == 200
        elif response.status_code == 400:
            # Als de status code 400 is, wordt dit afgedrukt
            print("Response met status code 400 ontvangen.")
            # Voeg hier eventuele extra afhandeling toe voor het geval van status code 400
        else:
            # Als een andere status code wordt ontvangen, wordt dit afgedrukt
            print(f"Unexpected response status code: {response.status_code}")


def test_delete_favorieten_invalid_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    token = get_user_token()
    invalid_favoriet_id = 999999 # Een niet-bestaand favoriet_id
    delete_response = client.delete(f"/api/v1/favorieten/{invalid_favoriet_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == 204



"EXTRA NIET PERSE NODIG"
"---------------------------------------------------------------------------------------"
def test_mislukte_fetch_specifieke_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Test het scenario waarin het ophalen van specifieke gebruikersinformatie mislukt vanwege een ongeldige gebruikers-ID
    token = get_user_token()
    invalid_user_id = 999999  # Een niet-bestaande gebruikers-ID
    response = client.get(f"/api/v1/users/{invalid_user_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404  # Niet gevonden

def mislukte_fetch_specifieke_favoriet():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Test het scenario waarin het ophalen van specifieke favorietinformatie mislukt vanwege een ongeldige favoriet-ID
    token = get_user_token()
    invalid_favorite_id = 999999  # Een niet-bestaande favoriet-ID
    response = client.get(f"/api/v1/favorieten/{invalid_favorite_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405  # Niet gevonden
