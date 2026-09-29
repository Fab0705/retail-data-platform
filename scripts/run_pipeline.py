import sys
from pathlib import Path

# Asegurar que Python encuentre el paquete 'src'
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.retail_platform.pipeline.pipeline import MasterPipeline

def main():
    # Inicializar y ejecutar el pipeline maestro
    pipeline = MasterPipeline(project_root)
    pipeline.run()

if __name__ == "__main__":
    main()