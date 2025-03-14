import os
import sys
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

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Shogun Connection Group
        shogun_group = QGroupBox('Shogun Connection')
        shogun_layout = QVBoxLayout()
        
        # IP and Port inputs
        connection_layout = QHBoxLayout()
        self.ip_input = QLineEdit(self.config.shogun_host)
        self.ip_input.setPlaceholderText('Shogun IP Address')
        self.port_input = QLineEdit(str(self.config.shogun_port))
        self.port_input.setPlaceholderText('Shogun Port')
        
        connection_layout.addWidget(QLabel('IP:'))
        connection_layout.addWidget(self.ip_input)
        connection_layout.addWidget(QLabel('Port:'))
        connection_layout.addWidget(self.port_input)
        shogun_layout.addLayout(connection_layout)

        # Capture Folder Section
        capture_layout = QHBoxLayout()
        self.capture_folder_input = QLineEdit()
        self.capture_folder_input.setPlaceholderText('Capture Folder Path')
        self.browse_capture_folder_btn = QPushButton('Browse')
        self.browse_capture_folder_btn.clicked.connect(self.browse_capture_folder)
        
        capture_layout.addWidget(QLabel('Capture Folder:'))
        capture_layout.addWidget(self.capture_folder_input)
        capture_layout.addWidget(self.browse_capture_folder_btn)
        shogun_layout.addLayout(capture_layout)

        # Set Capture Folder Button
        self.set_capture_folder_btn = QPushButton('Set Capture Folder')
        self.set_capture_folder_btn.clicked.connect(self.set_capture_folder)
        shogun_layout.addWidget(self.set_capture_folder_btn)

        shogun_group.setLayout(shogun_layout)
        main_layout.addWidget(shogun_group)

        # OSC Server Group
        osc_group = QGroupBox('OSC Server')
        osc_layout = QVBoxLayout()
        
        # OSC IP and Port inputs
        osc_connection_layout = QHBoxLayout()
        self.osc_ip_input = QLineEdit(self.config.osc_host)
        self.osc_ip_input.setPlaceholderText('OSC IP Address')
        self.osc_port_input = QLineEdit(str(self.config.osc_port))
        self.osc_port_input.setPlaceholderText('OSC Port')
        
        osc_connection_layout.addWidget(QLabel('IP:'))
        osc_connection_layout.addWidget(self.osc_ip_input)
        osc_connection_layout.addWidget(QLabel('Port:'))
        osc_connection_layout.addWidget(self.osc_port_input)
        osc_layout.addLayout(osc_connection_layout)

        osc_group.setLayout(osc_layout)
        main_layout.addWidget(osc_group)

        # Status Label
        self.status_label = QLabel('Ready')
        main_layout.addWidget(self.status_label)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton('Connect')
        self.connect_btn.clicked.connect(self.toggle_connection)
        button_layout.addWidget(self.connect_btn)
        
        self.close_btn = QPushButton('Close')
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(button_layout)

    def connectSignals(self):
        # Connect signals from Shogun Worker
        self.shogun_worker.connection_status_changed.connect(self.update_connection_status)
        self.shogun_worker.capture_folder_updated.connect(self.update_capture_folder_display)

    def browse_capture_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Capture Folder')
        if folder_path:
            self.capture_folder_input.setText(folder_path)

    def set_capture_folder(self):
        folder_path = self.capture_folder_input.text()
        if folder_path:
            try:
                # Call Shogun worker method to set capture folder
                self.shogun_worker.set_capture_folder(folder_path)
                # Optionally, send OSC message about capture folder
                self.osc_server.send_capture_folder(folder_path)
                QMessageBox.information(self, 'Success', f'Capture folder set to: {folder_path}')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to set capture folder: {str(e)}')
        else:
            QMessageBox.warning(self, 'Error', 'Please select a capture folder')

    def update_capture_folder_display(self, folder_path):
        # Update the capture folder input with the current folder path
        self.capture_folder_input.setText(folder_path)

    def toggle_connection(self):
        # Update configuration with current inputs
        self.config.shogun_host = self.ip_input.text()
        self.config.shogun_port = int(self.port_input.text())
        self.config.osc_host = self.osc_ip_input.text()
        self.config.osc_port = int(self.osc_port_input.text())

        # Toggle connection
        if not self.shogun_worker.is_connected:
            try:
                self.shogun_worker.connect()
                self.connect_btn.setText('Disconnect')
                self.status_label.setText('Connected to Shogun')
            except Exception as e:
                QMessageBox.warning(self, 'Connection Error', str(e))
        else:
            self.shogun_worker.disconnect()
            self.connect_btn.setText('Connect')
            self.status_label.setText('Disconnected')

    def update_connection_status(self, is_connected):
        if is_connected:
            self.connect_btn.setText('Disconnect')
            self.status_label.setText('Connected to Shogun')
        else:
            self.connect_btn.setText('Connect')
            self.status_label.setText('Disconnected')

    def closeEvent(self, event):
        # Ensure clean disconnection when closing the application
        if self.shogun_worker.is_connected:
            self.shogun_worker.disconnect()
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
    main()
