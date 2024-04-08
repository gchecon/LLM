from dotenv import load_dotenv
import os


class EnvVars:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        try:
            load_dotenv(dotenv_path)
        except Exception as e:
            raise EnvVarsLoadError(f"Erro ao carregar o arquivo .env: {e}")

    @staticmethod
    def get(key, default=None):
        try:
            return os.getenv(key, default)
        except KeyError as e:
            raise EnvVarNotFoundError(f"Variável de ambiente não encontrada: {e}")


class EnvVarsLoadError(Exception):
    pass


class EnvVarNotFoundError(Exception):
    pass
