# # import_initial_data.py
# import csv
# import os
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
#                             QPushButton, QFileDialog, QCheckBox, QGroupBox,
#                             QProgressBar, QMessageBox, QTableWidget, QTableWidgetItem,
#                             QHeaderView, QWidget)
# from PyQt5.QtCore import Qt, QThread, pyqtSignal
# from models import Region, Patronymic, Players_full, Coach, db

# class ImportThread(QThread):
#     progress = pyqtSignal(int, str)
#     finished = pyqtSignal(bool, str)
    
#     def __init__(self, import_data, file_paths):
#         super().__init__()
#         self.import_data = import_data
#         self.file_paths = file_paths
        
#     def run(self):
#         try:
#             total_steps = sum(1 for k, v in self.import_data.items() if v)
#             current_step = 0
            
#             # Импорт регионов
#             if self.import_data.get('regions'):
#                 self.progress.emit(0, "Импорт регионов...")
#                 self.import_regions()
#                 current_step += 1
#                 self.progress.emit(int(current_step / total_steps * 100), "Регионы импортированы")
            
#             # Импорт отчеств
#             if self.import_data.get('patronymics'):
#                 self.progress.emit(0, "Импорт отчеств...")
#                 self.import_patronymics()
#                 current_step += 1
#                 self.progress.emit(int(current_step / total_steps * 100), "Отчества импортированы")
            
#             # Импорт тренеров
#             if self.import_data.get('coaches'):
#                 self.progress.emit(0, "Импорт тренеров...")
#                 self.import_coaches()
#                 current_step += 1
#                 self.progress.emit(int(current_step / total_steps * 100), "Тренеры импортированы")
            
#             # Импорт полных данных игроков
#             if self.import_data.get('players_full'):
#                 self.progress.emit(0, "Импорт полных данных игроков...")
#                 self.import_players_full()
#                 current_step += 1
#                 self.progress.emit(int(current_step / total_steps * 100), "Данные игроков импортированы")
            
#             self.finished.emit(True, "Импорт завершен успешно!")
            
#         except Exception as e:
#             self.finished.emit(False, f"Ошибка импорта: {str(e)}")
    
#     def import_regions(self):
#         """Импорт регионов из CSV"""
#         file_path = self.file_paths.get('regions')
#         if not file_path or not os.path.exists(file_path):
#             return
        
#         with open(file_path, 'r', encoding='utf-8-sig') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 region_name = row.get('region') or row.get('Регион') or row.get('название')
#                 if region_name:
#                     Region.get_or_create(region=region_name.strip())
    
#     def import_patronymics(self):
#         """Импорт отчеств из CSV"""
#         file_path = self.file_paths.get('patronymics')
#         if not file_path or not os.path.exists(file_path):
#             return
        
#         with open(file_path, 'r', encoding='utf-8-sig') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 patronymic = row.get('patronymic') or row.get('Отчество') or row.get('название')
#                 sex = row.get('sex') or row.get('Пол') or row.get('пол')
#                 if patronymic:
#                     Patronymic.get_or_create(
#                         patronymic=patronymic.strip(),
#                         defaults={'sex': sex[0].lower() if sex else 'm'}
#                     )
    
#     def import_coaches(self):
#         """Импорт тренеров из CSV"""
#         file_path = self.file_paths.get('coaches')
#         if not file_path or not os.path.exists(file_path):
#             return
        
#         with open(file_path, 'r', encoding='utf-8-sig') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 coach_name = row.get('coach') or row.get('Тренер') or row.get('ФИО')
#                 if coach_name:
#                     Coach.get_or_create(coach=coach_name.strip())
    
#     def import_players_full(self):
#         """Импорт полных данных игроков из CSV"""
#         file_path = self.file_paths.get('players_full')
#         if not file_path or not os.path.exists(file_path):
#             return
        
#         from datetime import datetime
#         with open(file_path, 'r', encoding='utf-8-sig') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 player_name = row.get('player') or row.get('ФИО') or row.get('Игрок')
#                 if not player_name:
#                     continue
                
