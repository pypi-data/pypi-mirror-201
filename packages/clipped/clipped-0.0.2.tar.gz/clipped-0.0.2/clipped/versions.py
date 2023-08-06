def get_loose_version(vstring: str):
    try:
        from setuptools._distutils.version import LooseVersion
    except ImportError:
        from distutils.version import LooseVersion
    return LooseVersion(vstring)


def clean_version_for_compatibility(version: str):
    return "-".join(version.lstrip("v").replace(".", "-").split("-")[:3])


def clean_version_for_check(version: str):
    if not version:
        return version
    return ".".join(version.lstrip("v").replace("-", ".").split(".")[:3])


def compare_versions(current: str, reference: str, comparator: str) -> bool:
    current = get_loose_version(current)
    reference = get_loose_version(reference)

    if comparator == "=":
        return current == reference

    if comparator == "!=":
        return current != reference

    if comparator == "<":
        return current < reference

    if comparator == "<=":
        return current <= reference

    if comparator == ">":
        return current > reference

    if comparator == ">=":
        return current >= reference

    raise ValueError("Comparator `{}` is not supported.".format(comparator))
