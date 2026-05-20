import os
import subprocess
import datetime
import glob

# --- Configuration depuis les variables d'environnement ---
BACKUP_USER = os.environ.get("BACKUP_USER")
BACKUP_HOST = os.environ.get("BACKUP_HOST")
BACKUP_PATH = os.environ.get("BACKUP_PATH")
SSH_KEY_PATH = "/root/.ssh/backup_key"

# --- Répertoires à sauvegarder ---
VOLUMES = [
    "/mnt/wp_data",
    "/mnt/db_data"
]

# --- Répertoire local temporaire pour les archives ---
LOCAL_BACKUP_DIR = "/tmp/backups"
os.makedirs(LOCAL_BACKUP_DIR, exist_ok=True)

# --- Nom de l'archive horodatée ---
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
archive_name = f"backup_{timestamp}.tar.gz"
archive_path = os.path.join(LOCAL_BACKUP_DIR, archive_name)


def create_archive():
    """Créer une archive compressée des volumes."""
    print(f"\n[1/3] Création de l'archive : {archive_name}")
    
    cmd = ["tar", "-czf", archive_path] + VOLUMES
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Erreur lors de la création de l'archive : {result.stderr}")
        exit(1)
    
    size = os.path.getsize(archive_path)
    size_mb = round(size / (1024 * 1024), 2)
    print(f"Archive créée avec succès : {archive_name} ({size_mb} MB)")


def transfer_archive():
    """Transférer l'archive vers VM2 via rsync/SSH."""
    print(f"\n[2/3] Transfert vers {BACKUP_USER}@{BACKUP_HOST}:{BACKUP_PATH}")
    
    cmd = [
        "rsync", "-avz",
        "-e", f"ssh -i {SSH_KEY_PATH} -o StrictHostKeyChecking=no",
        archive_path,
        f"{BACKUP_USER}@{BACKUP_HOST}:{BACKUP_PATH}/"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Erreur lors du transfert : {result.stderr}")
        exit(1)
    
    print(f"Transfert réussi !")


def rotate_backups():
    """Supprimer les archives locales de plus de 7 jours."""
    print(f"\n[3/3] Rotation des sauvegardes locales (> 7 jours)")
    
    now = datetime.datetime.now()
    archives = glob.glob(os.path.join(LOCAL_BACKUP_DIR, "backup_*.tar.gz"))
    deleted = 0
    
    for archive in archives:
        modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(archive))
        age = (now - modified_time).days
        
        if age > 7:
            os.remove(archive)
            print(f"Supprimé : {os.path.basename(archive)} ({age} jours)")
            deleted += 1
    
    if deleted == 0:
        print("Aucune archive à supprimer.")
    else:
        print(f"{deleted} archive(s) supprimée(s).")


if __name__ == "__main__":
    print("=== Début de la sauvegarde ===")
    create_archive()
    transfer_archive()
    rotate_backups()
    print("\n=== Sauvegarde terminée avec succès ===")