#                 # Обработка даты рождения
#                 bday_str = row.get('bday') or row.get('Дата рождения')
#                 bday = None
#                 if bday_str:
#                     try:
#                         for fmt in ["%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d", "%d/%m/%Y"]:
#                             try:
#                                 bday = datetime.strptime(bday_str.strip(), fmt).date()
#                                 break
#                             except:
#                                 continue
#                     except:
#                         pass
                
#                 # Получаем регион
#                 region_name = row.get('region') or row.get('Регион')
#                 region = None
#                 if region_name:
#                     region_obj = Region.get_or_none(Region.region == region_name.strip())
#                     if region_obj:
#                         region = region_obj.region
                
#                 # Получаем отчество
#                 patronymic_name = row.get('patronymic') or row.get('Отчество')
#                 patronymic_id = None
#                 if patronymic_name:
#                     patronymic_obj = Patronymic.get_or_none(Patronymic.patronymic == patronymic_name.strip())
#                     if patronymic_obj:
#                         patronymic_id = patronymic_obj.id
                
#                 # Получаем тренера
#                 coach_name = row.get('coach_id') or row.get('Тренер')
#                 coach_id = None
#                 if coach_name:
#                     coach_obj = Coach.get_or_none(Coach.coach == coach_name.strip())
#                     if coach_obj:
#                         coach_id = coach_obj.id
                
#                 # Пол
#                 sex = row.get('sex') or row.get('Пол')
#                 if sex:
#                     sex = 'man' if sex.lower().startswith('м') else 'woman'
                
#                 # Создаем или обновляем запись
#                 Players_full.get_or_create(
#                     player=player_name.strip(),
#                     defaults={
#                         'bday': bday,
#                         'city': row.get('city') or row.get('Город'),
#                         'region': region,
#                         'razryad': row.get('razryad') or row.get('Разряд'),
#                         'coach_id': coach_id,
#                         'patronymic_id': patronymic_id,
#                         'sex': sex
#                     }
#                 )


# class InitialDataImportDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Импорт начальных данных")
#         self.setModal(True)
#         self.setMinimumWidth(600)
#         self.setMinimumHeight(500)
        
#         self.file_paths = {}
#         self.import_data = {
#             'regions': False,
#             'patronymics': False,
#             'coaches': False,
#             'players_full': False
#         }
        
#         self.init_ui()
    
#     def init_ui(self):
#         layout = QVBoxLayout(self)
        
#         # Заголовок
#         title_label = QLabel("Импорт начальных данных")
#         title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
#         layout.addWidget(title_label)
        
#         info_label = QLabel("База данных успешно создана.\n"
#                            "Выберите CSV файлы для импорта справочных данных:")
#         info_label.setWordWrap(True)
#         layout.addWidget(info_label)
        
#         # Группа для выбора файлов
#         files_group = QGroupBox("Выбор файлов для импорта")
#         files_layout = QVBoxLayout(files_group)
        
#         # Регионы
#         regions_widget = self.create_file_selector("Регионы", "regions")
#         files_layout.addWidget(regions_widget)
        
#         # Отчества
#         patronymics_widget = self.create_file_selector("Отчества", "patronymics")
#         files_layout.addWidget(patronymics_widget)
        
#         # Тренеры
#         coaches_widget = self.create_file_selector("Тренеры", "coaches")
#         files_layout.addWidget(coaches_widget)
        
#         # Полные данные игроков
#         players_widget = self.create_file_selector("Полные данные игроков", "players_full")
#         files_layout.addWidget(players_widget)
        
#         layout.addWidget(files_group)
        
#         # Кнопки
#         btn_layout = QHBoxLayout()
        
#         self.import_btn = QPushButton("🚀 Начать импорт")
#         self.import_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
#         self.import_btn.clicked.connect(self.start_import)
        
#         skip_btn = QPushButton("⏭️ Пропустить")
#         skip_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 8px;")
#         skip_btn.clicked.connect(self.reject)
        
#         btn_layout.addWidget(self.import_btn)
#         btn_layout.addWidget(skip_btn)
#         layout.addLayout(btn_layout)
        
