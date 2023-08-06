__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


def test_import():
    from biocgenerics.MetadataMixin import MetadataMixin

    assert MetadataMixin is not None
