try:
    from ._version import __VERSION__
except:
    import os
    from setuptools_scm import get_version
    def custom_version_scheme(version):
        return f"{version.tag}.{version.distance}"
    def custom_local_scheme(version):
        return "+dirty" if version.dirty else ""
    __VERSION__ = get_version(version_scheme=custom_version_scheme, local_scheme=custom_local_scheme, root=os.path.join(os.path.dirname(__file__), ".."))

from .registry import find_j2534_passthru_dlls
from .dll import J2534PassThru
