#!/usr/bin/env python
import argparse
import logging
import sys

from kazoo.client import KazooClient

import commands

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_client(hosts):
  zk = KazooClient(hosts)
  zk.start()
  return zk


def main(cmd_name, *args):
  cmd = commands.get_command(cmd_name)
  if cmd is None:
    logger.error('Unknown command %s', cmd)
    return 1

  zk = get_client('localhost')
  result = cmd(zk, *args)
  if result is not None:
    print(result)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('command', help='One of actions to perform', choices=commands.REGISTRY)
  parser.add_argument('params', help='Name of player or team name followed by players to assign to', nargs='+')
  args = parser.parse_args()

  try:
    exit(main(args.command, *args.params))
  except RuntimeError as ex:
    logger.error(ex)
    exit(1)
