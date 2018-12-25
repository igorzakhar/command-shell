# Shell
Тестовое задание [https://github.com/peterservice-rnd/new-job/blob/master/shell.md](https://github.com/peterservice-rnd/new-job/blob/master/shell.md)
#### Задача

Необходимо реализовать shell с поддержкой следующих возможностей:

- [ ] Задание переменных окружения
- [x] Навигация по файловой системе: cd, ls
- [x] Работа с данными (файлы, потоки): cat, echo, grep
- [ ] Перенаправление потоков: `cat file.txt > anotherfile.txt`
- [ ] Пайпы: `ls | grep vimrc`
- [x] Выход по `ctrl-d` и команде `exit`
- [x] История команд

#### Пример работы:

```sh
~$ ./ps-shell
~> cd /tmp
/tmp> ls
file1
file2
/tmp> cat file1 | grep cat
cat
mocat
/tmp>
```

# Цели проекта

Код написан в образовательных целях.
