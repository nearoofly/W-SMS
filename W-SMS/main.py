import csv
import os
from dotenv import load_dotenv
from twilio.rest import Client
from pyfiglet import Figlet

# Charger les variables d'environnement
load_dotenv()
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

# Initialisation Twilio
client = Client(account_sid, auth_token)

# Affichage ASCII
figlet = Figlet(font='slant')
print(figlet.renderText('W-SMS V1.1'))
print("🐄🌳 by Wharkly47\n")

def lire_contacts():
    with open('contacts.csv', newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def envoyer_message(contact, message):
    prenom = contact['prenom']
    numero = contact['telephone']
    corps = message.replace("{{prenom}}", prenom)
    try:
        client.messages.create(body=corps, from_=twilio_number, to=numero)
        print(f"✔️ SMS envoyé à {prenom} ({numero})")
    except Exception as e:
        print(f"❌ Erreur pour {prenom} ({numero}) : {e}")

def afficher_contacts():
    contacts = lire_contacts()
    for i, contact in enumerate(contacts):
        print(f"[{i+1}] {contact['prenom']} {contact['nom']} ({contact['telephone']})")

def ajouter_contact():
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    telephone = input("Téléphone (format +123...) : ")
    with open('contacts.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([nom, prenom, telephone])
    print("✅ Contact ajouté.")

def modifier_message():
    nouveau = input("Nouveau message (utilise {{prenom}} pour personnaliser) :\n> ")
    with open('messages/default.txt', 'w') as f:
        f.write(nouveau)
    print("✅ Message mis à jour.")

def envoyer_sms_selection():
    contacts = lire_contacts()
    afficher_contacts()
    selection = input("Sélectionne les contacts (ex: 1,3 ou 2-4) : ").replace(" ", "")
    indices = []
    for part in selection.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            indices.extend(range(start, end+1))
        else:
            indices.append(int(part))
    with open('messages/default.txt', 'r') as f:
        message = f.read()
    for i in indices:
        if 0 < i <= len(contacts):
            envoyer_message(contacts[i-1], message)

while True:
    print("\n[1] Envoyer une campagne SMS")
    print("[2] Modifier le message")
    print("[3] Voir les contacts")
    print("[4] Ajouter un contact")
    print("[5] Sélectionner contacts pour campagne")
    print("[6] Quitter")

    choix = input("Choix > ")
    if choix == "1":
        with open('messages/default.txt', 'r') as f:
            message = f.read()
        for contact in lire_contacts():
            envoyer_message(contact, message)
    elif choix == "2":
        modifier_message()
    elif choix == "3":
        afficher_contacts()
    elif choix == "4":
        ajouter_contact()
    elif choix == "5":
        envoyer_sms_selection()
    elif choix == "6":
        print("À bientôt 👋")
        break
    else:
        print("❌ Choix invalide.")
