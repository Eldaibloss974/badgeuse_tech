
# Badgeuse - Application d'Appel Étudiant

L'application **Badgeuse** permet de gérer l'appel des étudiants via un lecteur NFC. Elle affiche en temps réel la liste des étudiants et leur statut (présent ou absent), et vous permet de sauvegarder les données dans un fichier CSV.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **Python 3** : Si vous ne l'avez pas encore installé, vous pouvez le télécharger [ici](https://www.python.org/downloads/).
- **Lecteur NFC** : Un lecteur de cartes NFC est nécessaire pour utiliser cette application.

## Installation

Suivez les étapes ci-dessous pour installer et exécuter l'application.

### 1. Cloner ce projet

Clonez ce repository sur votre machine locale :

```bash
git clone https://votre-repository-url.git
cd badgeuse_tech
```

### 2. Créer un environnement virtuel

Pour éviter des conflits de dépendances avec d'autres projets, il est recommandé de créer un environnement virtuel. Si vous n'avez pas `virtualenv` installé, vous pouvez le faire avec la commande suivante :

```bash
pip install virtualenv
```

Ensuite, créez un environnement virtuel :

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

Sous **Windows** :

```bash
venv\Scripts\activate
```

Sous **macOS/Linux** :

```bash
source venv/bin/activate
```

### 4. Installer les dépendances

Une fois l'environnement virtuel activé, installez les dépendances requises avec la commande suivante :

```bash
pip install -r requirements.txt
```

### 5. Lancer l'application

Une fois les dépendances installées, vous pouvez démarrer l'application en exécutant :

```bash
python badgeuse.py
```

L'application devrait alors se lancer avec l'interface graphique.

## Fonctionnalités

- **Lecture de cartes NFC** : L'application scanne les cartes des étudiants et met à jour leur statut (présent ou absent).
- **Interface utilisateur** : Une interface graphique permet d'afficher la liste des étudiants et leur statut en temps réel.
- **Sauvegarde des données** : Vous pouvez sauvegarder l'état de la présence dans un fichier CSV (`presence_etudiants.csv`).
- **Connexion automatique au lecteur NFC** : L'application vérifie régulièrement la connexion au lecteur NFC et l'affiche à l'écran.

## Structure du projet

Voici une vue d'ensemble des fichiers du projet :

```text
badgeuse_tech/
├── badgeuse.py            # Script principal de l'application
├── etudiants.csv          # Fichier CSV contenant les informations des étudiants
├── requirements.txt       # Liste des dépendances Python
├── README.md              # Ce fichier
└── presence_etudiants.csv # Fichier CSV crée automatique pour sauvegarder l'état de la présence
```

## Contributions

Les contributions à ce projet sont les bienvenues ! Si vous avez des idées d'amélioration ou des corrections, n'hésitez pas à :

1. Forker le projet.
2. Créer une branche pour vos modifications (`git checkout -b feature/amélioration`).
3. Effectuer vos changements.
4. Committer vos modifications (`git commit -am 'Ajout de [fonctionnalité]'`).
5. Pousser la branche (`git push origin feature/amélioration`).
6. Ouvrir une *pull request* pour que vos modifications soient examinées.

Merci d'utiliser **Badgeuse** ! Si vous avez des questions, n'hésitez pas à ouvrir une issue ou à envoyer un message.