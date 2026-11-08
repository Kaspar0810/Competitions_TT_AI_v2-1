# # db_setup.py или в начале main_AI.py
# import sys
# import os, csv
# import subprocess
# from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QLineEdit, QFormLayout, QHBoxLayout
# from PyQt5.QtCore import Qt
# from models import db, Title, Region, Patronymic, Coach, Players_full, City, Referee  # импортируйте вашу БД и модели
# from import_initial_data import InitialDataImportDialog

# def offer_initial_import(self):
#     """Предлагает пользователю загрузить данные из экспортированных таблиц."""
#     reply = QMessageBox.question(
#         self,
#         "Импорт начальных данных",
#         "База данных создана. Хотите загрузить данные из таблиц,\n"
#         "экспортированных из MySQL Workbench?",
#         QMessageBox.Yes | QMessageBox.No,
#         QMessageBox.Yes
#     )
#     if reply != QMessageBox.Yes:
#         return

#     folder = QFileDialog.getExistingDirectory(
#         self, "Выберите папку с экспортированными таблицами (*.csv)"
#     )
#     if not folder:
#         return

#     # Порядок важен: сначала справочники, потом зависимые таблицы
#     # (иначе будут нарушены внешние ключи)
#     tables_in_order = [
#         ("Coachs.csv", Coach),
#         ("Patronymic.csv", Patronymic),
#         ("Citys.csv", City),
#         ("Players_full.csv", Players_full),
#         ("Referee.csv", Referee),
#         # добавьте остальные в правильном порядке
#     ]

#     imported, skipped = [], []
#     with db.atomic():  # транзакция peewee — либо всё, либо ничего
#         for filename, model in tables_in_order:
#             path = os.path.join(folder, filename)
#             if not os.path.exists(path):
#                 skipped.append(filename)
#                 continue

#             # читаем CSV, у которого первая строка — заголовки
#             with open(path, encoding="utf-8-sig", newline="") as f:
#                 reader = csv.DictReader(f)
#                 rows = [self._normalize_row(r, model) for r in reader]
#                 if rows:
#                     model.insert_many(rows).execute()
#             imported.append(filename)

#     msg = f"Импортировано: {len(imported)} файлов."
#     if skipped:
#         msg += "\nПропущены (нет файла): " + ", ".join(skipped)
#     QMessageBox.information(self, "Готово", msg)

# def _normalize_row(self, row, model):
#     """Приводит пустые строки вроде '' или 'NULL' к None."""
#     result = {}
#     for field in model._meta.fields:
#         name = field.name
#         val = row.get(name)
#         if val is None or val == "" or val.upper() == "NULL":
#             result[name] = None
#         else:
#             result[name] = val
#     return result

# def check_database_connection():
#     """Проверяет подключение к БД и наличие таблиц."""
#     try:
#         db.connect()
#         # Проверяем, существует ли хотя бы одна таблица
#         db.execute_sql('SELECT 1')
#         # Проверяем, есть ли таблицы (например, Title)
#         if Title.table_exists():
#             return True
#         else:
#             # Таблицы не созданы, но подключение есть
#             return True
#     except Exception as e:
#         print(f"Ошибка подключения к БД: {e}")
#         return False
#     finally:
#         if not db.is_closed():
#             db.close()

# def run_mysql_installer():
#     """Запускает диалог выбора установщика MySQL и запускает его."""
#     installer_path, _ = QFileDialog.getOpenFileName(
#         None,
#         "Выберите установщик MySQL",
#         os.path.expanduser("~"),
#         "Executable files (*.exe *.msi);;All files (*.*)"
#     )
#     if installer_path:
#         try:
#             # Запускаем установщик
#             # subprocess.Popen([installer_path])
#             subprocess.Popen(["msiexec", "/i", r"installer_path\mysql-installer.msi"])
#             QMessageBox.information(None, "Установка MySQL", 
#                                     "Установщик MySQL запущен.\n"
#                                     "После завершения установки перезапустите приложение.")
#             return True
#         except Exception as e:
#             QMessageBox.critical(None, "Ошибка", f"Не удалось запустить установщик: {e}")
#             return False
#     return False

