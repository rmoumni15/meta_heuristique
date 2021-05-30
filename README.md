## Projet meta-heuristique : 

<p> Ce projet consiste en l'étude d'un problème d’ordonnancement jobshop. Où on dispose d’un ensemble de jobs avec chaque job 
possédant plusieurs taches a exécuté. L’objectif est de minimiser le temps d’ordonnancement (makespan). 
Le programme fournit une implementation des solutions :
 </p>
 <ul>
    <li> <b>Gloutonne :</b> SPT, LRPT, EST-SPT, EST-LRPT   </li>
    <li> <b> Descente</b></li>
    <li> <b>Tabou</b></li>
 </ul> 
 
#### preparé par :
<ul>
<li> <b> Rida Moumni </b></li> 
<li><b> Waffa Pagou Brondon </b></li> 
<li><b> Alfousseyni Keita </b> </li>
</ul>

## Implémentation :

Nous avons implémenter notre solution dans un environnement avec <b> Anaconda </b>

#### 

```
conda create -n JobShop python=3.7.9
conda activate JobShop
```


#### Requirements : 
```
pip install -r requirements.txt
```
#### Execution :

```
python main.py --Instances instance1 instance2 ..etc --Descent True --Taboo True --export True
```
##### Exemple :
```
python main.py --Instances aaa1 ft06 --Descent True --Taboo True
```

#### Documentation :

```
usage: main.py [-h] [--Instances INSTANCES [INSTANCES ...]]
               [--Descent DESCENT] [--Taboo TABOO] [--stop STOP]
               [--maxiter MAXITER] [--taboo_period TABOO_PERIOD]
               [--export EXPORT]

optional arguments:
  -h, --help            show this help message and exit
  --Instances INSTANCES [INSTANCES ...]
                        Liste des instances a executer
  --Descent DESCENT     Executer la methode descente
  --Taboo TABOO         Execute la methode tabou
  --stop STOP           Le temps limite pour les methodes descente et tabou
  --maxiter MAXITER     Nombre maximum d'iteration (methode tabou)
  --taboo_period TABOO_PERIOD
                        le nombre d'itérations ou la permutation inverse est
                        interdite pour la méthode tabou
  --export EXPORT       Exporter les résultats dans un fichier Excel

```