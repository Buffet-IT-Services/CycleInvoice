"""Own faker providers."""
import secrets

from faker.providers import BaseProvider


class SwissUIDProvider(BaseProvider):
    """Faker provider for Swiss UID."""

    def swiss_uid(self) -> str:
        """Generate a Swiss UID using a secure PRNG for the digits."""
        digits = [str(secrets.randbelow(10)) for _ in range(9)]
        return (
            f"CHE-"
            f"{digits[0]}{digits[1]}{digits[2]}."
            f"{digits[3]}{digits[4]}{digits[5]}."
            f"{digits[6]}{digits[7]}{digits[8]}"
        )
