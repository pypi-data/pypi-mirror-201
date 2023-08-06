# Aide mémoire commande

## Docker
- Créer un docker streamlit :
    ```ssh
    sudo docker build -t streamlitapp:latest .
    ```

- Créer un docker ebp_flow :
    ```ssh
    sudo docker build -t ebp-script .
    ```

- Créer un docker etiquette :
    ```ssh
    sudo docker build -t etiquette .
    ```

- Lancer un docker sur le port **3306** :
    ```ssh
    sudo docker run -d --net=host -p 8501:8501 streamlitapp:latest
    ```

- Lancer un docker sur le port **3306** pour etiquette:
    ```ssh
    sudo docker run -d --net=host -p 8502:8502 etiquette
    ```

- Voir les dockers qui tournent :
    ```ssh
    sudo docker ps
    ```

- Arrêter un docker qui tourne :
    ```ssh
    sudo docker stop ...
    ```
    Remplacer les "..." par l’id du docker obtenu avec la commande ***docker ps***

## GIT

- Token de JClecodeur : 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
- Cloner le répertoire ACV de JClecodeur :
    ```ssh
    git clone https://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@github.com/JClecodeur/ACV.git
    ```

## SSH
- Supprimer un répertoire :
    ```ssh
    rm -rf lenomdurep
    ```

- Se connecter au serveur depuis le terminal :
    ```ssh
    ssh media@192.168.1.212
    ```

## Python
- Créer un fichier requirements.txt :
    ```ssh
    pipreqs #pip install pipreqs
    ```
- Créer un environnement virtuel :
    ```ssh
    virtualenv .venv #pip install virtualenv
    ```
- Utiliser l'environnement virtuel :
    ```ssh
    .venv/bin/activate
    ```
- Si ssh ne trouve pas un packages python pourtant installé, par exemple streamlit :
    ```ssh
    python3 -m streamlit run app.py
    ```
- Installer les packages de *requirements.txt* :
    ```ssh
    pip install -r requirements.txt
    ```