# def get_mysql_credentials():
#     """Диалог для ввода логина и пароля MySQL."""
#     dialog = QDialog()
#     dialog.setWindowTitle("Настройка подключения к MySQL")
#     layout = QVBoxLayout(dialog)
#     layout.addWidget(QLabel("Введите данные для подключения к MySQL:"))
    
#     form = QFormLayout()
#     login_edit = QLineEdit()
#     login_edit.setText("root")
#     password_edit = QLineEdit()
#     password_edit.setEchoMode(QLineEdit.Password)
#     form.addRow("Логин:", login_edit)
#     form.addRow("Пароль:", password_edit)
#     layout.addLayout(form)
    
#     btn_layout = QHBoxLayout()
#     ok_btn = QPushButton("Подключиться")
#     cancel_btn = QPushButton("Отмена")
#     btn_layout.addWidget(ok_btn)
#     btn_layout.addWidget(cancel_btn)
#     layout.addLayout(btn_layout)
    
#     result = None
#     def on_ok():
#         nonlocal result
#         result = (login_edit.text(), password_edit.text())
#         dialog.accept()
#     ok_btn.clicked.connect(on_ok)
#     cancel_btn.clicked.connect(dialog.reject)
    
#     if dialog.exec_() == QDialog.Accepted:
#         return result
#     return None

# def setup_database():
#     """Основная функция настройки БД при запуске."""
#     if check_database_connection():
#         # Проверяем, нужно ли импортировать начальные данные
#         if should_import_initial_data():
#             dialog = InitialDataImportDialog()
#             if dialog.exec_() == QDialog.Accepted:
#                 print("Начальные данные импортированы")
#         return True
    
#     # Нет подключения
#     reply = QMessageBox.question(
#         None,
#         "База данных не найдена",
#         "Не удалось подключиться к MySQL.\n\n"
#         "Установить MySQL сейчас?",
#         QMessageBox.Yes | QMessageBox.No
#     )
#     if reply == QMessageBox.Yes:
#         # Предлагаем выбрать установщик
#         if run_mysql_installer():
#             # После установки просим перезапустить приложение
#             QMessageBox.information(None, "Перезапуск", 
#                                     "После установки MySQL нажмите ОК для продолжения.\n"
#                                     "Если установка не завершена, приложение будет закрыто.")
#             # Пробуем снова подключиться
#             if check_database_connection():
#                 return True
#             else:
#                 # Запрашиваем логин/пароль
#                 creds = get_mysql_credentials()
#                 if creds:
#                     # Обновляем параметры подключения в models.py
#                     from models import update_db_credentials
#                     update_db_credentials(creds[0], creds[1])
#                     if check_database_connection():
#                         offer_initial_import()
#                         return True
#         else:
#             QMessageBox.critical(None, "Ошибка", "Установка MySQL не выполнена.")
#     else:
#         QMessageBox.critical(None, "Ошибка", "Приложение не может работать без MySQL.\n"
#                              "Установите MySQL и настройте подключение, затем перезапустите программу.")
#     return False

# def should_import_initial_data():
#         """Проверяет, есть ли данные в справочных таблицах"""
#         try:
#             # Проверяем, пусты ли основные справочники
#             regions_count = Region.select().count()
#             patronymics_count = Patronymic.select().count()
#             coaches_count = Coach.select().count()
            
#             if regions_count == 0 or patronymics_count == 0 or coaches_count == 0:
#                 return True
#             return False
#         except:
#             return True

# db_setup.py
import os
import json
import pymysql

CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "db_config.json"
)

DEFAULT_CONFIG = {
    "user": "root",
    "password": "db_pass",
    "host": "localhost",
    "port": 3306,
    "database": "mysql_db",
}


