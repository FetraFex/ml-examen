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
| <img src="https://avatars.githubusercontent.com/u/165788737?v=4" width="50" style="border-radius:50%"> | **ANDRIANARAHINJAKA** Yohannee Aintsoa    | IGGLIA 4 | 54  |


Réponses 5.Questions README (Q1-Q4)

Q1 — Analyse des coefficients (Régression Logistique) Observations : Pour le modèle x_wins, les coefficients les plus élevés en valeur absolue se trouvent sur la case centrale (index 4) et les quatre coins (0, 2, 6, 8). Une occupation par 'X' sur ces cases a un coefficient positif fort, tandis qu'une occupation par 'O' a un coefficient négatif fort.

Influence du centre : Oui, la case centrale est la plus influente car elle appartient à 4 combinaisons gagnantes (ligne, colonne et les 2 diagonales).

Cohérence stratégique : C'est parfaitement cohérent avec la stratégie humaine : prendre le centre permet de maximiser ses chances de créer des fourchettes (double menace) tout en bloquant celles de l'adversaire.

Q2 — Déséquilibre des classes État du Dataset : Le dataset du Morpion est naturellement déséquilibré. Il y a beaucoup plus de victoires (environ 60-70%) que de matchs nuls (moins de 10%). x_wins = 1 est donc plus fréquent que is_draw = 1.

Métrique privilégiée : On privilégie le F1-Score.

Pourquoi : L'Accuracy est trompeuse sur un dataset déséquilibré (un modèle qui prédit "pas de match nul" tout le temps aurait une bonne Accuracy mais serait inutile). Le F1-Score combine précision et rappel, forçant le modèle à être performant même sur la classe minoritaire (le nul).

Q3 — Comparaison des deux modèles (Wins vs Draw) Le meilleur score : C'est généralement le modèle x_wins qui obtient le meilleur score.

Difficulté d'apprentissage : Le modèle is_draw est plus difficile à apprendre car un match nul au Morpion ne dépend pas d'une seule "bonne case", mais d'une suite parfaite de blocages des deux côtés. C'est une condition beaucoup plus complexe et subtile que de simplement aligner trois pions.

Erreurs types : Les modèles se trompent le plus dans les positions de "fin de partie" avec beaucoup de pions, là où une seule erreur de blocage change radicalement l'issue, ou sur les "fourchettes" que la Régression Logistique (modèle linéaire) a du mal à percevoir.

Q4 — Mode Hybride (Minimax + ML) Différence de comportement : Le mode Hybride est visiblement plus "froid" et impitoyable. Contrairement au mode ML pur qui peut parfois faire une erreur bête (car il ne "voit" pas le futur, il réagit statistiquement), l'Hybride ne rate jamais un coup gagnant et bloque systématiquement l'adversaire.

Évitement des pièges : Oui, le joueur hybride évite parfaitement les pièges (comme les doubles menaces) car le Minimax explore tout l'arbre des possibles. Là où le ML pur pourrait privilégier une case "statistiquement bonne" mais perdante à cause d'une tactique précise, l'Hybride choisit la case mathématiquement sûre.

Dernière mise à jour de cette section : documentation des scripts et du notebook baseline (régression logistique Morpion).