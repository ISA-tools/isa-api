# -*- coding: utf-8 -*
"""Convert ISA-Tab to MAGE-TAB"""
import logging

from isatools import isatab, magetab


log = logging.getLogger('isatools')


def convert(source_inv_fp, output_path):
    """ Converter for ISA-Tab to MAGE-TAB.
    :param source_inv_fp: File descriptor of input investigation file
    :param output_path: Path to directory to write output MAGE-TAB files to
    """
    log.info("loading isatab %s", source_inv_fp.name)
    ISA = isatab.load(source_inv_fp)
    log.info("dumping magetab %s", output_path)
    magetab.dump(ISA, output_path)
