import requests

url = "http://localhost:4000/autocomplete"  # Modifier l'URL si nécessaire

headers = {
    "Content-Type": "application/json"  # Définir le type de contenu comme JSON
}

data = {
    "query": "A"  # Remplacez "votre_requete" par votre requête réelle
}

response = requests.get(url, headers=headers, json=data)

if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print("Erreur de réponse:", response.text)