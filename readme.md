# Эмулятор языка оболочки OC

Этот проект представляет собой эмулятор для языка оболочки OC, который позволяет пользователям взаимодействовать с виртуальной файловой системой, хранящейся в ZIP-архиве. Эмулятор поддерживает основные команды, такие как `ls`, `cd`, `cat`, `tree`, и `echo`, а также ведет журнал действий пользователей.

## Установка

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/ваш_логин/имя_репозитория.git
   cd имя_репозитория
   ```

2. Убедитесь, что у вас установлена версия Python 3.6 или выше.

3. Установите необходимые зависимости (если они есть):

   ```bash
   pip install -r requirements.txt
   ```

## Использование

### Запуск эмулятора

Чтобы запустить эмулятор, используйте следующую команду:

```bash
python emulator.py <user> <hostname> <vfs_zip> <log_file>
```

- `<user>`: имя пользователя.
- `<hostname>`: имя хоста.
- `<vfs_zip>`: путь к ZIP-файлу, содержащему виртуальную файловую систему.
- `<log_file>`: файл, в который будет записываться журнал действий.

### Поддерживаемые команды

- `ls [directory]`: выводит список файлов и папок в указанной директории (или в текущей, если не указана).
- `cd <directory>`: изменяет текущую директорию на указанную.
- `cat <file>`: выводит содержимое указанного файла.
- `tree`: выводит древовидную структуру файлов и папок текущей директории.
- `echo <text>`: выводит текст на экран.
- `exit`: завершает работу эмулятора.

### Пример использования

```bash
python emulator.py user1 localhost vfs.zip log.xml
```

После запуска вы можете вводить команды в эмуляторе:

```
user1@localhost:/home$ ls
documents/
pictures/
user1@localhost:/home$ cd documents
user1@localhost:/home/documents$ ls
file1.txt
file2.txt
user1@localhost:/home/documents$ cat file1.txt
Содержимое файла 1
user1@localhost:/home/documents$ tree
├── file1.txt
└── file2.txt
```

## Логирование

Все действия пользователей записываются в указанный файл журнала в формате XML. Это позволяет отслеживать историю команд и действий, выполненных в эмуляторе.
