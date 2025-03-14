"""
Панель статуса состояния Shogun Live и настроек OSC.
"""

import asyncio
import logging
import threading

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QGroupBox, QGridLayout,
                            QLineEdit, QSpinBox, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

import config
from styles.app_styles import set_status_style

class ShogunPanel(QGroupBox):
    """Панель информации о состоянии Shogun Live и кнопок управления"""
    def __init__(self, shogun_worker):
        super().__init__("Shogun Live")
        self.logger = logging.getLogger('ShogunOSC')
        self.shogun_worker = shogun_worker
        
        # Absolute path to icons
        icons_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icons"))
        red_icon_path = os.path.join(icons_dir, "icon_red.png")
        green_icon_path = os.path.join(icons_dir, "icon_green.png")
        
        # Load icons with error handling
        self.red_icon = QPixmap()
        self.green_icon = QPixmap()
        
        if os.path.exists(red_icon_path) and os.path.exists(green_icon_path):
            self.red_icon.load(red_icon_path)
            self.green_icon.load(green_icon_path)
        
        # Create fallback icons if loading failed
        if self.red_icon.isNull() or self.green_icon.isNull():
            self.logger.warning("Failed to load icons, creating fallback icons")
            self.red_icon = QPixmap(16, 16)
            self.green_icon = QPixmap(16, 16)
            self.red_icon.fill(Qt.red)
            self.green_icon.fill(Qt.green)
        
        self.icon_size = 16  # Set a reasonable default size for the icon
        self.red_icon = self.red_icon.scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio)
        self.green_icon = self.green_icon.scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio)
        
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        """Инициализация интерфейса панели Shogun"""
        layout = QGridLayout()

        # Информация о состоянии
        layout.addWidget(QLabel("Статус:"), 0, 0)
        self.status_label = QLabel(config.STATUS_DISCONNECTED)
        self.status_icon = QLabel()
        self.status_icon.setPixmap(self.red_icon)  # Default to red (disconnected)
        set_status_style(self.status_label, "disconnected")
        hbox = QHBoxLayout()
        hbox.addWidget(self.status_label)
        hbox.addWidget(self.status_icon)
        layout.addLayout(hbox, 0, 1)

        layout.addWidget(QLabel("Запись:"), 1, 0)
        self.recording_label = QLabel(config.STATUS_RECORDING_INACTIVE)
        self.recording_label.setStyleSheet("color: gray;")
        layout.addWidget(self.recording_label, 1, 1)

        # REMOVED: "Текущий тейк" field and label

        # Добавляем поле для отображения имени захвата
        layout.addWidget(QLabel("Имя захвата:"), 2, 0)
        self.capture_name_label = QLabel("Нет данных")
        layout.addWidget(self.capture_name_label, 2, 1)

        # Добавляем поле для отображения описания захвата
        layout.addWidget(QLabel("Описание:"), 3, 0)
        self.description_label = QLabel("Нет данных")
        layout.addWidget(self.description_label, 3, 1)

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.connect_button = QPushButton("Подключиться")
        self.connect_button.clicked.connect(self.reconnect_shogun)
        button_layout.addWidget(self.connect_button)

        self.start_button = QPushButton("Начать запись")
        self.start_button.clicked.connect(self.start_recording)
        self.start_button.setEnabled(False)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Остановить запись")
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout, 4, 0, 1, 2)
        self.setLayout(layout)

    def resizeEvent(self, event):
        """Resizes the status icon when the panel is resized."""
        # We don't need to reload the icons on resize, just rescale the existing ones
        if not self.red_icon.isNull() and not self.green_icon.isNull():
            new_size = min(24, self.width() // 20)  # Limit maximum size
            scaled_red = self.red_icon.scaled(new_size, new_size, Qt.KeepAspectRatio)
            scaled_green = self.green_icon.scaled(new_size, new_size, Qt.KeepAspectRatio)
            
            # Only update if we successfully scaled
            if not scaled_red.isNull() and not scaled_green.isNull():
                self.red_icon = scaled_red
                self.green_icon = scaled_green
                
                # Update the current icon
                if self.shogun_worker.connected:
                    self.status_icon.setPixmap(self.green_icon)
                else:
                    self.status_icon.setPixmap(self.red_icon)
        
        super().resizeEvent(event)

    def connect_signals(self):
        """Подключение сигналов от Shogun Worker"""
        self.shogun_worker.connection_signal.connect(self.update_connection_status)
        self.shogun_worker.recording_signal.connect(self.update_recording_status)
        # REMOVED: self.shogun_worker.take_name_signal.connect(self.update_take_name)
        self.shogun_worker.capture_name_changed_signal.connect(self.update_capture_name)
        self.shogun_worker.description_changed_signal.connect(self.update_description)
        self.shogun_worker.connection_error_signal.connect(self.update_connection_error)

    def update_connection_status(self, connected):
        """Обновление отображения статуса подключения"""
        if connected:
            self.status_label.setText(config.STATUS_CONNECTED)
            set_status_style(self.status_label, "connected")
            self.status_icon.setPixmap(self.green_icon)
            self.start_button.setEnabled(True)
            self.connect_button.setEnabled(False)
        else:
            self.status_label.setText(config.STATUS_DISCONNECTED)
            set_status_style(self.status_label, "disconnected")
            self.status_icon.setPixmap(self.red_icon)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.connect_button.setEnabled(True)

    def update_connection_error(self, error):
        """Обновление иконки при ошибке подключения"""
        if error:
            self.status_icon.setPixmap(self.red_icon)
        else:
            self.status_icon.setPixmap(self.green_icon)

    def update_recording_status(self, is_recording):
        """Обновление отображения статуса записи"""
        if is_recording:
            self.recording_label.setText(config.STATUS_RECORDING_ACTIVE)
            set_status_style(self.recording_label, "recording")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.recording_label.setText(config.STATUS_RECORDING_INACTIVE)
            set_status_style(self.recording_label, "")
            self.start_button.setEnabled(self.shogun_worker.connected)
            self.stop_button.setEnabled(False)

    # REMOVED: update_take_name method

    def update_capture_name(self, name):
        """Обновление имени захвата"""
        self.capture_name_label.setText(name)

    def update_description(self, description):
        """Обновление описания захвата"""
        self.description_label.setText(description)

    def reconnect_shogun(self):
        """Запуск переподключения к Shogun Live"""
        threading.Thread(target=self._run_reconnect).start()

    def _run_reconnect(self):
        """Выполнение переподключения в отдельном потоке"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.shogun_worker.reconnect_shogun())
            if result:
                self.logger.info("Переподключение выполнено успешно")
            else:
                self.logger.error("Не удалось переподключиться")
        finally:
            loop.close()

    def start_recording(self):
        """Запуск записи"""
        threading.Thread(target=self._run_start_recording).start()

    def _run_start_recording(self):
        """Запуск записи в отдельном потоке"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.shogun_worker.startcapture())
        finally:
            loop.close()

    def stop_recording(self):
        """Остановка записи"""
        threading.Thread(target=self._run_stop_recording).start()

    def _run_stop_recording(self):
        """Остановка записи в отдельном потоке"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.shogun_worker.stopcapture())
        finally:
            loop.close()

class OSCPanel(QGroupBox):
    """Панель настроек OSC-сервера"""
    osc_status_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__("OSC Сервер")
        self.init_ui()
        self.osc_server_running = False
    
    def init_ui(self):
        """Инициализация интерфейса панели OSC"""
        layout = QGridLayout()
        
        # Настройки приема OSC-сообщений
        layout.addWidget(QLabel("<b>Настройки приема:</b>"), 0, 0, 1, 2)
        
        layout.addWidget(QLabel("IP:"), 1, 0)
        self.ip_input = QLineEdit(config.DEFAULT_OSC_IP)
        layout.addWidget(self.ip_input, 1, 1)
        
        layout.addWidget(QLabel("Порт:"), 2, 0)
        self.port_input = QSpinBox()
        self.port_input.setRange(1000, 65535)
        self.port_input.setValue(config.DEFAULT_OSC_PORT)
        layout.addWidget(self.port_input, 2, 1)
        
        # Настройки отправки OSC-сообщений
        layout.addWidget(QLabel("<b>Настройки отправки:</b>"), 3, 0, 1, 2)
        
        layout.addWidget(QLabel("IP:"), 4, 0)
        self.broadcast_ip_input = QLineEdit(config.DEFAULT_OSC_BROADCAST_IP)
        layout.addWidget(self.broadcast_ip_input, 4, 1)
        
        layout.addWidget(QLabel("Порт:"), 5, 0)
        self.broadcast_port_input = QSpinBox()
        self.broadcast_port_input.setRange(1000, 65535)
        self.broadcast_port_input.setValue(config.DEFAULT_OSC_BROADCAST_PORT)
        layout.addWidget(self.broadcast_port_input, 5, 1)
        
        # Статус и управление OSC-сервером
        layout.addWidget(QLabel("<b>Управление сервером:</b>"), 6, 0, 1, 2)
        
        # Статус сервера
        layout.addWidget(QLabel("Статус:"), 7, 0)
        self.osc_status_label = QLabel("Остановлен")
        set_status_style(self.osc_status_label, "disconnected")
        layout.addWidget(self.osc_status_label, 7, 1)
        
        # Кнопки управления OSC-сервером
        osc_control_layout = QHBoxLayout()
        
        self.osc_start_button = QPushButton("Запустить")
        self.osc_start_button.clicked.connect(self.on_start_clicked)
        osc_control_layout.addWidget(self.osc_start_button)
        
        self.osc_stop_button = QPushButton("Остановить")
        self.osc_stop_button.clicked.connect(self.on_stop_clicked)
        self.osc_stop_button.setEnabled(False)
        osc_control_layout.addWidget(self.osc_stop_button)
        
        self.osc_restart_button = QPushButton("Перезапустить")
        self.osc_restart_button.clicked.connect(self.on_restart_clicked)
        self.osc_restart_button.setEnabled(False)
        osc_control_layout.addWidget(self.osc_restart_button)
        
        layout.addLayout(osc_control_layout, 8, 0, 1, 2)
        
        # Автозапуск при старте
        self.osc_enabled = QCheckBox("Автозапуск при старте приложения")
        self.osc_enabled.setChecked(config.app_settings.get("osc_enabled", True))
        layout.addWidget(self.osc_enabled, 9, 0, 1, 2)
        
        # Информация о командах OSC
        layout.addWidget(QLabel("<b>Доступные команды:</b>"), 10, 0, 1, 2)
        layout.addWidget(QLabel(f"Старт записи: {config.OSC_START_RECORDING}"), 11, 0, 1, 2)
        layout.addWidget(QLabel(f"Стоп записи: {config.OSC_STOP_RECORDING}"), 12, 0, 1, 2)
        layout.addWidget(QLabel(f"Установка имени: /SetCaptureName [имя]"), 13, 0, 1, 2)
        layout.addWidget(QLabel(f"Установка описания: /SetCaptureDescription [описание]"), 14, 0, 1, 2)
        layout.addWidget(QLabel(f"Уведомление об имени: {config.OSC_CAPTURE_NAME_CHANGED}"), 15, 0, 1, 2)
        layout.addWidget(QLabel(f"Уведомление об описании: {config.OSC_DESCRIPTION_CHANGED}"), 16, 0, 1, 2)
        
        self.setLayout(layout)
        
    def get_broadcast_settings(self):
        """Получение настроек для отправки OSC-сообщений"""
        return {
            "ip": self.broadcast_ip_input.text(),
            "port": self.broadcast_port_input.value()
        }

    def on_start_clicked(self):
        """Обработчик нажатия кнопки запуска OSC-сервера"""
        self.osc_status_changed.emit(True)
        self.osc_start_button.setEnabled(False)
        self.osc_stop_button.setEnabled(True)
        self.osc_restart_button.setEnabled(True)
        self.ip_input.setEnabled(False)
        self.port_input.setEnabled(False)
        self.osc_status_label.setText("Запущен")
        set_status_style(self.osc_status_label, "connected")
        self.osc_server_running = True

    def on_stop_clicked(self):
        """Обработчик нажатия кнопки остановки OSC-сервера"""
        self.osc_status_changed.emit(False)
        self.osc_start_button.setEnabled(True)
        self.osc_stop_button.setEnabled(False)
        self.osc_restart_button.setEnabled(False)
        self.ip_input.setEnabled(True)
        self.port_input.setEnabled(True)
        self.osc_status_label.setText("Остановлен")
        set_status_style(self.osc_status_label, "disconnected")
        self.osc_server_running = False

    def on_restart_clicked(self):
        """Обработчик нажатия кнопки перезапуска OSC-сервера"""
        self.osc_status_changed.emit(False)
        self.osc_status_changed.emit(True)
        self.on_stop_clicked()
        self.on_start_clicked()

class StatusPanel(QWidget):
    """Составная панель статуса и настроек"""
    def __init__(self, shogun_worker):
        super().__init__()
        self.shogun_worker = shogun_worker
        self.init_ui(shogun_worker)
    
    def init_ui(self, shogun_worker):
        """Инициализация составной панели"""
        layout = QHBoxLayout()
        
        # Создаем панели
        self.shogun_panel = ShogunPanel(shogun_worker)
        self.osc_panel = OSCPanel()
        
        # Добавляем панели с разным весом
        layout.addWidget(self.shogun_panel, 3)  # Больший вес для панели Shogun
        layout.addWidget(self.osc_panel, 2)
        
        self.setLayout(layout)
        self.shogun_worker.connection_error_signal.connect(self.shogun_panel.update_connection_error)