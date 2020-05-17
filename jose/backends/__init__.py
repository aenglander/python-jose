
try:
    from jose.backends.cryptography_backend import CryptographyRSAKey as RSAKey  # noqa: F401
except ImportError:
    try:
        from jose.backends.pycrypto_backend import RSAKey  # noqa: F401

        # time.clock was deprecated in python 3.3 in favor of time.perf_counter
        # and removed in python 3.8. pycrypto was never updated for this. If
        # time has no clock, lt it use perf_counter instead to work in 3.8+
        try:
            # noinspection PyUnresolvedReferences
            import time
            if not hasattr(time, "clock"):
                time.clock = time.perf_counter
        except ImportError:
            pass

    except ImportError:
        from jose.backends.rsa_backend import RSAKey  # noqa: F401

try:
    from jose.backends.cryptography_backend import CryptographyECKey as ECKey  # noqa: F401
except ImportError:
    from jose.backends.ecdsa_backend import ECDSAECKey as ECKey  # noqa: F401
