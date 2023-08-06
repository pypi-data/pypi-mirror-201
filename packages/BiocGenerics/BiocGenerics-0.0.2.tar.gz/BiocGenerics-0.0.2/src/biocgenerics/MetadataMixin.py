from typing import Optional, MutableMapping

from collections import Mapping

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class MetadataMixin:
    """Mixin class to manage metadata property.
    """

    @property
    def metadata(self) -> Optional[MutableMapping]:
        """Access metadata.

        Returns:
            Optional[MutableMapping]: metadata object if available, 
                usually a dict-like object.
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: MutableMapping):
        """Set new metadata.

        Args:
            metadata (MutableMapping): new metadata object.

        Raises:
            TypeError: if `metadata` is not a dict-like object.
        """
        if not isinstance(metadata, Mapping):
            raise TypeError("metadata must be a dict-like object.")

        self._metadata = metadata

    @metadata.deleter
    def metadata(self):
        """Remove metadata.

        Note: Doesn't really remove from the instance, sets metadata to `None`.
        """
        self._metadata = None
