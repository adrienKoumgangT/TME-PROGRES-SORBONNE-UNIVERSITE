# Exercice 1 - Client / Serveur UDP

On cherche à programmer en Python un mécanisme de PING
entre deux machines connectées à Internet.
Le client envoie une série de requetes au serveur sous
forme de paquets UDP de contenu arbitraire.
Le serveur répond à chaque requete par un paquet UDP
de contenu arbitraire adressé au client qui a effectué
la requete. Le client mesure le temps écoulé entre sa
requete initiale et la réponse reçue du serveur pour
évaluer le RTT avec le serveur.
Puis, il effectue la moyenne des RTT mesurés et l'affiche
à l'utilisateur.

1. A partir des exemples de code vus en cours pour le client
et el serveur UDP, programmer le mécanisme PING client / serveur
en Python;
2. Tester les programmes client et serveur sur la meme machine
et sur des machines différentes;
3. tester le serveur et plusieurs clients qui effectuent des
requetes simultanées;
4. Modifier le code du serveur pour qu'il oublie de répondre
avec une probabilité 0.5 à une requete formulée par un client.
Que se passe-t'il ? Modifier le client pour rétablir un
fonctionnement normal. Tester les modifications comme en 2. en 3.
