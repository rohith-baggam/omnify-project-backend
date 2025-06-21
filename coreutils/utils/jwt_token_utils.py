import jwt
from datetime import datetime
import logging
from core.settings import logger
from typing import Dict

logger = logging.LoggerAdapter(logger, {"app_name": __name__})


class JwtTokenUtils:
    jwt_token: str

    def __init__(self, jwt_token: str):
        self.jwt_token = jwt_token

    def decrypt_jwt_token(self) -> Dict:
        """
        This method will decode the JWT token and return its payload without verifying its signature.
        """
        try:

            decoded_token: Dict = jwt.decode(
                self.jwt_token, options={"verify_signature": False}
            )

            return decoded_token
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return {}
        except jwt.DecodeError:
            logger.error("Invalid token")
            return {}
        except Exception as e:
            logger.error(f"An error occurred while decoding the token: {e}")
            return {}

    def is_token_expired(self) -> bool:
        """
        This method checks if the JWT token is expired.
        Returns True if expired, False otherwise.
        """
        try:
            # Decode the token to get the payload and check its expiration
            decoded_token = self.decrypt_jwt_token()
            exp_timestamp = decoded_token.get("exp")

            if exp_timestamp is None:
                logger.error("Token does not contain an expiration date.")

            # Check if the current time is past the expiration time
            expiration_time = datetime.utcfromtimestamp(exp_timestamp)
            return datetime.utcnow() > expiration_time

        except jwt.ExpiredSignatureError:
            return True
        except jwt.DecodeError:
            logger.error("Invalid token")
            return True
        except Exception as e:
            logger.error(f"An error occurred while checking expiration: {e}")
            return True