def load_db_config():
    """Читает конфиг БД из файла. При отсутствии — дефолт."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
            # дополнить дефолтами недостающие поля
            for k, v in DEFAULT_CONFIG.items():
                cfg.setdefault(k, v)
            return cfg
        except Exception:
            pass
    return dict(DEFAULT_CONFIG)


def save_db_config(cfg):
    """Сохраняет конфиг БД в файл."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def check_mysql_connection(cfg=None):
    """Проверяет подключение к серверу MySQL (без базы)."""
    if cfg is None:
        cfg = load_db_config()
    try:
        conn = pymysql.connect(
            user=cfg["user"], password=cfg["password"],
            host=cfg["host"], port=cfg["port"],
            connect_timeout=5,
        )
        conn.close()
        return True, ""
    except pymysql.err.OperationalError as e:
        code = e.args[0] if e.args else 0
        if code == 1045:
            return False, "Неверный логин или пароль MySQL."
        if code == 2003:
            return False, "MySQL-сервер не запущен или недоступен."
        return False, f"Ошибка MySQL: {e}"
    except Exception as e:
        return False, f"Ошибка подключения: {e}"


def ensure_database(cfg=None):
    """Создаёт базу данных, если её нет."""
    if cfg is None:
        cfg = load_db_config()
    try:
        conn = pymysql.connect(
            user=cfg["user"], password=cfg["password"],
            host=cfg["host"], port=cfg["port"], charset="utf8mb4",
        )
        cur = conn.cursor()
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{cfg['database']}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
        cur.close()
        conn.close()
        return True, ""
    except Exception as e:
        return False, f"Не удалось создать базу: {e}"


def ensure_tables():
    """Создаёт все таблицы через peewee.create_tables (safe=True)."""
    try:
        from models import (
            db, init_from_config,
            Title, Coach, Region, City, Patronymic, Player, Players_full,
            Players_double, System, Choice, Delete_player, Result,
            Referee, Team, Choice_Team, Game_list,
            Choice_double_player, GskMember,
        )
        init_from_config()  # гарантируем актуальные параметры db
        if not db.is_closed():
            db.close()
        db.connect()

        db.create_tables([
            Title, Coach, Region, City, Patronymic, Player, Players_full,
            Players_double, System, Choice, Delete_player, Result,
            Referee, Team, Choice_Team, Game_list,
            Choice_double_player, GskMember,
        ], safe=True)
        return True, ""
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, f"Не удалось создать таблицы: {e}"


# ==================== ДИАЛОГ ПОДКЛЮЧЕНИЯ ====================

