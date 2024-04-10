import dotenv
import os


class ENV:
    env = {}

    @staticmethod
    def load_env() -> None:
        dotenv.load_dotenv()

        ENV.env = {'NATURE_BOUNDARY_X': int(os.getenv('NATURE_BOUNDARY_X')), 'NATURE_BOUNDARY_Y': int(os.getenv('NATURE_BOUNDARY_Y')),
                   'ALPHA_A': float(os.getenv('ALPHA_A')), 'ALPHA_B': float(os.getenv('ALPHA_B')), 'LAMBDA_A': float(os.getenv('LAMBDA_A')),
                   'LAMBDA_B': float(os.getenv('LAMBDA_B')), 'BETA_A': float(os.getenv('BETA_A')), 'BETA_B': float(os.getenv('BETA_B'))}

    @staticmethod
    def get(key: str) -> any:
        return ENV.env[key]
