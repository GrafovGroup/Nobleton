#!/usr/bin/env bash
set -euo pipefail
release_dir="$(cd "$(dirname "$0")/.." && pwd)"
site_dir=/home/nvfglyl5/nobleton.ca
private_dir=/home/nvfglyl5/nobleton-private
deploy_dir=/home/nvfglyl5/nobleton-deployments
php_bin="$(command -v php)"
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
test -d "$site_dir"
test -s "$private_dir/idx-token"
test -f "$release_dir/dist/homes-for-sale/index.html"
"$php_bin" -l "$release_dir/server/idx/lib.php"
"$php_bin" -l "$release_dir/server/idx/sync.php"
"$php_bin" -l "$release_dir/server/listings.php"
"$php_bin" "$release_dir/tests/idx.php"
umask 077
mkdir -p "$private_dir/idx"
cp "$release_dir/server/idx/"*.php "$private_dir/idx/"
chmod 700 "$private_dir" "$private_dir/idx"
chmod 600 "$private_dir/idx-token" "$private_dir/idx/"*.php
"$php_bin" "$private_dir/idx/sync.php"
tar -czf "$deploy_dir/backup-before-idx-$stamp.tar.gz" -C "$site_dir" .
crontab -l > "$deploy_dir/cron-before-idx-$stamp.txt" 2>/dev/null || true
umask 022
cp -r "$release_dir/dist/." "$site_dir/"
mkdir -p "$site_dir/api"
cp "$release_dir/server/listings.php" "$site_dir/api/listings.php"
chmod 644 "$site_dir/api/listings.php"
awk '!/nobleton-private\/idx\/sync\.php/' "$deploy_dir/cron-before-idx-$stamp.txt" > "$private_dir/idx-cron.new"
printf '\n*/15 * * * * %s /home/nvfglyl5/nobleton-private/idx/sync.php > /home/nvfglyl5/nobleton-private/idx-sync.log 2>&1\n' "$php_bin" >> "$private_dir/idx-cron.new"
crontab "$private_dir/idx-cron.new"
echo 'Nobleton IDX deployed; refresh runs every 15 minutes.'
echo "Rollback archive: backup-before-idx-$stamp.tar.gz"
