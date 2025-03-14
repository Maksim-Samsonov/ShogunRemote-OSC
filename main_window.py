import os
import sys
import logging
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFileDialog, QWidget, 
                             QMessageBox, QCheckBox, QGroupBox)
from PyQt5.QtCore import pyqtSignal, Qt

from config import Config
from shogun_worker import ShogunWorker
from osc_server import OSCServer

class MainWindow(QMainWindow):
    def __init__(self, config: Config, shogun_worker: ShogunWorker, osc_server: OSCServer):
        super().__init__()
        self.config = config
        self.shogun_worker = shogun_worker
        self.osc_server = osc_server

        self.initUI()
        self.connectSignals()

    def initUI(self):
        self.setWindowTitle('Shogun Remote OSC')
        self.setGeometry(100, 100, 600, 500)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Shogun Connection Group
        shogun_group = QGroupBox('Shogun Live')
        shogun_layout = QVBoxLayout()
        
        # IP и Порт для Shogun
        connection_layout = QHBoxLayout()
        self.shogun_ip_input = QLineEdit(self.config.shogun_host)
        self.shogun_ip_input.setPlaceholderText('Shogun IP Address')
        self.shogun_port_input = QLineEdit(str(self.config.shogun_port))
        self.shogun_port_input.setPlaceholderText('Shogun Port')
        
        connection_layout.addWidget(QLabel('IP:'))
        connection_layout.addWidget(self.shogun_ip_input)
        connection_layout.addWidget(QLabel('Порт:'))
        connection_layout.addWidget(self.shogun_port_input)
        shogun_layout.addLayout(connection_layout)

        # Capture Folder Section
        capture_layout = QHBoxLayout()
        self.capture_folder_label = QLabel('Папка захвата:')
        self.capture_folder_display = QLineEdit()
        self.capture_folder_display.setReadOnly(True)
        self.capture_folder_display.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                border: 1px solid #a0a0a0;
                padding: 5px;
            }
        """)
        
        self.browse_capture_folder_btn = QPushButton('Обзор')
        self.browse_capture_folder_btn.clicked.connect(self.browse_capture_folder)
        
        capture_layout.addWidget(self.capture_folder_label)
        capture_layout.addWidget(self.capture_folder_display)
        capture_layout.addWidget(self.browse_capture_folder_btn)
        shogun_layout.addLayout(capture_layout)

        # Set Capture Folder Button
        self.set_capture_folder_btn = QPushButton('Установить папку захвата')
        self.set_capture_folder_btn.clicked.connect(self.set_capture_folder)
        shogun_layout.addWidget(self.set_capture_folder_btn)

        shogun_group.setLayout(shogun_layout)
        main_layout.addWidget(shogun_group)

        # OSC Server Group
        osc_group = QGroupBox('OSC Сервер')
        osc_layout = QVBoxLayout()
        
        # OSC IP и Порт
        osc_connection_layout = QHBoxLayout()
        self.osc_ip_input = QLineEdit(self.config.osc_host)
        self.osc_ip_input.setPlaceholderText('OSC IP')
        self.osc_port_input = QLineEdit(str(self.config.osc_port))
        self.osc_port_input.setPlaceholderText('OSC Порт')
        
        osc_connection_layout.addWidget(QLabel('IP:'))
        osc_connection_layout.addWidget(self.osc_ip_input)
        osc_connection_layout.addWidget(QLabel('Порт:'))
        osc_connection_layout.addWidget(self.osc_port_input)
        osc_layout.addLayout(osc_connection_layout)

        osc_group.setLayout(osc_layout)
        main_layout.addWidget(osc_group)

        # Статус соединения
        self.status_label = QLabel('Готов')
        main_layout.addWidget(self.status_label)

        # Кнопки управления
        button_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton('Подключить')
        self.connect_btn.clicked.connect(self.toggle_connection)
        button_layout.addWidget(self.connect_btn)
        
        self.close_btn = QPushButton('Закрыть')
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(button_layout)

    def connectSignals(self):
        # Сигналы от Shogun Worker
        self.shogun_worker.connection_status_changed.connect(self.update_connection_status)
        self.shogun_worker.capture_folder_updated.connect(self.update_capture_folder_display)
        
        # Сигналы от OSC Server
        self.osc_server.server_status_changed.connect(self.update_osc_server_status)
        self.osc_server.capture_folder_received.connect(self.update_capture_folder_display)

    def browse_capture_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку захвата')
        if folder_path:
            self.capture_folder_display.setText(folder_path)

    def set_capture_folder(self):
        folder_path = self.capture_folder_display.text()
        if folder_path:
            try:
                # Установка папки захвата через Shogun Worker
                self.shogun_worker.set_capture_folder(folder_path)
                
                # Отправка пути папки захвата через OSC
                self.osc_server.send_capture_folder(folder_path)
                
                QMessageBox.information(self, 'Успех', f'Папка захвата установлена: {folder_path}')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не удалось установить папку захвата: {str(e)}')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, выберите папку захвата')

    def update_capture_folder_display(self, folder_path):
        # Обновление отображения пути к папке захвата
        self.capture_folder_display.setText(folder_path)

    def update_connection_status(self, is_connected):
        if is_connected:
            self.connect_btn.setText('Отключить')
            self.status_label.setText('Подключено к Shogun')
            
            # Получение текущей папки захвата при подключении
            current_folder = self.shogun_worker.get_capture_folder()
            if current_folder:
                self.update_capture_folder_display(current_folder)
        else:
            self.connect_btn.setText('Подключить')
            self.status_label.setText('Отключено')

    def update_osc_server_status(self, is_running):
        # Обновление статуса OSC-сервера (можно добавить визуальную индикацию)
        pass

    def toggle_connection(self):
        # Обновление конфигурации перед подключением
        self.config.shogun_host = self.shogun_ip_input.text()
        self.config.shogun_port = int(self.shogun_port_input.text())
        self.config.osc_host = self.osc_ip_input.text()
        self.config.osc_port = int(self.osc_port_input.text())

        # Переключение состояния подключения
        if not self.shogun_worker.is_connected:
            try:
                self.shogun_worker.connect()
                self.osc_server.start_server()
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка подключения', str(e))
        else:
            self.shogun_worker.disconnect()
            self.osc_server.stop_server()

    def closeEvent(self, event):
        # Корректное закрытие соединений при выходе
        if self.shogun_worker.is_connected:
            self.shogun_worker.disconnect()
        if self.osc_server._is_running:
            self.osc_server.stop_server()
        event.accept()

def main():
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    config = Config()
    shogun_worker = ShogunWorker(config)
    osc_server = OSCServer(config, shogun_worker)
    
    main_window = MainWindow(config, shogun_worker, osc_server)
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('shogun_remote_osc.log')
        ]
    )
    main()
