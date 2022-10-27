# brewery_api_restful

# Test-technique-Django-DRF

Un test technique django/drf sur la thématique de bars/bières.

# Test Technique Unyc

## Préambule

L'objectif de ce test est de développer une application Django en respectant les objectifs suivants:
- Utiliser Django et Django Rest Framework (vous pouvez utiliser les dernières versions)
- Coder en Python 3
- Utiliser les bonnes pratiques de Django et de DRF
- Coder le moins de lignes possible

Cela nous permettra d'évaluer ton degré de compréhension d'une spécification, ta capacité à lire et interpréter la documentation, et la rigueur et la qualité de ton code. Bien entendu, ton niveau d'expérience sur Django/DRF sera pris en compte !

Il n'existe pas de solution unique ni de *bonne* réponse, ta capacité à trouver des solutions et à interpréter les consignes fait partie de l'exercice.

L'utilisation de git et github/bitbucket/gitlab est obligatoire. Lorsque tu as terminé il faudra :
- Créer une issue
- Mettre ton code dans une branche attachée à l'issue
- Créer une merge request et nous la transmettre afin de procéder à la review du code et qu'on puisse y mettre nos commentaires.

*Merci de respecter la confidentialité de ce test et de ne pas le diffuser*.


## Consignes

L'objectif est de développer une API Restful utilisée par un bar.

Ce bar référence plusieurs types de bières. Il dispose de plusieurs comptoirs qui ont chacun leur propre stock.

Les clients (utilisateurs anonymes) peuvent commander et le personnel (utilisateurs authentifiés) peut gérer les références et le stock.

### Les references

L'endpoint `/api/references/` permet de lister les références de bières (qu'elles soient en stock ou non).

```
[
    {
        "pk": 1,
        "ref": "leffeblonde",
        "name": "Leffe blonde",
        "description": "Une bière blonde d'abbaye brassée depuis 1240 et que l'on ne présente plus !",
        "availability": "available"
    },
    {
        "pk": 2,
        "ref": "brewdogipa",
        "name": "Brewdog Punk IPA",
        "description": "La Punk IPA est une bière écossaise s'inspirant des tendances américaines en matière de brassage et du choix des houblons.",
        "availability": "outofstock"
    },
    {
        "pk": 3,
        "ref": "fullerindiapale",
        "name": "Fuller's India Pale Ale",
        "description": "Brassée pour l'export, la Fuller's India Pale Ale est la vitrine du savoir faire bien « british » de cette brasserie historique. ",
        "availability": "available"
    }
]
```

Les clients peuvent accéder à cet endpoint.
Seul le personnel peut modifier les références (toute suppression doit automatiquement supprimer les stocks décrits plus bas).

Le champs availability n'est pas stocké en base de données et doit être défini dynamiquement.

Il faut pouvoir trier, rechercher et paginer les résultats.

*Optionnel - Ajouter des paramètres GET pour :*
- *préciser un comptoir et donc avoir des résultats de disponibilité différents puisque chaque bar a son propre stock*
- *préciser que l'on veut seulement voir les références qui sont en stock*


### Les comptoirs du bar

L'endpoint `/api/bars/` renvoie la liste des comptoirs présents dans le bar (minimum 2).

```
[
    {
        "pk" : 1,
        "name": "1er étage"

    },
    {
        "pk" : 2,
        "name": "2ème étage"
    }
]
```

Les clients  ont le droit d'accéder à cet endpoint.
Seul le personnel peut ajouter, modifier ou supprimer des entrées via cet endpoint (penser à implémenter POST et PUT).

Il faut pouvoir trier et paginer les résultats.

### Les stocks

Il convient de modéliser un *stock* qui permet de connaitre le nombre de référence disponibles pour chaque comptoir.

L'endpoint `/api/stocks/` permet de lister les références disponibles dans le stock d'un comptoir et leurs quantités.

```
[
    {
        "reference": 1,
        "bar": 1,
        "stock": 10
    },
    {
        "reference": 2,
        "bar": 1,
        "stock": 8
    },

    {
        "reference": 2,
        "bar": 2,
        "stock": 5
    },
    {
        "reference": 3,
        "bar": 2,
        "stock": 1
    }
]
```

Seul le personnel a le droit d'accéder à cet endpoint qui est en lecture seule.

Il faut pouvoir trier, filtrer et paginer les résultats.


### Classer les comptoirs

Il est nécessaire de fournir au personnel des informations sur les comptoirs.

L'endpoint `/api/statistics/` permet de lister les bars en fonction de leurs caractéristiques.

Les caractéristiques attendues sont :
- all_stocks
- miss_at_least_one


```
[
    "all_stocks" : {
        "description": "Liste des comptoirs qui ont toutes les références en stock",
        "bars": [1]
    },
    miss_at_least_one: {
        "description": "Liste des comptoirs qui ont au moins une référence épuisée",
        "bars": [2]
    }
]
```

Seul le personnel a le droit d'accéder à cet endpoint.


### Les commandes


L'endpoint `/api/orders/` permet de commander des bières à un comptoir donné en faisant un `POST` avec le payload suivant :

```
{
    "bar": 1,
    "items": [
        {
            "reference": 1,
            "count": 2
        },
        {
            "reference": 2,
            "count": 1
        },
        {
            "reference": 3,
            "count": 1
        }
    ]
}
```

Toute commande est définitive.

Une entrée dans la table `Orders` doit être créé et `n` entrées dans la table `OrderItems` doivent être créées.

Chaque création dans la table `OrderItems` doit diminuer le comptage du stock du comptoir pour la référence. Le code mettant à jour le stock ne doit se trouver ni dans la view, ni dans le serializer, ni dans le model. Django offre un moyen élégant de réagir sur des création d'objets en base de données. Si le stock descend en dessous de 2, un message doit être affiché dans les *logs*.

Seuls les clients peuvent commander.

Le résultat de cet appel doit être un order serializé sous la forme suivante :

```
{
    "pk": 1,
    "bar": 1,
    "items": [
        {
            "reference": 1,
            "count": 2
        },
        {
            "reference": 2,
            "count": 1
        },
        {
            "reference": 3,
            "count": 1
        }
    ]
}
```

Seul le personnel peut lister les commandes.

## Pour finir

Les droits doivent être gérés dans des groupes.

Pour permettre de se servir de cette application, il faut ajouter des fixtures que l'on peut charger pour bootstraper l'application (utilisateurs, bars, references, stocks).

Bien sûr, des tests utilisant les fixtures sont attendus pour valider le fonctionnement de l'application.

N'hésite pas à intégrer dans le code tous type de bonus qui pourraient nous permettre de bien cerner ton niveau (Dockerfile, déploiement kubernetes, packaging, documentation..., les possibilités sont infinies ;-) ).

Bon test !
