import time
from datetime import timedelta

import jwt


class JWTGenerator:
    def __init__(
        self,
        client_id,
        private_key,
        username,
        audience="https://login.salesforce.com",
        session_duration_hours=1,
    ):
        self.client_id = client_id
        self.private_key = private_key
        self.username = username
        self.audience = audience
        self.session_duration_hours = session_duration_hours

    def generate_token(self) -> str:
        current_time = int(time.time())
        expiration_time = str(
            current_time
            + int(timedelta(hours=self.session_duration_hours).total_seconds())
        )

        payload = {
            "iss": self.client_id,
            "sub": self.username,
            "aud": self.audience,
            "exp": expiration_time,
        }

        try:
            token = jwt.encode(payload, self.private_key, algorithm="RS256")
        except ValueError:
            token = ""

        return token
