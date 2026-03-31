# 🤖 Examen Machine Learning | Mardi 31 mars 2026 | [ISPM](https://ispm-edu.com/)

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=00b4d8&height=200&section=header&text=Examen%20Machine%20Learning&fontSize=50&animation=fadeIn&fontAlignY=38" alt="Header Banner">
</p>

<p align="center">
  <a href="https://ml-examen.vercel.app/">
    <img src="https://img.shields.io/badge/Demo-Live%20Project-success?style=for-the-badge&logo=vercel&logoColor=white" alt="Live Demo">
  </a>
  <a href="https://github.com/FetraFex/ml-examen">
    <img src="https://img.shields.io/badge/Source-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>
</p>

## 👥 Présentation de l'Équipe

| Photo | Informations Personnelles | Classe | N° |
| :---: | :--- | :---: | :---: |
| <img src="https://avatars.githubusercontent.com/u/106149835?v=4" width="50" style="border-radius:50%"> | **RASOAMAHAZOMANANA** Tsitoniaina Rogella | IGGLIA 4 | 15 |
| <img src="https://avatars.githubusercontent.com/u/171586866?v=4" width="50" style="border-radius:50%"> | **ANDRIAMAHEFA** Ny Fetra Phanoël | IGGLIA 4 | 16 |
| <img src="https://avatars.githubusercontent.com/u/144239227?v=4" width="50" style="border-radius:50%"> | **ANDRIANTSOA** Velotiana Todisoa Angelo | IGGLIA 4 | 22 |
| <img src="https://avatars.githubusercontent.com/u/110011721?v=4" width="50" style="border-radius:50%"> | **RAKOTOARISOA** Fanaja Manoa Ny Avo | IGGLIA 4 | 32 |
| <img src="https://avatars.githubusercontent.com/u/117814535?v=4" width="50" style="border-radius:50%"> | **NOMESAHANINA** Aiky | IGGLIA 4 | 35 |
| <img src="https://avatars.githubusercontent.com/u/165788737?v=4" width="50" style="border-radius:50%"> | **ANDRIANARAHINJAKA** Yohannee Aintsoa | IGGLIA 4 | 54 |

---

## Description du Projet
Ce projet a été réalisé dans le cadre de l'examen de Machine Learning à l'ISPM. Il consiste en la création d'une plateforme interactive de **Morpion (Tic-Tac-Toe)** augmentée par l'intelligence artificielle. L'objectif est de comparer des modèles statistiques classiques (Régression Logistique) avec des algorithmes hybrides pour prédire l'issue d'une partie en temps réel.

**Lien du projet :** [https://ml-examen.vercel.app/](https://ml-examen.vercel.app/)

---

## Structure du Répertoire
L'architecture suit une séparation stricte entre la logique de données et l'interface utilisateur :

* `root` : Fichiers de configuration et documentation.
* `backend/` : Serveur **FastAPI** gérant les prédictions du modèle.
    * `main.py` : Points de terminaison de l'API.
    * `models/` : Modèles sérialisés (`.pkl`).
* `frontend/` : Interface client développée avec **React**.
* `notebooks/` : Analyse exploratoire et entraînement des modèles (Baselines).
* `src/` : Les fichiers générteur de dataset.
* `ressources/` : Les fichiers dataset.

---

## Résultats Machine Learning
Nous avons évalué nos modèles sur deux cibles : la victoire de X (`x_wins`) et le match nul (`is_draw`).

| Modèle | Cible | Accuracy | F1-Score |
| :--- | :--- | :---: | :---: |
| Régression Logistique | `x_wins` | **~98%** | **0.98** |
| Régression Logistique | `is_draw` | ~91% | 0.45 |

*Note : Le modèle de victoire est extrêmement performant, tandis que le match nul reste un défi statistique dû au déséquilibre naturel du dataset.*

---

## Réponses aux Questions (Q1 - Q4)

### Q1 — Analyse des coefficients
Les coefficients les plus élevés se situent sur la **case centrale (index 4)** et les **quatre coins**. Cela confirme mathématiquement que le contrôle du centre est la stratégie pivot pour maximiser les menaces de victoire.

### Q2 — Déséquilibre des classes
Le dataset contient environ 60-70% de victoires contre moins de 10% de nuls. Nous privilégions le **F1-Score** car l'Accuracy ignorerait la difficulté du modèle à prédire correctement la classe minoritaire (le nul).

### Q3 — Comparaison des modèles (Wins vs Draw)
Le modèle `x_wins` surpasse `is_draw`. Prédire un nul est complexe car il ne s'agit pas d'une position gagnante isolée, mais d'une **succession parfaite de blocages** mutuels, ce qui est moins linéaire à apprendre.

### Q4 — Mode Hybride (Minimax + ML)
Le mode **Hybride** est impitoyable. En combinant l'exploration de l'arbre des possibles du **Minimax** avec les probabilités du ML, l'IA évite tous les pièges tactiques (fourchettes) et garantit un jeu sans erreur.

---

<p align="right"><i>Dernière mise à jour : 31 mars 2026.</i></p>