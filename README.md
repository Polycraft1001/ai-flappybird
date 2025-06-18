# Projet Flappy Bird AI

Ce projet implémente une version de Flappy Bird avec un agent d'intelligence artificielle entraîné par Q-learning.

## Structure du projet

- `flappy_game.py`: Contient le moteur du jeu Flappy Bird, incluant les classes `Bird`, `Pipe`, et `Ground`. Il gère la physique du jeu (gravité, saut), la génération des tuyaux, et la détection des collisions. Il expose une fonction `get_state()` pour l'IA.
- `train_ai.py`: Implémente l'algorithme de Q-learning pour entraîner l'agent IA. Il utilise une version sans affichage du jeu pour accélérer l'entraînement. La Q-table entraînée est sauvegardée dans `q_table.pkl`.
- `play_ai.py`: Permet de visualiser l'agent IA entraîné jouer au jeu Flappy Bird avec l'affichage graphique. Il charge la Q-table sauvegardée et utilise les actions optimales basées sur l'état actuel du jeu.

## Prérequis

Assurez-vous d'avoir Python 3 et `pip` installés. Vous aurez également besoin de la bibliothèque `pygame` et `numpy`.

Pour installer les dépendances, exécutez la commande suivante :

```bash
pip install pygame numpy
```

## Comment exécuter le projet

1.  **Entraîner l'agent IA (recommandé en premier)**

    Pour entraîner l'agent Q-learning et générer le fichier `q_table.pkl`, exécutez :

    ```bash
    python3 train_ai.py
    ```

    L'entraînement peut prendre un certain temps (environ 10 000 épisodes par défaut). Vous verrez le score moyen affiché toutes les 100 épisodes.

2.  **Jouer avec l'agent IA entraîné**

    Une fois que `q_table.pkl` a été généré par l'étape d'entraînement, vous pouvez lancer le jeu avec l'IA en exécutant :

    ```bash
    python3 play_ai.py
    ```

    L'IA jouera automatiquement au jeu, et vous pourrez observer son comportement et son score.

3.  **Jouer au jeu manuellement (pour tester le moteur)**

    Si vous souhaitez tester uniquement le moteur du jeu sans l'IA, vous pouvez exécuter :

    ```bash
    python3 flappy_game.py
    ```

    Notez que cette version n'a pas de contrôle utilisateur, l'oiseau tombera simplement et se crashera.

## Remarques

-   Les paramètres de Q-learning (taux d'apprentissage, facteur de remise, taux d'exploration) peuvent être ajustés dans `train_ai.py` pour optimiser les performances de l'IA.
-   La discrétisation de l'espace d'état est définie dans `train_ai.py` et peut être affinée pour de meilleures performances.