#         # Прогресс
#         self.progress_bar = QProgressBar()
#         self.progress_bar.setVisible(False)
#         layout.addWidget(self.progress_bar)
        
#         self.status_label = QLabel("")
#         self.status_label.setStyleSheet("color: green;")
#         layout.addWidget(self.status_label)
    
#     def create_file_selector(self, title, key):
#         widget = QWidget()
#         layout = QHBoxLayout(widget)
#         layout.setContentsMargins(0, 0, 0, 0)
        
#         checkbox = QCheckBox(title)
#         checkbox.stateChanged.connect(lambda state, k=key: self.on_checkbox_changed(k, state))
#         layout.addWidget(checkbox)
        
#         file_label = QLabel("Файл не выбран")
#         file_label.setStyleSheet("color: gray;")
#         layout.addWidget(file_label, 1)
        
#         select_btn = QPushButton("Выбрать")
#         select_btn.clicked.connect(lambda: self.select_file(key, file_label))
#         layout.addWidget(select_btn)
        
#         self.file_paths[key] = None
#         widget.checkbox = checkbox
#         widget.file_label = file_label
        
#         return widget
    
#     def on_checkbox_changed(self, key, state):
#         self.import_data[key] = (state == Qt.Checked)
    
#     def select_file(self, key, label):
#         file_path, _ = QFileDialog.getOpenFileName(
#             self,
#             f"Выберите CSV файл",
#             "",
#             "CSV files (*.csv);;All files (*.*)"
#         )
#         if file_path:
#             self.file_paths[key] = file_path
#             label.setText(os.path.basename(file_path))
#             label.setStyleSheet("color: green;")
    
#     def start_import(self):
#         # Проверяем, выбраны ли файлы для импорта
#         has_selected = False
#         for key, selected in self.import_data.items():
#             if selected and not self.file_paths.get(key):
#                 QMessageBox.warning(self, "Ошибка", 
#                                    f"Для импорта '{key}' необходимо выбрать файл")
#                 return
#             if selected and self.file_paths.get(key):
#                 has_selected = True
        
#         if not has_selected:
#             QMessageBox.warning(self, "Ошибка", "Не выбрано ни одного файла для импорта")
#             return
        
#         # Запускаем импорт
#         self.import_btn.setEnabled(False)
#         self.progress_bar.setVisible(True)
#         self.progress_bar.setValue(0)
        
#         self.import_thread = ImportThread(self.import_data, self.file_paths)
#         self.import_thread.progress.connect(self.update_progress)
#         self.import_thread.finished.connect(self.import_finished)
#         self.import_thread.start()
    
#     def update_progress(self, value, message):
#         self.progress_bar.setValue(value)
#         self.status_label.setText(message)
    
#     def import_finished(self, success, message):
#         self.progress_bar.setValue(100)
#         if success:
#             QMessageBox.information(self, "Успех", message)
#             self.accept()
#         else:
#             QMessageBox.critical(self, "Ошибка", message)
#             self.import_btn.setEnabled(True)

# import_initial_data.py
import os
from datetime import datetime
import pandas as pd

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QFileDialog, QMessageBox, QProgressBar,
    QFrame, QApplication,
)
from PyQt5.QtCore import Qt

from models import (
    db, Region, City, Coach, Patronymic, Players_full,
)


