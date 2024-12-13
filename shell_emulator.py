import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from io import StringIO

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.zip_ref = zipfile.ZipFile(zip_path, 'r')

    def list_dir(self, path):
        files = self.zip_ref.namelist()
        dir_content = set()
        for file in files:
            if file.startswith(path) and file != path:
                relative_path = file[len(path):].lstrip('/')
                if '/' in relative_path:
                    dir_content.add(relative_path.split('/', 1)[0])
                else:
                    dir_content.add(relative_path)
        return sorted(dir_content)

    def change_dir(self, current_dir, path):
        # Если путь начинается с '/', то это абсолютный путь
        if path.startswith('/'):
            full_path = path
        else:
            # Иначе это относительный путь, объединяем с текущей директорией
            full_path = os.path.join(current_dir, path).replace('\\', '/')

        # Проверяем, существует ли директория
        if any(file.startswith(full_path) and file != full_path for file in self.zip_ref.namelist()):
            return full_path
        else:
            raise FileNotFoundError(f"Directory not found: {path}")

    def read_file(self, path):
        if path in self.zip_ref.namelist():
            with self.zip_ref.open(path) as file:
                return file.read().decode('utf-8')
        else:
            raise FileNotFoundError(f"File not found: {path}")

    def print_tree(self, path, level=0):
        tree_str = StringIO()
        indent = ' ' * level * 2
        files = self.list_dir(path)
        for file in files:
            file_path = os.path.join(path, file).replace('\\', '/')
            if any(f.startswith(file_path) and f != file_path for f in self.zip_ref.namelist()):
                tree_str.write(f"{indent}├── {file}/\n")
                tree_str.write(self.print_tree(file_path, level + 1))
            else:
                tree_str.write(f"{indent}├── {file}\n")
        return tree_str.getvalue()

def log_action(log_file, user, action):
    if not os.path.exists(log_file):
        root = ET.Element("log")
    else:
        root = ET.parse(log_file).getroot()

    action_elem = ET.SubElement(root, "action")
    action_elem.set("user", user)
    action_elem.set("timestamp", datetime.now().isoformat())
    action_elem.text = action

    ET.ElementTree(root).write(log_file, encoding='utf-8', xml_declaration=True)

def main(user, hostname, vfs_zip, log_file):
    vfs = VirtualFileSystem(vfs_zip)
    current_dir = ""  # Начальная директория - корневая

    while True:
        try:
            prompt = f"{user}@{hostname}:{current_dir}$ "
            command = input(prompt)

            if command == "exit":
                break

            parts = command.split()
            cmd = parts[0]

            if cmd == "ls":
                if len(parts) > 1:
                    files = vfs.list_dir(os.path.join(current_dir, parts[1]).replace('\\', '/'))
                else:
                    files = vfs.list_dir(current_dir)
                print("\n".join(files))
                log_action(log_file, user, f"ls {' '.join(parts[1:]) if len(parts) > 1 else current_dir}")

            elif cmd == "cd":
                if len(parts) != 2:
                    print("Usage: cd <directory>")
                else:
                    try:
                        current_dir = vfs.change_dir(current_dir, parts[1])
                        log_action(log_file, user, f"cd {parts[1]}")
                    except FileNotFoundError as e:
                        print(e)

            elif cmd == "cat":
                if len(parts) != 2:
                    print("Usage: cat <file>")
                else:
                    try:
                        content = vfs.read_file(os.path.join(current_dir, parts[1]).replace('\\', '/'))
                        print(content)
                        log_action(log_file, user, f"cat {parts[1]}")
                    except FileNotFoundError as e:
                        print(e)

            elif cmd == "tree":
                print(vfs.print_tree(current_dir))
                log_action(log_file, user, "tree")

            elif cmd == "echo":
                print(" ".join(parts[1:]))
                log_action(log_file, user, f"echo {' '.join(parts[1:])}")

            else:
                print(f"Unknown command: {cmd}")

        except Exception as e:
            print(f"Error: {e}")
            log_action(log_file, user, f"error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python emulator.py <user> <hostname> <vfs_zip> <log_file>")
        sys.exit(1)

    user = sys.argv[1]
    hostname = sys.argv[2]
    vfs_zip = sys.argv[3]
    log_file = sys.argv[4]

    main(user, hostname, vfs_zip, log_file)
    