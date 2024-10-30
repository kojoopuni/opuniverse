#!/bin/bash
BACKUP_DIR=~/n8n-backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Stop n8n container temporarily
cd ~/n8n
docker-compose down

# Create backup
tar -czf $BACKUP_DIR/n8n_backup_$TIMESTAMP.tar.gz ~/.n8n

# Restart n8n
docker-compose up -d

# Keep only last 7 backups
ls -t $BACKUP_DIR/n8n_backup_*.tar.gz | tail -n +8 | xargs -r rm
