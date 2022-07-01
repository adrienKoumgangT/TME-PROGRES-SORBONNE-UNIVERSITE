# Exercice 1 - Surveillance du réseau local

On cherche à programmer en Python un mécanisme de 
surveillance du réseau local. Il s'agit, pour
chaque machine pouvant se trouver sur ce réseau local,
de déterminer si elle répond à l'exécution de la
commande ping. L'ensemble des machines qui répondent
à la commande ping devrait ensuite etre affiché par
le programme.


# Exercice 2 - Evolution des routes réseau

On cherche à programmer en Python un mécanisme pour
l'évolution des routes entre une machine client (celle
qui exécute le programme Python) et un serveur (spécifié
par une chaine de caractères). Plus spécifiquement, on 
pourra exécuter plusieurs fois (à intervalles réguliers)
la commande `traceroute` pour obtenir la route entre client
et le serveur à un instant donné, puis stocker la route
obtenue si elle diffère des routes déjà stockées.


# Exercice 3 - Impact de l'équilibrage DNS

On cherche à programmer en Python un mécanisme qui permette
d'obtenir l'ensemble des adresses IP qui correspondent
à un nom logique (comme www.google.com). Pour cela, on 
peut exécuter plusieurs fois (à intervalles réguliers) la
commande `dig` et ajouter les adresses IP obtenues
si elles ne se trouvent pas déjà parmi celles déjà obtenues.


# Exercice 4 - Evolution du RTT

On cherche à programmer en Python un mécanisme qui permette
de suivre au cours du temps l'évolution du RTT entre une machine
(celle qui exécute le programme Python) et plusieurs autres machines
qui sont fournies en paramètres au programme. on pourra par exemple,
à intervalles réguliers (la durée de l'intervalle étant un paramètre
du programme) effectuer une séries de mesures de RTT pour chacune
des machines cibles. A la fin de chaque série de mesures, les nouvelles
données sont sauvegardées dans un fichier qui répertoire les résultats
de toutes les mesures depuis le début du programme, et un graphique
de la situation depuis le début de l'exécution du programme est actualisé.
Ce graphique comprend en particulier l'évolution dans le temps mesuré
vers chaque machine cible.
