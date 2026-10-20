#!/bin/bash
# =============================================================================
# JARVIS MASTER INSTALLER — AI Builds AI
# AI Jarvis Assistants Swarms Systems
# Intergalactic Corporate Services LLC
# aievolutionaryevolutions.com
# =============================================================================
# ONE COMMAND:
#   bash <(curl -s https://raw.githubusercontent.com/lippytm/AI-Jarvis-Assistant-AI-Copilot-for-Self-Healing-and-Self-Improvements-for-all-Repositories-/main/scripts/jarvis-master-install.sh)
# =============================================================================

set -e
DOMAIN="aievolutionaryevolutions.com"
JARVIS_PORT=3001
N8N_PORT=5678
REPO_URL="https://github.com/lippytm/aievolutionaryevolutions.com-Hermes-Fabric-MemPalace-.git"
INSTALL_DIR="$HOME/jarvis"
LOG_FILE="$HOME/jarvis-install.log"
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'
log()  { echo -e "${GREEN}[JARVIS]${NC} $1" | tee -a "$LOG_FILE"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"; }

echo "$(date): Jarvis Install started" >> "$LOG_FILE"
echo -e "${CYAN}${BOLD}JARVIS AI SWARMS — ALL 5 PHASES${NC}"

# PHASE 1
log "Phase 1: VPS Foundation"
apt-get update -qq && apt-get upgrade -y -qq
apt-get install -y -qq git curl wget unzip nginx certbot python3-certbot-nginx ufw
curl -fsSL https://deb.nodesource.com/setup_20.x | bash - >> "$LOG_FILE" 2>&1
apt-get install -y -qq nodejs
npm install -g pm2 >> "$LOG_FILE" 2>&1
ufw --force enable >> "$LOG_FILE" 2>&1; ufw allow OpenSSH >> "$LOG_FILE" 2>&1; ufw allow 'Nginx Full' >> "$LOG_FILE" 2>&1
mkdir -p "$INSTALL_DIR"
[ -d "$INSTALL_DIR/mempalace" ] && (cd "$INSTALL_DIR/mempalace" && git pull) || git clone "$REPO_URL" "$INSTALL_DIR/mempalace"
cd "$INSTALL_DIR/mempalace" && npm install >> "$LOG_FILE" 2>&1
[ ! -f .env ] && cat > .env << EOF
PORT=$JARVIS_PORT
HOST=0.0.0.0
NODE_ENV=production
DOMAIN=$DOMAIN
MCP_ENABLED=true
ANTHROPIC_API_KEY=your-claude-key
OPENAI_API_KEY=your-openai-key
GEMINI_API_KEY=your-gemini-key
EOF
pm2 delete jarvis 2>/dev/null || true
pm2 start server.js --name jarvis --env production >> "$LOG_FILE" 2>&1 && pm2 save
log "Phase 1 DONE — MemPalace on :$JARVIS_PORT"

# PHASE 2
log "Phase 2: Nginx + Subdomains + SSL"
cat > /etc/nginx/sites-available/jarvis.conf << NGINXEOF
server { listen 80; server_name jarvis.$DOMAIN; location / { proxy_pass http://localhost:$JARVIS_PORT; proxy_http_version 1.1; proxy_set_header Upgrade \$http_upgrade; proxy_set_header Connection upgrade; proxy_set_header Host \$host; } }
server { listen 80; server_name n8n.$DOMAIN; location / { proxy_pass http://localhost:$N8N_PORT; proxy_http_version 1.1; proxy_set_header Upgrade \$http_upgrade; proxy_set_header Connection upgrade; proxy_set_header Host \$host; } }
server { listen 80; server_name books.$DOMAIN; root /var/www/books; index index.html; }
server { listen 80; server_name affiliate.$DOMAIN; root /var/www/affiliate; index index.html; }
server { listen 80; server_name content.$DOMAIN; root /var/www/content; index index.html; }
server { listen 80; server_name academy.$DOMAIN; root /var/www/academy; index index.html; }
server { listen 80; server_name api.$DOMAIN; location / { proxy_pass http://localhost:$JARVIS_PORT/api; } }
server { listen 80; server_name dash.$DOMAIN; root /var/www/dash; index index.html; }
NGINXEOF
for d in books affiliate content academy dash; do mkdir -p /var/www/$d; echo "<h1>$d.$DOMAIN</h1>" > /var/www/$d/index.html; done
ln -sf /etc/nginx/sites-available/jarvis.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
certbot --nginx -d jarvis.$DOMAIN -d n8n.$DOMAIN -d books.$DOMAIN -d affiliate.$DOMAIN -d content.$DOMAIN -d academy.$DOMAIN -d api.$DOMAIN -d dash.$DOMAIN --non-interactive --agree-tos --email support@intergalacticcorporateservices.com --redirect >> "$LOG_FILE" 2>&1 || warn "SSL warnings—check DNS"
log "Phase 2 DONE — 8 subdomains + SSL"

# PHASE 3
log "Phase 3: n8n Automation Engine"
npm install -g n8n >> "$LOG_FILE" 2>&1
N8N_PASS="JarvisSwarm$(date +%Y)!"
N8N_KEY=$(openssl rand -hex 16)
cat > "$HOME/.n8n-env" << N8NEOF
export N8N_HOST=n8n.$DOMAIN
export N8N_PORT=$N8N_PORT
export N8N_PROTOCOL=https
export WEBHOOK_URL=https://n8n.$DOMAIN/
export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER=jarvis-admin
export N8N_BASIC_AUTH_PASSWORD=$N8N_PASS
export N8N_ENCRYPTION_KEY=$N8N_KEY
N8NEOF
source "$HOME/.n8n-env"
echo "source $HOME/.n8n-env" >> "$HOME/.bashrc"
pm2 delete n8n-jarvis 2>/dev/null || true
pm2 start n8n --name n8n-jarvis -- start >> "$LOG_FILE" 2>&1 && pm2 save
log "Phase 3 DONE — n8n on :$N8N_PORT (user: jarvis-admin / pass: $N8N_PASS)"

# PHASE 4
log "Phase 4: Deploy Key + Blotato MCP"
[ ! -f ~/.ssh/jarvis_deploy ] && ssh-keygen -t ed25519 -C "jarvis@$DOMAIN" -f ~/.ssh/jarvis_deploy -N ""
echo ""; echo "=== ADD TO GITHUB DEPLOY KEYS ==="; cat ~/.ssh/jarvis_deploy.pub; echo "================================"
MCP=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$JARVIS_PORT/mcp 2>/dev/null || echo 0)
[ "$MCP" != "0" ] && log "MCP live: https://jarvis.$DOMAIN/mcp — paste into Blotato Settings"
log "Phase 4 DONE"

# PHASE 5
log "Phase 5: Autonomous Loops"
pm2 install pm2-logrotate >> "$LOG_FILE" 2>&1
pm2 set pm2-logrotate:max_size 100M; pm2 set pm2-logrotate:retain 7
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet") | sort -u | crontab -
log "Phase 5 DONE — crons + log rotation active"

pm2 list
echo ""
echo "ALL 5 PHASES COMPLETE — JARVIS SWARM ONLINE"
echo "  MemPalace: https://jarvis.$DOMAIN"
echo "  n8n:       https://n8n.$DOMAIN  (jarvis-admin / $N8N_PASS)"
echo "  MCP:       https://jarvis.$DOMAIN/mcp"
echo "  API keys:  nano ~/jarvis/mempalace/.env"
echo "$(date): Install COMPLETE" >> "$LOG_FILE"
