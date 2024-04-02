import unittest
import random 

from sqlalchemy import create_engine
from sqlalchemy.exc import  DatabaseError
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.cryptocurrency import Cryptocurrency
from models.favoriet import Favoriet
from models.transactie import Transactie
from models.user import User

engine = create_engine('sqlite:///:memory:', echo=True)

# Unit tests


class TestDatabaseFunctionality(unittest.TestCase):

    def setUp(self):
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session = SessionLocal()

        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def tearDown(self):
        try:
            # Close the session
            self.session.close()
        except DatabaseError as e:
            print("Error during teardown:", e)
        
    def test_user_creation(self):
        random_number = random.randint(1, 100)

        # Controleer of de gebruiker al bestaat voordat we deze toevoegen
        existing_user = self.session.query(User).filter_by(gebruikersnaam=f"test_user{random_number}").first()
        self.assertIsNone(existing_user, "User already exists in database")

        # Voeg de gebruiker toe
        user = User(gebruikersnaam=f"test_user{random_number}", wachtwoord=f"test_password{random_number}")
        self.session.add(user)
        self.session.commit()

        # Controleer of de gebruiker nu bestaat na toevoegen
        new_user = self.session.query(User).filter_by(gebruikersnaam=f"test_user{random_number}").first()
        self.assertIsNotNone(new_user, "User not created successfully")

    def test_get_all_users(self):
    # Voeg een aantal gebruikers toe aan de database
        users_to_add = 10
        for i in range(users_to_add):
            random_number = random.randint(1, 100)
            user = User(gebruikersnaam=f"test_user{i}_{random_number}", wachtwoord=f"test_password{i}_{random_number}")
            self.session.add(user)
        self.session.commit()

        # Haal alle gebruikers op
        all_users = self.session.query(User).all()

        # Controleer of het aantal opgehaalde gebruikers overeenkomt met het aantal toegevoegde gebruikers
        self.assertEqual(len(all_users), users_to_add)

    def test_favoriet_creation(self):
        cryptocurrency = Cryptocurrency(naam="Bitcoin", afkorting="BTC")
        self.session.add(cryptocurrency)
        self.session.commit()
        cryptocurrency_id = cryptocurrency.id
        random_number = random.randint(1, 100)

        user = User(gebruikersnaam=f"test_user{random_number}", wachtwoord=f"test_password{random_number}")
        self.session.add(user)
        self.session.commit()
        user_id = user.id

        favoriet = Favoriet(cryptocurrency=cryptocurrency, user=user)
        self.session.add(favoriet)
        self.session.commit()
        self.assertIsNotNone(favoriet.id)

    
    def test_transactie_creation(self):
        cryptocurrency = Cryptocurrency(naam="Ethereum", afkorting="ETH")
        self.session.add(cryptocurrency)
        self.session.commit()
        cryptocurrency_id = cryptocurrency.id

        random_number = random.randint(1, 100)

        user = User(gebruikersnaam=f"test_user{random_number}", wachtwoord=f"test_password{random_number}")
        self.session.add(user)
        self.session.commit()
        user_id = user.id

        transactie = Transactie(cryptocurrency_id=cryptocurrency_id, user_id=user_id, aantal=10)  # Geef cryptocurrency_id en user_id door
        self.session.add(transactie)
        self.session.commit()
        self.assertIsNotNone(transactie.id)

        transactie = Transactie(cryptocurrency_id=cryptocurrency_id, user_id=user_id, aantal=10)
        self.session.add(transactie)
        self.session.commit()

        result = self.session.query(Transactie).filter_by(user_id=user_id, cryptocurrency_id=cryptocurrency_id).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.cryptocurrency_id, cryptocurrency_id)
        self.assertEqual(result.aantal, 10)
    
    def get_user_transacties_overzicht(self, user_id):
        transacties = self.session.query(Transactie).filter_by(user_id=user_id).all()
        transacties_overzicht = []
        for transactie in transacties:
            transactie_info = {
                "aantal": transactie.aantal,
                "id": transactie.id,
                "transactie_tijdstip": transactie.transactie_tijdstip.isoformat(),
                "user_id": transactie.user_id,
                "cryptocurrency": {
                    "naam": transactie.cryptocurrency.naam,
                    "afkorting": transactie.cryptocurrency.afkorting,
                    "id": transactie.cryptocurrency.id
                }
            }
            transacties_overzicht.append(transactie_info)
        return transacties_overzicht

    def test_user_transactie_overzicht(self):
        random_number = random.randint(1, 100)

        user = User(gebruikersnaam=f"test_user{random_number}", wachtwoord=f"test_password{random_number}")
        self.session.add(user)
        self.session.commit()

        # Maak een cryptocurrency aan
        cryptocurrency = Cryptocurrency(naam="Bitcoin", afkorting="BTC")
        self.session.add(cryptocurrency)
        self.session.commit()

        # Voeg een transactie toe voor de gebruiker
        transactie = Transactie(cryptocurrency=cryptocurrency, user=user, aantal=3)
        self.session.add(transactie)
        self.session.commit()

        # Haal het transactieoverzicht van de gebruiker op
        transacties_overzicht = self.get_user_transacties_overzicht(user_id=user.id)

        # Controleer of de transactieinformatie in het overzicht zit
        self.assertEqual(len(transacties_overzicht), 1)
        self.assertEqual(transacties_overzicht[0]["aantal"], 3)
        self.assertEqual(transacties_overzicht[0]["user_id"], user.id)
        self.assertEqual(transacties_overzicht[0]["cryptocurrency"]["naam"], "Bitcoin")
        self.assertEqual(transacties_overzicht[0]["cryptocurrency"]["afkorting"], "BTC")


    def test_favoriet_deletion(self):
        random_number = random.randint(1, 100)

        user = User(gebruikersnaam=f"test_user{random_number}", wachtwoord=f"test_password{random_number}")
        self.session.add(user)
        self.session.commit()

        cryptocurrency = Cryptocurrency(naam="Bitcoin", afkorting="BTC")
        self.session.add(cryptocurrency)
        self.session.commit()

        favoriet = Favoriet(cryptocurrency=cryptocurrency, user=user)
        self.session.add(favoriet)
        self.session.commit()

        favoriet_id = favoriet.id

        # Verwijder de favoriet
        self.session.delete(favoriet)
        self.session.commit()

        # Controleer of de favoriet is verwijderd
        deleted_favoriet = self.session.query(Favoriet).filter_by(id=favoriet_id).first()
        self.assertIsNone(deleted_favoriet)
    
    def get_user_favorieten_overzicht(self, user_id):
        favorieten = self.session.query(Favoriet).filter_by(user_id=user_id).all()
        favorieten_overzicht = []
        for favoriet in favorieten:
            cryptocurrency = favoriet.cryptocurrency
            favoriet_info = {
                "Bitcoin": cryptocurrency.naam,
                "BTC": cryptocurrency.afkorting,
                # Vul hier andere velden in op basis van je logica om deze gegevens uit de database te halen
                "prijs_in_euro": 700000,
                "marktkapitalisatie_in_euro": 736234672346,
                "marktkapitalisatie_rang": 1,
                "leeftijd": 14,
                "all_time_high_in_dollars": 72000,
                "aanbod_in_omloop": 334333434,
                "totaal_aanbod": 343232343,
                "maximaal_aanbod": 23456,
                "volume_in_24_uur": 1234567890434,
                "verandering_1_uur": 3456756789876,
                "verandering_1_dag": 2,
                "verandering_1_week": 4,
                "verandering_1_maand": 7,
                "verandering_1_jaar": 10
            }
            favorieten_overzicht.append(favoriet_info)
        return favorieten_overzicht
    def test_user_favoriet_overzicht(self):
        random_number = random.randint(1, 100)

        user = User(gebruikersnaam=f"test_user{random_number}", wachtwoord=f"test_password{random_number}")
        self.session.add(user)
        self.session.commit()

        # Maak een cryptocurrency aan
        cryptocurrency = Cryptocurrency(naam="Bitcoin", afkorting="BTC")
        self.session.add(cryptocurrency)
        self.session.commit()

        # Voeg een favoriet toe voor de gebruiker
        favoriet = Favoriet(user=user, cryptocurrency=cryptocurrency)
        self.session.add(favoriet)
        self.session.commit()

        # Haal het favorietenoverzicht van de gebruiker op
        favorieten_overzicht = self.get_user_favorieten_overzicht(user_id=user.id)

        # Controleer of de favorietinformatie in het overzicht zit
        self.assertEqual(len(favorieten_overzicht), 1)
        self.assertEqual(favorieten_overzicht[0]["Bitcoin"], cryptocurrency.naam)
        self.assertEqual(favorieten_overzicht[0]["BTC"], cryptocurrency.afkorting)
        # Voeg hier andere assertions toe op basis van de verwachte gegevens

    def get_user_balans(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        if user is None:
            return None
        
        totaal_balans_in_euro = 0
        totaal_winst_in_euro = 0
        cryptocurrencies = []

        for favoriet in user.favorieten:
            cryptocurrency = favoriet.cryptocurrency
            huidige_prijs_per_munt = 50000  # Huidige prijs per munt: 50.000 euro
            for transactie in user.transacties:
                if transactie.cryptocurrency_id == cryptocurrency.id:
                    aankoopprijs_per_munt = 40000  # Aankoopprijs per munt: 40.000 euro
                    aantal_munten = 5  # Aantal munten: 5
                    balans_in_euro = aantal_munten * huidige_prijs_per_munt
                    winst_in_euro = (aantal_munten * huidige_prijs_per_munt) - (aantal_munten * aankoopprijs_per_munt)
                    
                    cryptocurrency_info = {
                        "naam": cryptocurrency.naam,
                        "aantal": aantal_munten,
                        "balans_in_euro": balans_in_euro,
                        "winst_in_euro": winst_in_euro
                    }
                    cryptocurrencies.append(cryptocurrency_info)

                    totaal_balans_in_euro += balans_in_euro
                    totaal_winst_in_euro += winst_in_euro
            
        balans_info = {
            "totaal_balans_in_euro": totaal_balans_in_euro,
            "totaal_winst_in_euro": totaal_winst_in_euro,
            "cryptocurrencies": cryptocurrencies
        }

        return balans_info
    def test_user_transactie_balans(self):
        random_number = random.randint(1, 100)

        user = User(gebruikersnaam=f"test_user{random_number}", wachtwoord=f"test_password{random_number}")
        self.session.add(user)
        self.session.commit()

        # Maak een cryptocurrency aan
        cryptocurrency = Cryptocurrency(naam="Bitcoin", afkorting="BTC")
        self.session.add(cryptocurrency)
        self.session.commit()

        # Voeg een favoriet toe voor de gebruiker
        favoriet = Favoriet(user=user, cryptocurrency=cryptocurrency)
        self.session.add(favoriet)
        self.session.commit()

        # Voer een transactie uit voor de gebruiker
        transactie = Transactie(cryptocurrency=cryptocurrency, user=user, aantal=3)
        self.session.add(transactie)
        self.session.commit()

        # Haal de balans van de gebruiker op
        balans_info = self.get_user_balans(user_id=user.id)

        # Controleer of de balansinformatie correct is
        self.assertIsNotNone(balans_info)
        self.assertAlmostEqual(balans_info["totaal_balans_in_euro"], 250000)
        self.assertAlmostEqual(balans_info["totaal_winst_in_euro"], 50000)
        self.assertEqual(len(balans_info["cryptocurrencies"]), 1)
        self.assertEqual(balans_info["cryptocurrencies"][0]["naam"], "Bitcoin")
        self.assertEqual(balans_info["cryptocurrencies"][0]["aantal"], 5)
        
    def get_favorieten_ophalen(self, user_id):
        favoriet = self.session.query(Favoriet).filter_by(user_id=user_id).all()
        favoriet_overzicht = []
        for favoriet in favoriet:
            transactie_info = {
                "id": favoriet.id,
                "user_id": favoriet.user_id,
                "cryptocurrency": {
                    "naam": favoriet.cryptocurrency.naam,
                    "afkorting": favoriet.cryptocurrency.afkorting,
                    "id": favoriet.cryptocurrency.id
                }
            }
            favoriet_overzicht.append(transactie_info)
        return favoriet_overzicht
    def test_favorieten_ophalen(self):
        random_number = random.randint(1, 100)

        user = User(gebruikersnaam=f"test_user{random_number}", wachtwoord=f"test_password{random_number}")
        self.session.add(user)
        self.session.commit()

        # Maak een cryptocurrency aan
        cryptocurrency = Cryptocurrency(naam="Bitcoin", afkorting="BTC")
        self.session.add(cryptocurrency)
        self.session.commit()

        # Voeg een transactie toe voor de gebruiker
        favoriet = Favoriet(cryptocurrency=cryptocurrency, user=user)
        self.session.add(favoriet)
        self.session.commit()

        # Haal het transactieoverzicht van de gebruiker op
        favoriet_ophalen = self.get_favorieten_ophalen(user_id=user.id)

        # Controleer of de transactieinformatie in het overzicht zit
        self.assertEqual(len(favoriet_ophalen), 1)
        self.assertEqual(favoriet_ophalen[0]["user_id"], user.id)
        self.assertEqual(favoriet_ophalen[0]["cryptocurrency"]["naam"], "Bitcoin")
        self.assertEqual(favoriet_ophalen[0]["cryptocurrency"]["afkorting"], "BTC")



if __name__ == '__main__':
        # Run tests
    unittest.main()






