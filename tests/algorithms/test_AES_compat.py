import pytest

try:
    from jose.backends.pycrypto_backend import AESKey as PyCryptoAESKey
    from jose.backends.cryptography_backend import CryptographyAESKey
except ImportError:
    PyCryptoAESKey = CryptographyAESKey = None
from jose.exceptions import JWEError
from jose.constants import ALGORITHMS

CRYPTO_BACKENDS = (
    pytest.param(CryptographyAESKey, id="pyca/cryptography"),
    pytest.param(PyCryptoAESKey, id="pycrypto/dome"),
)

SUPPORTED_ALGORITHMS = filter(lambda x: x in ALGORITHMS.SUPPORTED,
                              ALGORITHMS.AES_ENC)


@pytest.mark.backend_compatibility
@pytest.mark.skipif(
    None in (CryptographyAESKey, PyCryptoAESKey),
    reason="Multiple crypto backends not available for backend compatibility tests"
)
class TestBackendAesCompatibility(object):
    @pytest.mark.parametrize("backend_encrypt", CRYPTO_BACKENDS)
    @pytest.mark.parametrize("backend_decrypt", CRYPTO_BACKENDS)
    @pytest.mark.parametrize("algorithm", SUPPORTED_ALGORITHMS)
    def test_encryption_parity(self, backend_encrypt, backend_decrypt, algorithm):
        if "128" in algorithm:
            key = b"8slRzzty6dKMaFCP"
        elif "192" in algorithm:
            key = b"8slRzzty6dKMaFCP8slRzzty"
        else:
            key = b"8slRzzty6dKMaFCP8slRzzty6dKMaFCP"

        key_encrypt = backend_encrypt(key, algorithm)
        key_decrypt = backend_decrypt(key, algorithm)

        plain_text = b'test'
        aad = b"extra data" if "GCM" in algorithm else None

        iv, cipher_text, tag = key_encrypt.encrypt(plain_text, aad)

        # verify decrypt to original plain text
        actual = key_decrypt.decrypt(cipher_text, iv, aad, tag)
        assert actual == plain_text

        with pytest.raises(JWEError):
            key_decrypt.decrypt(b'n' * 64)
