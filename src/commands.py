import functools
import json

serialize = json.dumps
deserialize = json.loads


def build_path(prefix, suffix):
  return '/zooteam/%s/%s' % (prefix, suffix)


def assert_exists(client, *args):
  for path in args:
    if not client.exists(path):
      raise RuntimeError('Node %s does not exist' % path)


def assert_not_exists(client, *args):
  for path in args:
    if client.exists(path):
      raise RuntimeError('Node %s exists already' % path)


def assert_free(client, *args):
  for path in args:
    data, stat = client.get(path)
    if data != '':
      raise RuntimeError('Player %s is occupied' % path)


def read(prefix, client, name):
  path = build_path(prefix, name)
  assert_exists(client, path)
  data, stat = client.get(path)
  return data


def add(prefix, client, name, value=''):
  path = build_path(prefix, name)
  assert_not_exists(client, path)
  return client.create(path, value, makepath=True)


def remove(prefix, client, name):
  path = build_path(prefix, name)
  assert_exists(client, path)
  client.delete(path)


def update(prefix, client, name, value=''):
  path = build_path(prefix, name)
  assert_exists(client, path)
  return client.set(path, str(value))


def make_team(client, team_name, *members):
  player_path_list = [build_path('players', member) for member in members]
  assert_exists(client, *player_path_list)
  teams = [data for data, stat in (client.get(path) for path in player_path_list)]
  if any(teams):
    raise RuntimeError('Not all players are available: %s' % filter(None, teams))

  # Do transaction here
  for member in members:
    update('players', client, member, team_name)

  payload = serialize(members)
  return add('teams', client, team_name, payload)


def drop_team(client, name):
  # Do transaction
  # Update players
  path = build_path('teams', name)
  assert_exists(client, path)
  team, stat = client.get(path)
  for member in deserialize(team):
    update('players', client, member)
  client.delete(path)


REGISTRY = {
  'player': functools.partial(read, 'players'),
  'team': functools.partial(read, 'teams'),
  'add_player': functools.partial(add, 'players'),
  'del_player': functools.partial(remove, 'players'),
  'make_team': make_team,
  'drop_team': drop_team,
}

def get_command(name):
  return REGISTRY.get(name)

