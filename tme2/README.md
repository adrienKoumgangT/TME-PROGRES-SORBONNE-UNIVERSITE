# Exercice 1 - Expressions régulières

1. Utiliser les expressions régulières pour identifier les adresses gmails valides et les affichers
2. Utiliser les expressions régulières si une chaine caractères se termine par un chiffre.
3. Utiliser les expressions régulières pour supprimer les zéros problématiques 
dans une adresses IPv4 exprimée sous la forme d'une chaine de caractères.
4. utiliser les expressions régulières pour transformer une date au format
MM-DD-YYYY vers le format DD-MM-YYYY


# Exercice 2 - Analyser du XML

Ecrire un programme Python qui va:
1. Récupérer le contenu de la page à l'adresse [https//w3schools.com/xml/cd_catalog.xml]
2. Afficher pour les CD: le titre, l'artiste, le pays, la compagnie, l'année
3. Afficher tous les CD des années 1980
4. Afficher tous les CD anglais


# Exercice 3 - Analyser du JSON

Ecrire un programme Python qui va:
1. Récupérer le fichier de tournage à Paris à l'adresse:
[https://opendata.paris.fr/explore/dataset/lieux-de-tournage-a-paris/download/?format=json&timezone=Europe/Berlin&lang=fr]
2. Analyser le fichier JSON pour afficher, pour toutes les entrées:
le réalisateur, le titre, l'arrondissement, la date de début, la date de fin,
les coordonnées géographiques.
3. Afficher pour chaque film (il peut y avoir plusieurs entrées pour un
meme film) le réalisateur, les dates de tournage, et les lieux.
4. Afficher pour chaque arrondissement son nombre de tournages.


# Exercice 4 - Analyser du CSV

Ecrire un programme Python qui va
1. Récupérer le fichier des titres les plus prétés dans les
bibliothèques à Paris à l'adresses:
[https://opendata.paris.fr/explore/dataset/les-titres-les-plus-pretes/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B]
2. Analyser le fichier CSV obtenu pour afficher, pour toutes les entrées:
le titre, l'auteur, le nombre de prets.
3. Afficher pour chaque type de documents (il peut y avoir
plusieurs entrées pour un meme type de documents),
le nombre total de prets pour ce type.
4. Afficher les titres dans l'ordre de rentabilité (par ordre décroissant du nombre de prets
par exemplaire).


# Exercice 5 - Analyser du HTML

Ecrire un programme Python qui va:
1. Récupérer le contenu de la page Wikipedia à l'adresse:
[https://fr.wikipedia.org/wiki/Liste_des_pays_par_densit%c3%A9_de_population]
2. Afficher tous les pays mentionnés dans le tableau "Densité par pays (1950-2018)".
3. Afficher pour chaque pays son rang, sa densité, sa population, sa superficie.
4. Sauvegarder les informations obtenues dans un dictionnaire Python.
5. En utilisant le dictionnaire Python ainsi sauegardé, demander à l'utilisateur un pays,
lui afficher les informations correspondantes.


# Exercice 6 - API Web

1. Ecrire un programme Python qui va rendre disponible
une API Web permettant des calculs élémentaires sur des nombres entiers.
Les API sont accessibles par GET et de la forme:
- `/add/{entier1}/{entier2}` : réaliser l'addition de entier1 et entier2
- `/sub/{entier1}/{entier2}` : réaliser la soustraction de entier1 et entier2
- `/mul/{entier1}/{entier2}` : réaliser la multiplication de entier1 et entier2
- `/div/{entier1}/{entier2}` : réaliser la division entière de entier1 par entier2
- `/mod/{entier1}/{entier2}` : réaliser le reste de la division de entier1 et entier2

2. Ecrire un programme Python qui va tester l'API rendue disponible
au moyen de la bibliothèque requests.