class ReferenceDataImportDialog(QDialog):
    """
    Диалог импорта справочников: Регионы, Города, Тренеры,
    Отчества, Players_full.
    Используется при первичной настройке и через меню.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Импорт справочников")
        self.setModal(True)
        self.setMinimumWidth(760)

        self.selected_files = {
            "regions": None, "cities": None, "coaches": None,
            "patronymics": None, "players_full": None,
        }

        self._build_ui()
        self._refresh_counts()

    # --------------------------------------------------------------
    def _build_ui(self):
        layout = QVBoxLayout(self)

        info = QLabel(
            "Загрузите справочники (можно частично).\n"
            "Уже заполненные таблицы будут пропущены, если не указан файл."
        )
        info.setWordWrap(True)
        info.setStyleSheet("background:#f5f5f5; padding:8px; border-radius:4px;")
        layout.addWidget(info)

        layout.addWidget(self._make_row(
            "Регионы (Субъекты РФ)", "regions",
            "Excel: колонка «Субъект РФ» или «Регион»"))
        layout.addWidget(self._make_row(
            "Города", "cities",
            "Excel: колонки «Город», «Регион»"))
        layout.addWidget(self._make_row(
            "Тренеры", "coaches",
            "Excel: колонка «Тренер»"))
        layout.addWidget(self._make_row(
            "Отчества", "patronymics",
            "Excel: колонки «Отчество», «Пол» (м/ж)"))
        layout.addWidget(self._make_row(
            "Игроки (Players_full)", "players_full",
            "Excel: ФИО, дата рождения, город, регион, разряд, тренер, отчество, пол"))

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color:#333; padding:6px;")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        btn_row = QHBoxLayout()
        import_btn = QPushButton("🚀 Импортировать выбранное")
        import_btn.setStyleSheet(
            "background:#4CAF50; color:white; padding:8px 16px; "
            "font-weight:bold;")
        import_btn.clicked.connect(self._do_import)
        skip_btn = QPushButton("Пропустить")
        skip_btn.clicked.connect(self.reject)
        btn_row.addWidget(import_btn)
        btn_row.addStretch()
        btn_row.addWidget(skip_btn)
        layout.addLayout(btn_row)

    def _make_row(self, title, key, hint):
        frame = QFrame()
        frame.setStyleSheet(
            "QFrame{background:#fafafa; border:1px solid #ddd; "
            "border-radius:4px; padding:4px;}")
        row = QHBoxLayout(frame)
        row.setContentsMargins(8, 4, 8, 4)

        cb = QCheckBox(title)
        cb.setMinimumWidth(180)
        cb.setChecked(True)
        setattr(self, f"cb_{key}", cb)
        row.addWidget(cb)

        lbl = QLabel("…")
        lbl.setStyleSheet("color:#666; font-size:11px;")
        setattr(self, f"lbl_{key}", lbl)
        row.addWidget(lbl, 1)

        btn = QPushButton("📂 Файл…")
        btn.setStyleSheet("padding:4px 10px;")
        setattr(self, f"btn_{key}", btn)

        def _pick(checked=False, k=key, t=title, l=lbl):
            path, _ = QFileDialog.getOpenFileName(
                self, f"Excel для «{t}»", "",
                "Excel (*.xlsx *.xls)")
            if not path:
                return
            self.selected_files[k] = path
            l.setText(os.path.basename(path))
            l.setStyleSheet("color:#2e7d32; font-weight:bold; font-size:11px;")

        btn.clicked.connect(_pick)
        row.addWidget(btn)

        return frame

    def _refresh_counts(self):
        try:
            db.connect(reuse_if_open=True)
            counts = {
                "regions": Region.select().count(),
                "cities": City.select().count(),
                "coaches": Coach.select().count(),
                "patronymics": Patronymic.select().count(),
                "players_full": Players_full.select().count(),
            }
            for key, cnt in counts.items():
                lbl = getattr(self, f"lbl_{key}", None)
                if lbl is None:
                    continue
                if cnt == 0:
                    lbl.setText("пусто — нужно загрузить")
                    lbl.setStyleSheet("color:#c62828; font-size:11px;")
                else:
                    lbl.setText(f"в базе: {cnt}")
                    lbl.setStyleSheet("color:#666; font-size:11px;")
        except Exception as e:
            self.status_label.setText(f"Ошибка проверки БД: {e}")

    # --------------------------------------------------------------
    def _do_import(self):
        tasks = []
        for key in ("regions", "cities", "coaches",
                    "patronymics", "players_full"):
            cb = getattr(self, f"cb_{key}")
            if not cb.isChecked():
                continue
            path = self.selected_files[key]
            if not path:
                # если таблица уже заполнена — пропустить молча
                try:
                    db.connect(reuse_if_open=True)
                    if self._count_for(key) > 0:
                        continue
                except Exception:
                    pass
                QMessageBox.warning(
                    self, "Нет файла",
                    f"«{cb.text()}» отмечено, но файл не выбран.")
                return
            tasks.append((key, path))

        if not tasks:
            QMessageBox.information(self, "Импорт", "Нечего импортировать.")
            return

        self.progress.setVisible(True)
        self.progress.setRange(0, len(tasks))
        self.progress.setValue(0)

        summary = []
        try:
            with db.atomic():
                for i, (key, path) in enumerate(tasks, 1):
                    self.status_label.setText(
                        f"Импорт: {key} ({i}/{len(tasks)})...")
                    QApplication.processEvents()

                    n = self._import_one(key, path)
                    summary.append(f"{key}: +{n}")
                    self.progress.setValue(i)
                    QApplication.processEvents()

            self.status_label.setText(
                "✅ Готово: " + ", ".join(summary))
            QMessageBox.information(
                self, "Успех",
                "Импорт завершён.\n\n" + "\n".join(summary))
            self._refresh_counts()
            self.accept()

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self, "Ошибка",
                f"Импорт не выполнен (транзакция откатана).\n\n{e}")

    def _count_for(self, key):
        return {
            "regions": lambda: Region.select().count(),
            "cities": lambda: City.select().count(),
            "coaches": lambda: Coach.select().count(),
            "patronymics": lambda: Patronymic.select().count(),
            "players_full": lambda: Players_full.select().count(),
        }[key]()

    def _import_one(self, key, path):
        return {
            "regions": self._import_regions,
            "cities": self._import_cities,
            "coaches": self._import_coaches,
            "patronymics": self._import_patronymics,
            "players_full": self._import_players_full,
        }[key](path)

    # --------------------------------------------------------------
    # Импортёры
    # --------------------------------------------------------------
    def _import_regions(self, path):
        df = pd.read_excel(path)
        col = None
        for c in df.columns:
            cl = str(c).lower()
            if "субъект" in cl or "регион" in cl:
                col = c
                break
        if col is None:
            col = df.columns[0]

        existing = {r.region for r in Region.select(Region.region)}
        n = 0
        for v in df[col].dropna().astype(str):
            v = v.strip()
            if not v or v in existing:
                continue
            Region.create(region=v)
            existing.add(v)
            n += 1
        return n

    def _import_cities(self, path):
        df = pd.read_excel(path)
        city_col, region_col = None, None
        for c in df.columns:
            cl = str(c).lower()
            if city_col is None and "город" in cl:
                city_col = c
            if region_col is None and ("регион" in cl or "субъект" in cl):
                region_col = c
        if city_col is None:
            city_col = df.columns[0]
        if region_col is None and len(df.columns) > 1:
            region_col = df.columns[1]

        n = 0
        for _, row in df.iterrows():
            city_name = str(row.get(city_col, "")).strip()
            if not city_name or city_name == "nan":
                continue
            region_name = (str(row.get(region_col, "")).strip()
                           if region_col else "")
            if not region_name or region_name == "nan":
                continue
            region, _ = Region.get_or_create(region=region_name)
            _, created = City.get_or_create(
                city=city_name, region_id=region.id)
            if created:
                n += 1
        return n

    def _import_coaches(self, path):
        df = pd.read_excel(path)
        col = None
        for c in df.columns:
            cl = str(c).lower()
            if "тренер" in cl or "coach" in cl:
                col = c
                break
        if col is None:
            col = df.columns[0]

        existing = {c.coach for c in Coach.select(Coach.coach)}
        n = 0
        for v in df[col].dropna().astype(str):
            v = v.strip()
            if not v or v in existing:
                continue
            Coach.create(coach=v)
            existing.add(v)
            n += 1
        return n

    def _import_patronymics(self, path):
        df = pd.read_excel(path)
        pat_col, sex_col = None, None
        for c in df.columns:
            cl = str(c).lower()
            if pat_col is None and "отчеств" in cl:
                pat_col = c
            if sex_col is None and ("пол" in cl or "sex" in cl):
                sex_col = c
        if pat_col is None:
            pat_col = df.columns[0]
        if sex_col is None and len(df.columns) > 1:
            sex_col = df.columns[1]

        n = 0
        for _, row in df.iterrows():
            pat = str(row.get(pat_col, "")).strip()
            if not pat or pat == "nan":
                continue
            raw = (str(row.get(sex_col, "m")).strip().lower()
                   if sex_col else "m")
            if raw in ("м", "муж", "m", "male"):
                sex = "m"
            elif raw in ("ж", "жен", "w", "f", "female"):
                sex = "w"
            else:
                sex = "m"
            _, created = Patronymic.get_or_create(
                patronymic=pat, defaults={"sex": sex})
            if created:
                n += 1
        return n

    def _import_players_full(self, path):
        df = pd.read_excel(path)
        cmap = {}
        for c in df.columns:
            cl = str(c).lower()
            if "фио" in cl or "player" in cl or "спортсмен" in cl:
                cmap.setdefault("player", c)
            elif "дата" in cl and ("рожд" in cl or "birth" in cl):
                cmap.setdefault("bday", c)
            elif "город" in cl or "city" in cl:
                cmap.setdefault("city", c)
            elif "регион" in cl or "субъект" in cl:
                cmap.setdefault("region", c)
            elif "разряд" in cl:
                cmap.setdefault("razryad", c)
            elif "тренер" in cl or "coach" in cl:
                cmap.setdefault("coach", c)
            elif "отчество" in cl or "patronymic" in cl:
                cmap.setdefault("patronymic", c)
            elif "пол" in cl or "sex" in cl:
                cmap.setdefault("sex", c)

        for req in ("player", "bday", "city", "region"):
            if req not in cmap:
                raise ValueError(
                    f"В Players_full не найдена колонка «{req}»")

        n = 0
        for _, row in df.iterrows():
            fio = str(row.get(cmap["player"], "")).strip()
            if not fio or fio == "nan":
                continue

            bday_raw = row.get(cmap["bday"])
            if pd.isna(bday_raw):
                continue
            try:
                if isinstance(bday_raw, (pd.Timestamp, datetime)):
                    bday = bday_raw.date()
                else:
                    bday = pd.to_datetime(bday_raw).date()
            except Exception:
                continue

            city = str(row.get(cmap["city"], "")).strip()
            region = str(row.get(cmap["region"], "")).strip()
            if not city or city == "nan" or not region or region == "nan":
                continue

            razryad = (str(row.get(cmap["razryad"], "")).strip()
                       if "razryad" in cmap else "")
            if razryad == "nan":
                razryad = ""

            coach_name = (str(row.get(cmap["coach"], "")).strip()
                          if "coach" in cmap else "")
            if coach_name == "nan":
                coach_name = ""

            patr_name = (str(row.get(cmap["patronymic"], "")).strip()
                         if "patronymic" in cmap else "")
            if patr_name == "nan":
                patr_name = ""

            sex_raw = (str(row.get(cmap["sex"], "m")).strip().lower()
                       if "sex" in cmap else "m")
            if sex_raw in ("м", "муж", "m", "male"):
                sex = "man"
            elif sex_raw in ("ж", "жен", "w", "f", "female"):
                sex = "woman"
            else:
                sex = "man"

            coach_id = None
            if coach_name:
                coach_obj, _ = Coach.get_or_create(coach=coach_name)
                coach_id = coach_obj.id

            patr_id = None
            if patr_name:
                p, _ = Patronymic.get_or_create(
                    patronymic=patr_name,
                    defaults={"sex": "m" if sex == "man" else "w"})
                patr_id = p.id

            if Players_full.get_or_none(
                (Players_full.player == fio) &
                (Players_full.bday == bday)
            ):
                continue

            Players_full.create(
                player=fio, bday=bday, city=city, region=region,
                razryad=razryad, coach_id=coach_id,
                patronymic_id=patr_id, sex=sex,
            )
            n += 1
        return n
    # ─── Обратная совместимость: старое имя класса ───
InitialDataImportDialog = ReferenceDataImportDialog