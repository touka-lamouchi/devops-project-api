# Utiliser une image Python légère
FROM python:3.11-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app.py .

# Exposer le port 5000
EXPOSE 5000

# Définir les variables d'environnement
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Commande pour lancer l'application
CMD ["python", "app.py"]