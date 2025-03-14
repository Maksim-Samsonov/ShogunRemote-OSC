import logging
from pythonosc import udp_client, dispatcher, osc_server
from PyQt5.QtCore import QObject, pyqtSignal
import threading
import socketserver
from config import Config

class OSCServer(QObject):
    server_status_changed = pyqtSignal(bool)
    capture_folder_received = pyqtSignal(str)

    def __init__(self, config: Config, shogun_worker):
        super().__init__()
        self.config = config
        self.shogun_worker = shogun_worker
        self.client = None
        self.server = None
        self._server_thread = None
        self._last_sent_capture_folder = None
        self._last_received_capture_folder = None
        self._is_running = False

        # Создание OSC-клиента для отправки сообщений
        try:
            self.client = udp_client.SimpleUDPClient(self.config.osc_host, self.config.osc_port)
        except Exception as e:
            logging.error(f'Ошибка создания OSC-клиента: {e}')

    def start_server(self):
        try:
            # Создание диспетчера для обработки OSC-сообщений
            self.dispatcher = dispatcher.Dispatcher()
            self.dispatcher.map("/ShogunLiveCaptureFolder", self.handle_capture_folder)
            
            # Создание сервера
            self.server = osc_server.ThreadingOSCUDPServer(
                (self.config.osc_host, self.config.osc_port), 
                self.dispatcher
            )

            # Запуск сервера в отдельном потоке
            self._server_thread = threading.Thread(target=self.server.serve_forever)
            self._server_thread.daemon = True
            self._server_thread.start()

            self._is_running = True
            self.server_status_changed.emit(True)
            logging.info('OSC-сервер запущен')

        except Exception as e:
            logging.error(f'Ошибка запуска OSC-сервера: {e}')
            self._is_running = False
            self.server_status_changed.emit(False)

    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server = None
            self._is_running = False
            self.server_status_changed.emit(False)
            logging.info('OSC-сервер остановлен')

    def handle_capture_folder(self, address, *args):
        if args and isinstance(args[0], str):
            folder_path = args[0]
            # Предотвращение дублирования сообщений
            if self._last_received_capture_folder != folder_path:
                self._last_received_capture_folder = folder_path
                self.capture_folder_received.emit(folder_path)
                logging.info(f'Получено OSC-сообщение: {address} -> {folder_path}')

    def send_capture_folder(self, folder_path):
        if self.client:
            try:
                # Проверка на повторение пути перед отправкой
                if self._last_sent_capture_folder != folder_path:
                    self.client.send_message("/ShogunLiveCaptureFolder", folder_path)
                    self._last_sent_capture_folder = folder_path
                    logging.info(f'Отправлено OSC-сообщение: /ShogunLiveCaptureFolder -> {folder_path}')
            except Exception as e:
                logging.error(f'Ошибка отправки OSC-сообщения: {e}')
