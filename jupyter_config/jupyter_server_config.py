# Configuration chargée si vous lancez Jupyter avec :
#   export JUPYTER_CONFIG_DIR="$(pwd)/jupyter_config"
# (voir run_jupyter.sh)
#
# Évite l’avertissement : websocket_ping_timeout ne peut pas dépasser
# websocket_ping_interval (Jupyter ajuste tout seul sinon).
from traitlets.config import get_config

c = get_config()

c.ServerApp.websocket_ping_interval = 30
c.ServerApp.websocket_ping_timeout = 30
