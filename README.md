# TaxHub-api

Essaie de réécriture en flask de l'api de TaxHub.

Manque les routes :
 /taxonsattribut/{id}/{value}
 /bibtaxons/taxonomie
 /biblistes + toutes les autres routes


##Run serveur
./venv_flask/bin/python taxhubapi.py

##Run client

Pour le moment bidouille qui consiste à lié la partie angular du dépot TaxHub dans le dossier static

Pour faire fonctionner en test en localhost il faut copier le fichier constants.js.sample et le renommer constants.js.
Puis éditer le paramètre api_url avec la valeur suivante : "http://localhost:5000/",
