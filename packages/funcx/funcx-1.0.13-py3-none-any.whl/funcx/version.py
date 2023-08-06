from packaging.version import Version

from funcx.errors import VersionMismatch

# single source of truth for package version,
# see https://packaging.python.org/en/latest/single_source_version/
__version__ = "1.0.13"


def compare_versions(
    current: str, min_version: str, *, package_name: str = "funcx"
) -> None:
    current_v = Version(current)
    min_v = Version(min_version)

    if (
        current_v.is_devrelease
        or min_v.is_devrelease
        and current_v.release == min_v.release
    ):
        return

    if current_v < min_v:
        raise VersionMismatch(
            f"Your version={current} is lower than the "
            f"minimum version for {package_name}: {min_version}.  "
            "Please update. "
            f"pip install {package_name}>={min_version}"
        )
