from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE_PATH = BASE_DIR / 'deploy' / 'env' / '.env'