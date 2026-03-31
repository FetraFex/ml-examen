# 🤖 Examen Machine Learning | Mardi 31 mars 2026 | [ISPM](https://ispm-edu.com/)

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
    <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
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
| <img src="https://avatars.githubusercontent.com/u/165788737?v=4" width="50" style="border-radius:50%"> | **ANDRIANARAHINJAKA** Yohannee Aintsoa    | IGGLIA 4 | 54  |

---

## Réponses aux Questions (Q1 - Q4)

### Q1 — Analyse des coefficients (Régression Logistique)

- **Observations :** Pour le modèle `x_wins`, les coefficients les plus élevés se trouvent sur la **case centrale (index 4)** et les **quatre coins (0, 2, 6, 8)**. Une occupation par 'X' sur ces cases a un coefficient positif fort, tandis qu'une occupation par 'O' a un coefficient négatif marqué.
- **Influence du centre :** **Oui**, la case centrale est la plus influente car elle appartient à 4 combinaisons gagnantes potentielles (ligne, colonne et les 2 diagonales).
- **Cohérence stratégique :** C'est parfaitement cohérent avec la stratégie humaine : contrôler le centre maximise les chances de créer des menaces multiples (fourchettes) tout en bloquant l'adversaire.

### Q2 — Déséquilibre des classes

- **État du Dataset :** Le dataset est naturellement déséquilibré. Les victoires (~60-70%) sont beaucoup plus fréquentes que les matchs nuls (< 10%).
- **Métrique privilégiée :** Nous privilégions le **F1-Score**.
- **Pourquoi :** L'**Accuracy** est trompeuse sur un dataset déséquilibré. Un modèle qui prédirait toujours "pas de match nul" aurait une bonne Accuracy mais serait inutile. Le F1-Score force le modèle à être performant sur la classe minoritaire (le nul) en combinant précision et rappel.

### Q3 — Comparaison des modèles (Wins vs Draw)

- **Performance :** Le modèle `x_wins` obtient généralement de meilleurs scores que le modèle `is_draw`.
- **Difficulté d'apprentissage :** Le modèle `is_draw` est plus complexe à entraîner. Un nul ne dépend pas d'un seul "bon coup", mais d'une **succession parfaite de blocages**. C'est une condition structurelle plus difficile à capturer pour un modèle linéaire.
- **Erreurs types :** Les erreurs surviennent surtout en fin de partie (saturation de pions) ou sur des tactiques de "fourchettes" que la Régression Logistique peine à modéliser par sa nature linéaire.

### Q4 — Mode Hybride (Minimax + ML)

- **Comportement :** Le mode **Hybride** est plus rigoureux et impitoyable. Contrairement au ML pur qui réagit statistiquement, l'Hybride ne rate jamais un coup gagnant immédiat.
- **Évitement des pièges :** **Oui**, l'Hybride évite parfaitement les pièges. Grâce au **Minimax**, il explore l'arbre des possibles pour choisir la case mathématiquement sûre, là où le ML pur pourrait privilégier une case "statistiquement bonne" mais tactiquement perdante.

---

Lien vidéo: [Vidéo de présentation](https://drive.google.com/file/d/1covfbs8eK48zV7f3qOvspRAW0894Neas/view?usp=sharing)
