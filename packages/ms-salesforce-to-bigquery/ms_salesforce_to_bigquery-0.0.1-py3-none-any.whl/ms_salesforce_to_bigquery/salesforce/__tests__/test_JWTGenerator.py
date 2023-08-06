import time
import unittest

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

from ms_salesforce_to_bigquery.salesforce.JWTGenerator import JWTGenerator


class TestJWTGenerator(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()

    def test_generate_token(self):
        client_id = "example_client_id"
        username = "example_username"
        audience = "https://login.salesforce.com"

        jwt_generator = JWTGenerator(
            client_id, self.private_key, username, audience
        )

        token = jwt_generator.generate_token()
        self.assertIsNotNone(token)

        # Verify that the generated token has the correct data
        decoded_payload = jwt.decode(
            token, self.public_key, algorithms="RS256", audience=audience
        )
        self.assertEqual(decoded_payload["iss"], client_id)
        self.assertEqual(decoded_payload["sub"], username)
        self.assertEqual(decoded_payload["aud"], audience)

    def test_generate_token_with_custom_session_duration(self):
        client_id = "example_client_id"
        username = "example_username"
        audience = "https://login.salesforce.com"
        session_duration_hours = 2

        jwt_generator = JWTGenerator(
            client_id,
            self.private_key,
            username,
            audience,
            session_duration_hours,
        )

        token = jwt_generator.generate_token()
        self.assertIsNotNone(token)

        # Verify that the generated token has the correct data
        decoded_payload = jwt.decode(
            token, self.public_key, algorithms="RS256", audience=audience
        )
        self.assertEqual(decoded_payload["iss"], client_id)
        self.assertEqual(decoded_payload["sub"], username)
        self.assertEqual(decoded_payload["aud"], audience)

        # Verify that the token has the custom session duration
        token_duration_seconds = int(decoded_payload["exp"]) - int(time.time())
        self.assertAlmostEqual(
            token_duration_seconds, session_duration_hours * 3600, delta=10
        )
