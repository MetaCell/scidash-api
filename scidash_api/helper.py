import logging

logger = logging.getLogger(__name__)


def deprecated(method_name, will_be_removed, replacement, strict=False):

    logger.warning(
            "Method {} deprecated"
            " and will be removed in version {}"
            " please, use {} instead".format(method_name, will_be_removed,
                replacement)
            )
