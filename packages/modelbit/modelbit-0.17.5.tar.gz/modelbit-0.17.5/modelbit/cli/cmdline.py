#!/usr/bin/env python3
import argparse
import logging
import os
import sys
from typing import Optional

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)


def cloneAction(target_folder: str, origin: Optional[str], **_) -> None:
  from .clone import clone
  clone(target_folder, origin=origin)


def versionAction(**_) -> None:
  from modelbit import __version__
  print(__version__)
  exit(0)


def cacheAction(command: str, **_) -> None:
  from . import secure_storage
  if command == "clear":
    secure_storage.clearCache()
  elif command == "list":
    from .. import ux
    headers = [
        ux.TableHeader("Workspace"),
        ux.TableHeader("Kind"),
        ux.TableHeader("Name"),
        ux.TableHeader("Size", alignment=ux.TableHeader.RIGHT)
    ]
    print(ux.renderTextTable(headers, secure_storage.getCacheList(), maxWidth=120))


def describeAction(filepath: str, depth: int, **_) -> None:
  from .describe import getObjectDescription
  print(getObjectDescription(filepath, depth))


def gitfilterAction(**_) -> None:
  from .filter import process
  process()


def initializeParser() -> argparse.ArgumentParser:
  visibleOptions: Optional[str] = '{clone,version}'
  if "-hh" in sys.argv:  # modelbit -hh to show full help
    visibleOptions = None
  parser = argparse.ArgumentParser(description="Modelbit CLI")
  subparsers = parser.add_subparsers(title='Actions', required=True, dest="action", metavar=visibleOptions)

  clone_parser = subparsers.add_parser('clone', help="Clone your modelbit repository via git")
  clone_parser.set_defaults(func=cloneAction)
  clone_parser.add_argument('target_folder', nargs='?', default="modelbit")
  clone_parser.add_argument(
      '--origin',
      metavar='{modelbit,github,gitlab,etc}',
      required=False,
      help=
      'Repository to clone. Set to modelbit, github, or gitlab to specify the remote to use. If not set, will show an interactive prompt'
  )

  subparsers.add_parser('version', help="Display modelbit package version").set_defaults(func=versionAction)

  cache_parser = subparsers.add_parser('cache')
  cache_parser.set_defaults(func=cacheAction)
  cache_parser.add_argument('command', choices=['list', 'clear'])

  describe_parser = subparsers.add_parser('describe')
  describe_parser.set_defaults(func=describeAction)
  describe_parser.add_argument('filepath', nargs='?')
  describe_parser.add_argument('-d', '--depth', default=1, type=int)

  filter_parser = subparsers.add_parser('gitfilter')
  filter_parser.set_defaults(func=gitfilterAction)
  filter_parser.add_argument('command', choices=['process'])
  return parser


def processArgs() -> None:
  parser = initializeParser()
  args = parser.parse_args()
  try:
    args.func(**vars(args))
  except TypeError as e:
    # Catch wrong number of args
    logger.info("Bad command line", exc_info=e)
    parser.print_help()
  except KeyboardInterrupt:
    exit(1)
  except Exception as e:
    raise
