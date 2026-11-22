import sys
from pathlib import Path

# Agrega la raiz para que pytest encuentre los modulos del proyecto.
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))
