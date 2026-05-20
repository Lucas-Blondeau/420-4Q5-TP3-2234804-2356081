# TP3 - Infrastructure Docker et Automatisation de Sauvegarde

## Équipe
| Nom | DA |
|-----|----|
| Lucas Blondeau | 2234804 |
| Alicia Masson | 2356081 |

## Dépôt GitHub
https://github.com/Lucas-Blondeau/420-4Q5-TP3-2234804-2356081

## Adresses IP
| Machine | IP |
|---------|----|
| VM1 (production) | 172.20.45.194 |
| VM2 (sauvegarde) | 172.20.45.199 |

---

## Architecture

Client → reverse-proxy (Nginx) → app (WordPress) → db (MySQL)
                                       ↓
                                  maintenance
                                       ↓
                              VM2 /srv/backups/tp3

---

## Comment exécuter le projet

### Prérequis
- Docker et Docker Compose installés sur VM1
- SSH configuré entre VM1 et VM2
- Fichier `.env` créé à partir de `.env.example`

### 1. Cloner le dépôt
git clone https://github.com/Lucas-Blondeau/420-4Q5-TP3-2234804-2356081.git
cd 420-4Q5-TP3-2234804-2356081

### 2. Configurer les variables d'environnement
cp .env.example .env
nano .env

Variables à configurer :
| Variable | Description |
|----------|-------------|
| WORDPRESS_DB_NAME | Nom de la base de données WordPress |
| WORDPRESS_DB_USER | Utilisateur WordPress |
| WORDPRESS_DB_PASSWORD | Mot de passe WordPress |
| MYSQL_ROOT_PASSWORD | Mot de passe root MySQL |
| MYSQL_DATABASE | Nom de la base de données MySQL |
| MYSQL_USER | Utilisateur MySQL |
| MYSQL_PASSWORD | Mot de passe MySQL |
| BACKUP_USER | Utilisateur SSH sur VM2 |
| BACKUP_HOST | IP de VM2 |
| BACKUP_PATH | Chemin de sauvegarde sur VM2 |

### 3. Configurer la clé SSH
ssh-keygen -t ed25519 -C "backup-key" -f ~/.ssh/backup_key
ssh-copy-id -i ~/.ssh/backup_key.pub backupuser@172.168.10.2

### 4. Déployer
docker compose up -d

---

## Commandes de test

### Vérifier l'état des conteneurs
docker compose ps

### Afficher les logs du conteneur de maintenance
docker compose logs maintenance

### Exécuter une sauvegarde manuellement
docker exec -it maintenance python backup.py

### Vérifier la présence des sauvegardes sur VM2
ssh -i ~/.ssh/backup_key backupuser@172.168.10.2 "ls -lh /srv/backups/tp3"

### Vérifier l'accès à WordPress
Ouvrir un navigateur et aller sur :
http://172.20.45.194