def _make_mysql_dialog(cfg, error_msg, parent):
    from PyQt5.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
        QLineEdit, QSpinBox, QFormLayout, QMessageBox
    )

    class MySQLConnectionDialog(QDialog):
        def __init__(self):
            super().__init__(parent)
            self.setWindowTitle("Подключение к MySQL")
            self.setModal(True)
            self.setMinimumWidth(480)

            layout = QVBoxLayout(self)

            if error_msg:
                err = QLabel(f"⚠ {error_msg}")
                err.setStyleSheet(
                    "color:#b00; background:#fff3e0; padding:8px; "
                    "border-radius:4px; font-weight:bold;"
                )
                err.setWordWrap(True)
                layout.addWidget(err)

            hint = QLabel(
                "Убедитесь, что MySQL установлен и служба запущена.\n"
                "Стандартные параметры: localhost, порт 3306."
            )
            hint.setStyleSheet("color:#333; background:#f5f5f5; padding:8px; "
                               "border-radius:4px;")
            hint.setWordWrap(True)
            layout.addWidget(hint)

            form = QFormLayout()
            self.user_edit = QLineEdit(cfg.get("user", "root"))
            self.pass_edit = QLineEdit(cfg.get("password", ""))
            self.pass_edit.setEchoMode(QLineEdit.Password)
            self.host_edit = QLineEdit(cfg.get("host", "localhost"))
            self.port_spin = QSpinBox()
            self.port_spin.setRange(1, 65535)
            self.port_spin.setValue(int(cfg.get("port", 3306)))
            self.db_edit = QLineEdit(cfg.get("database", "mysql_db"))

            form.addRow("Пользователь:", self.user_edit)
            form.addRow("Пароль:", self.pass_edit)
            form.addRow("Хост:", self.host_edit)
            form.addRow("Порт:", self.port_spin)
            form.addRow("Имя базы:", self.db_edit)
            layout.addLayout(form)

            btn = QHBoxLayout()
            help_btn = QPushButton("❓ Как установить MySQL")
            help_btn.clicked.connect(self._show_help)
            btn.addWidget(help_btn)
            btn.addStretch()

            test_btn = QPushButton("🔌 Проверить")
            test_btn.clicked.connect(self._test)
            btn.addWidget(test_btn)

            ok_btn = QPushButton("OK")
            ok_btn.setStyleSheet("background:#4CAF50; color:white; "
                                 "padding:6px 14px; font-weight:bold;")
            ok_btn.clicked.connect(self._ok)
            btn.addWidget(ok_btn)

            cancel_btn = QPushButton("Отмена")
            cancel_btn.clicked.connect(self.reject)
            btn.addWidget(cancel_btn)

            layout.addLayout(btn)

        def get_config(self):
            return {
                "user": self.user_edit.text().strip() or "root",
                "password": self.pass_edit.text(),
                "host": self.host_edit.text().strip() or "localhost",
                "port": self.port_spin.value(),
                "database": self.db_edit.text().strip() or "mysql_db",
            }

        def _test(self):
            ok, err = check_mysql_connection(self.get_config())
            if ok:
                QMessageBox.information(self, "Успех",
                                        "Подключение к MySQL работает.")
            else:
                QMessageBox.warning(self, "Ошибка", err)

        def _ok(self):
            ok, err = check_mysql_connection(self.get_config())
            if not ok:
                QMessageBox.warning(self, "Ошибка подключения", err)
                return
            self.accept()

        def _show_help(self):
            QMessageBox.information(self, "Как установить MySQL",
                "1. Скачайте MySQL Community Server:\n"
                "   https://dev.mysql.com/downloads/installer/\n\n"
                "2. Запустите установщик → «Developer Default».\n"
                "3. Придумайте и запомните пароль пользователя root.\n"
                "4. Убедитесь, что служба MySQL запущена\n"
                "   (Windows → «Службы» → MySQL80 → «Выполняется»).\n"
                "5. Введите логин (обычно «root») и ваш пароль в это окно.")

    return MySQLConnectionDialog()


def setup_database(parent=None):
    """
    Оркестратор первичной настройки БД.
    Возвращает True, если можно продолжать запуск.
    """
    from PyQt5.QtWidgets import QDialog, QMessageBox

    cfg = load_db_config()

    # ---------- 1. Проверка подключения ----------
    while True:
        ok, err = check_mysql_connection(cfg)
        if ok:
            break

        dlg = _make_mysql_dialog(cfg, err, parent)
        if dlg.exec_() != QDialog.Accepted:
            return False
        cfg = dlg.get_config()
        save_db_config(cfg)

        # Обновляем db внутри models
        try:
            from models import init_from_config
            init_from_config()
        except Exception as e:
            print(f"init_from_config: {e}")

    # ---------- 2. Создание базы ----------
    ok, err = ensure_database(cfg)
    if not ok:
        QMessageBox.critical(parent, "Ошибка БД",
                             f"Не удалось создать базу данных.\n\n{err}")
        return False

    # ---------- 3. Создание таблиц ----------
    ok, err = ensure_tables()
    if not ok:
        QMessageBox.critical(parent, "Ошибка таблиц",
                             f"Не удалось создать таблицы.\n\n{err}")
        return False

    return True