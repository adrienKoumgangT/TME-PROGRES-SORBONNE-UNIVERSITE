# Exercice 3 - Serveur Web avec TCP

On cherche à programmer en Python un serveur Web simplifié
qui répond aux requetes formulées par les clients
(navigateur Web) de la manière suivante:

1. Création d'une socket de connection lors d'une demande par un client;
2. Réception de la requete (supposée suivre le protocole HTTP)
sur cette socket de connection;
3. Analyse de la requete pour déterminer le fichier demandé;
4. trouver le fichier demander dans le système de fichiers du serveur;
5. Créer une réponse au format HTTP comprenant l'entete et le contenu
du fichier;
6. Envoyer la réponse sur la socket de connection, puis fermer.

Dans le cas où le navigateur demande un fichier qui n'est pas présent
sur le serveur, le serveur doit retourner au client un message HTTP de type 404.
Si le serveur est exécuté sur une machine qui execute déjà un serveur web,
il pourra etre nécessaire d'utiliser un numéro de port différent du port 80.

1. Programmer le serveur Web en Python;
2. Tester le programme avec un navigateur Web,
sur la meme machine et sur des machines différentes;
3. Tester le serveur et plusieurs client qui effectuent
des requetes simultanées.
