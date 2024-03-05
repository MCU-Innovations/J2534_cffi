from setuptools import setup
from setuptools_scm.version import guess_next_simple_semver, release_branch_semver_version


def custom_version_scheme(version):
  return f"{version.tag}.{version.distance}"

def custom_local_scheme(version):
    return "+dirty" if version.dirty else ""


setup(use_scm_version={
    'version_scheme': custom_version_scheme,
    'local_scheme': custom_local_scheme,
})