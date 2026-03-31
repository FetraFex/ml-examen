# 🤖 Examen Machine Learning | Mardi 31 mars 2026 | ISPM

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=00b4d8&height=200&section=header&text=Examen%20Machine%20Learning&fontSize=50&animation=fadeIn&fontAlignY=38" alt="Header Banner">
</p>

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Matplotlib-ffffff?style=for-the-badge&logo=matplotlib&logoColor=black" alt="Matplotlib">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge&logo=generic&logoColor=white" alt="Seaborn">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">
  </a>
</p>

## 👥 Présentation de l'Équipe

|                                                 Photo                                                  | Informations Personnelles                 |  Classe  | N°  |
| :----------------------------------------------------------------------------------------------------: | :---------------------------------------- | :------: | :-: |
| <img src="https://avatars.githubusercontent.com/u/106149835?v=4" width="50" style="border-radius:50%"> | **RASOAMAHAZOMANANA** Tsitoniaina Rogella | IGGLIA 4 | 15  |
| <img src="https://avatars.githubusercontent.com/u/171586866?v=4" width="50" style="border-radius:50%"> | **ANDRIAMAHEFA** Ny Fetra Phanoël         | IGGLIA 4 | 16  |
| <img src="https://avatars.githubusercontent.com/u/144239227?v=4" width="50" style="border-radius:50%"> | **ANDRIANTSOA** Velotiana Todisoa Angelo  | IGGLIA 4 | 22  |
| <img src="https://avatars.githubusercontent.com/u/110011721?v=4" width="50" style="border-radius:50%"> | **RAKOTOARISOA** Fanaja Manoa Ny Avo      | IGGLIA 4 | 32  |
| <img src="https://avatars.githubusercontent.com/u/117814535?v=4" width="50" style="border-radius:50%"> | **NOMESAHANINA** Aiky                     | IGGLIA 4 | 35  |
| <img src="https://avatars.githubusercontent.com/165788737?v=4" width="50" style="border-radius:50%"> | **ANDRIANARAHINJAKA** Yohannee Aintsoa    | IGGLIA 4 | 54  |

---

## Baseline Machine Learning — Morpion (régression logistique)

Cette section décrit **tout ce qui a été ajouté ou mis à jour** pour la baseline : fichiers, rôles et utilisation.

### Fonctionnalités du notebook `baseline_logistic_regression.ipynb`

| Étape | Description |
| ----- | ----------- |
| Chargement | Lecture du CSV (`ressources/dataset.csv`) avec **pandas** |
| Features / cibles | 18 colonnes binaires `c0_x, c0_o, …, c8_o` ; cibles **`x_wins`** et **`is_draw`** |
| Découpage | **Train / test 80/20** (`train_test_split`), un seul split aligné pour les deux cibles |
| Modèles | Deux **`LogisticRegression`** (sklearn), une par cible |
| Prédictions | Sur le jeu de test |
| Métriques | **Accuracy**, **F1-score**, **matrice de confusion**, **`classification_report`** |
| Comparaison | Tableau récapitulatif (`pandas.DataFrame`) des deux modèles |

Le notebook inclut aussi :

- Une **cellule de vérification** du Python utilisé (chemin doit contenir `.venv` si tu travailles dans l’environnement virtuel du projet).
- Des **métadonnées de noyau** réglées sur **`Python (ml-examen .venv)`** pour éviter d’ouvrir par défaut le mauvais interpréteur.

### Fichiers du dépôt (rôles)

| Fichier / dossier | Rôle |
| ----------------- | ---- |
| **`baseline_logistic_regression.ipynb`** | Notebook principal : baseline, métriques, fonctions réutilisables (`load_dataset`, `split_features_and_targets`, `train_logistic_regression`, `evaluate_binary_classifier`). |
| **`requirements.txt`** | Dépendances Python : **pandas**, **scikit-learn**, **jupyter**, **notebook**, **jupyterlab**, **ipykernel**, **streamlit**. |
| **`run_jupyter.sh`** | Lance **`jupyter lab`** avec `JUPYTER_CONFIG_DIR` pointant vers `jupyter_config/` (timeouts WebSocket cohérents, moins de warnings serveur). |
| **`register_jupyter_kernel.sh`** | Enregistre le Python du **`.venv`** comme noyau Jupyter nommé **`ml-examen`** (`Python (ml-examen .venv)`), pour que `import pandas` fonctionne dans le notebook. |
| **`jupyter_config/jupyter_server_config.py`** | Configuration **Jupyter Server** : `websocket_ping_interval` / `websocket_ping_timeout` alignés (évite l’avertissement sur les pings). |
| **`ressources/`** | Dossier attendu pour **`dataset.csv`** (chemin relatif utilisé dans le notebook). |
| **`src/board_encoding.py`** | Conversion plateau 3×3 → 18 features (même convention que le CSV). |
| **`src/ml_baseline_service.py`** | Entraînement des deux régressions logistiques + prédictions (utilisé par l’interface, logique alignée sur le notebook). |
| **`streamlit_app.py`** | Interface : **test des prédictions** sur un plateau encodé à la main, **Humain vs Humain**, **Humain vs IA** (heuristique ML). Ne modifie pas le notebook. |
| **`docs/ARCHITECTURE.md`** | Vue d’ensemble des dossiers / fichiers cible hackathon. |
| **`docs/PROCHAINES_ETAPES.md`** | Ordre recommandé : générateur → EDA → baseline → modèles avancés → interface complète → README final. |

### Interface utilisateur (test des modèles)

```bash
cd ml-examen
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Ouvre l’URL affichée (souvent `http://localhost:8501`). Mode **« Test ML »** : régler chaque case (vide / X / O) et lire **P(x_wins)** et **P(is_draw)**. Les modes **Humain vs Humain** et **Humain vs IA** permettent de jouer ; l’IA utilise les mêmes modèles baseline (heuristique sur les coups possibles).

### Installation et exécution (résumé)

```bash
cd ml-examen
python3 -m venv .venv
source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
./register_jupyter_kernel.sh
./run_jupyter.sh
```

Puis dans le navigateur : ouvrir **`baseline_logistic_regression.ipynb`**, vérifier le noyau **`Python (ml-examen .venv)`**, exécuter toutes les cellules (**Run → Run All Cells**).

### Problèmes fréquents

| Symptôme | Cause probable | Piste |
| -------- | -------------- | ----- |
| `No module named 'pandas'` | Le noyau Jupyter n’est pas le **`.venv`** | `./register_jupyter_kernel.sh` puis **Kernel → Change Kernel… → Python (ml-examen .venv)** |
| `Kernel does not exist` | Session / serveur redémarré | Recharger la page ou **Kernel → Restart** |
| Erreurs `/lab/api/...` ou `Stream is closed` | Plusieurs clients (IDE + navigateur) sur le même port | Un seul client à la fois, ou utiliser `./run_jupyter.sh` |

---

*Dernière mise à jour de cette section : documentation des scripts et du notebook baseline (régression logistique Morpion).*
