# Image de base Python 3.12 slim
FROM python:3.12-slim

# Installer les outils nécessaires
RUN apt-get update && apt-get install -y \
    rsync \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier le script de sauvegarde
COPY backup.py .

# Vérifier que les outils sont bien installés et que la connexion SSH vers VM2 fonctionne
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD rsync --version && ssh -i /root/.ssh/backup_key -o StrictHostKeyChecking=no \
    -o ConnectTimeout=5 ${BACKUP_USER}@${BACKUP_HOST} exit 0 || exit 1

# Lancer le script de sauvegarde
CMD ["python", "backup.py"]