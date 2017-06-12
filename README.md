# Players and teams on Zookeeper

Приложение позволяет управлять игроками и командами. Один игрок может состоять только в одной команде. В качастве хранилища используется Zookeeper.

## Example

Соберем образ и запусим сервис
```
docker build --tag zooteam .
docker run -d zooteam
```

Просмотреть справку
```
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py -h
```

Добавить игроков в команду
```
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py add_player ronaldo
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py add_player pele
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py make_team brazil ronaldo pele
```

Просмотреть состав команды и принадлежность игрока
```
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py team brazil
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py player pele
```

Удалить команду, и освободить игроков
```
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py drop_team brazil
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py player pele
```

Удалить свободного игрока
```
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py add_player foo
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py del_player foo
```

Создать новую команду
```
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py make_team all_stars ronaldo pele
```

### Обработка ошибок

Нельзя удалить то, что не существует; нельза создать то, что уже создано

Неудастся создать команду с игроком, уже занятым в другой команде
```
docker exec zooteam python /usr/local/lib/zooteam/zooteam.py make_team pele_only pele
ERROR:__main__:Not all players are available
```

## Открытые вопросы

- Перенести игрока из одной команды в другую
- Обеспечить транзакционность
- Обеспечить целостность при конкуррентных обновлениях
