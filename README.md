# Badgeuse - Application d'Appel Étudiant

L'application **Badgeuse** permet de gérer l'appel des étudiants via un lecteur NFC. Elle affiche en temps réel la liste des étudiants et leur statut (présent, absent ou en retard), et vous permet de sauvegarder les données dans un fichier CSV.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **Python 3** : Si vous ne l'avez pas encore installé, vous pouvez le télécharger [ici](https://www.python.org/downloads/).
- **Lecteur NFC compatible avec libnfc**.
- **libnfc** : Bibliothèque nécessaire pour la communication avec le lecteur NFC.

### Installation de libnfc

#### Sous Linux / macOS

1. Installez la bibliothèque via le gestionnaire de paquets :

```bash
sudo apt update && sudo apt install libnfc-bin libnfc-dev
```

2. Vérifiez la détection du lecteur :

```bash
nfc-list
```

#### Sous Windows

1. Téléchargez les fichiers binaires pré-compilés depuis le site officiel de libnfc.
2. Configurez les variables d'environnement pour pointer vers les fichiers de la bibliothèque.
3. Vérifiez la détection du lecteur avec :

```bash
nfc-list.exe
```

## Installation du projet

1. **Cloner ce projet**

Clonez ce repository sur votre machine locale :

```bash
git clone https://votre-repository-url.git
cd badgeuse_tech
```

2. **Installer les dépendances Python**

Installez les bibliothèques nécessaires avec la commande suivante :

```bash
pip install -r requirements.txt
```

## Lancer l'application

Une fois les dépendances installées, exécutez simplement :

```bash
python badgeuse.py
```

L'application se lance avec une interface graphique.

## Fonctionnalités

- **Lecture de cartes NFC** : L'application scanne les cartes des étudiants et met à jour leur statut (présent, absent ou en retard).
- **Choix dynamique du fichier étudiants** : Vous pouvez choisir un fichier CSV commençant par `etudiants_*.csv`.
- **Interface utilisateur** : Une interface graphique affiche la liste des étudiants et leur statut en temps réel.
- **Sauvegarde des données** : L'état de la présence peut être sauvegardé dans un fichier CSV (`presence_etudiants.csv`).
- **Connexion automatique au lecteur NFC** : L'application vérifie régulièrement la connexion au lecteur NFC.

## Structure du projet

Voici une vue d'ensemble des fichiers du projet :

```text
badgeuse_tech/
├── badgeuse.py            # Script principal de l'application
├── etudiants_*.csv        # Fichiers CSV contenant les informations des étudiants
├── requirements.txt       # Liste des dépendances Python
├── README.md              # Ce fichier
└── presence_etudiants.csv # Fichier CSV créé automatiquement pour sauvegarder l'état de la présence
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

