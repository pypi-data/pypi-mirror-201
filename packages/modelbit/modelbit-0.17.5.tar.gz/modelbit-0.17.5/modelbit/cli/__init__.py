#!/usr/bin/env python3

import logging
import os

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)


def main() -> None:
  from . import cmdline
  cmdline.processArgs()


if __name__ == '__main__':
  main()
