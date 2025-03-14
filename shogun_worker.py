import logging
import time
from PyQt5.QtCore import QObject, pyqtSignal
from vicon_dsk import ViconDataStream
from config import Config

class ShogunWorker(QObject):
    connection_status_changed = pyqtSignal(bool)
    recording_status_changed = pyqtSignal(bool)
    capture_folder_updated = pyqtSignal(str)

    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self._client = None
        self.is_connected = False
        self._current_capture_folder = None
        self._is_recording = False

    def connect(self):
        try:
            self._client = ViconDataStream.Client()
            self._client.Connect(self.config.shogun_host, self.config.shogun_port)
            
            if self._client.IsConnected():
                self.is_connected = True
                self.connection_status_changed.emit(True)
                
                # Получаем текущую папку захвата при подключении
                current_folder = self._client.capture_folder()
                if current_folder:
                    self._current_capture_folder = current_folder
                    self.capture_folder_updated.emit(current_folder)
                
                logging.info(f'Успешно подключено к Shogun Live')
            else:
                raise ConnectionError('Не удалось установить соединение')
        
        except Exception as e:
            logging.error(f'Ошибка подключения: {e}')
            self.is_connected = False
            self.connection_status_changed.emit(False)
            raise

    def disconnect(self):
        if self._client and self.is_connected:
            self._client.Disconnect()
            self.is_connected = False
            self.connection_status_changed.emit(False)
            logging.info('Отключено от Shogun Live')

    def start_recording(self, name='', description=''):
        if self.is_connected and not self._is_recording:
            try:
                self._client.StartRecording(name, description)
                self._is_recording = True
                self.recording_status_changed.emit(True)
                logging.info(f'Начата запись: {name}')
            except Exception as e:
                logging.error(f'Ошибка при старте записи: {e}')

    def stop_recording(self):
        if self.is_connected and self._is_recording:
            try:
                self._client.StopRecording()
                self._is_recording = False
                self.recording_status_changed.emit(False)
                logging.info('Остановлена запись')
            except Exception as e:
                logging.error(f'Ошибка при остановке записи: {e}')

    def set_capture_folder(self, folder_path):
        if self.is_connected:
            try:
                # Проверка на совпадение текущего и нового пути
                if self._current_capture_folder != folder_path:
                    self._client.set_capture_folder(folder_path)
                    self._current_capture_folder = folder_path
                    self.capture_folder_updated.emit(folder_path)
                    logging.info(f'Путь к папке захвата изменился: {folder_path}')
            except Exception as e:
                logging.error(f'Ошибка при установке папки захвата: {e}')
        else:
            logging.error('Невозможно установить папку захвата - нет соединения')

    def get_capture_folder(self):
        if self.is_connected:
            try:
                folder = self._client.capture_folder()
                return folder
            except Exception as e:
                logging.error(f'Ошибка при получении папки захвата: {e}')
                return None
        return None
