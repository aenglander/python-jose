from jose.jwk import Key

import pytest


@pytest.fixture
def alg():
    return Key("key", "ALG")


class TestBaseAlgorithm:

    def test_sign_is_interface(self, alg):
        with pytest.raises(NotImplementedError):
            alg.sign('msg')

    def test_verify_is_interface(self, alg):
        with pytest.raises(NotImplementedError):
            alg.verify('msg', 'sig')

    def test_encrypt_is_interface(self, alg):
        with pytest.raises(NotImplementedError):
            alg.encrypt('plain text')

    def test_decrypt_is_interface(self, alg):
        with pytest.raises(NotImplementedError):
            alg.decrypt('plain text', iv='iv')
