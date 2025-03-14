##################################################################################
## MIT License
##
## Copyright (c) 2019-2023 Vicon Motion Systems Ltd
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.
##################################################################################
"""Automatically generated CameraCalibrationServices for Vicon Shogun Live API."""

from enum import Enum
from vicon_core_api import SchemaServices
from vicon_core_api import ViconInterface


class CameraCalibrationServices(ViconInterface):
    """Support for creating, managing and maintaining camera calibrations."""

    class WandWaveProgressData(object):
        """Wand wave progress data for a single camera.

        Members:
            device_urn < string >: Device URN of camera.
            wand_count < int >: Number of frames with a wand detection. All cameras must see wand detections across their field of view in order to calibrate
                successfully.
            image_error < float >: Image error in pixels for current calibration.
            is_calibrated < bool >: If the camera is calibrated.
        """
        def __init__(self):
            """Initialiser for WandWaveProgressData."""
            self.device_urn = ""
            self.wand_count = 0
            self.image_error = 0.0
            self.is_calibrated = False

        def __str__(self):
            """Provide JSON string representation for WandWaveProgressData."""
            return SchemaServices.write(self)


    class ECameraCalibrationState(Enum):
        """State of camera calibration system.

        Enum Values:
            ENone: No calibration operation in progress, system is ready to start.
            ECollecting: Collecting data.
            EProcessing: Processing data.
            ECompleted: Operation completed, system is ready to start another.
            ECanceling: Operation is being canceled.
            ECanceled: Operation canceled, system is ready to start another.
        """
        ENone = 0
        ECollecting = 1
        EProcessing = 2
        ECompleted = 3
        ECanceling = 4
        ECanceled = 5


    class ESetOriginReadyState(Enum):
        """Whether set origin is ready to process.

        Enum Values:
            EReady: Ready to set the volume origin.
            ENotReadyLabeledDataNotDetected: No labeled reconstructions detected.
            ENotReadyInsufficientFramesCollected: Calibration object hasn't been detected in enough frames yet.
            ENotReadyMotionDetected: Calibration object has moved.
            ENotReadyInternalError: An internal error has occurred.
            ENotReadyNoCalibrationObject: Calibration object not detected.
            ENotReadyMultipleSubjectsDetected: Multiple subjects detected. Exactly one calibration object should be visible.
            ENotReadyCalibrationObjectChanged: Calibration object was changed during set origin.
            ENotReadyInsufficentConsistentCameras: Not enough cameras can see all the calibration object markers.
        """
        EReady = 0
        ENotReadyLabeledDataNotDetected = 1
        ENotReadyInsufficientFramesCollected = 2
        ENotReadyMotionDetected = 3
        ENotReadyInternalError = 4
        ENotReadyNoCalibrationObject = 5
        ENotReadyMultipleSubjectsDetected = 6
        ENotReadyCalibrationObjectChanged = 7
        ENotReadyInsufficentConsistentCameras = 8


    class ECameraCalibrationType(Enum):
        """Type of camera calibration operation.

        Enum Values:
            EMasking: Mask out unwanted IR sources in the camera's field of view.
            EWandWaveCalibration: Camera calibration using wand wave detections.
            ESetOrigin: Set the origin of the calibrated capture volume.
            ESetFloorPlane: Set the floor plane of the calibrated capture volume.
            ERecoverCameraPosition: Recalibrate the position and orientation of selected cameras.
        """
        EMasking = 0
        EWandWaveCalibration = 1
        ESetOrigin = 2
        ESetFloorPlane = 3
        ERecoverCameraPosition = 4


    class CameraCalibrationDeviceRecord(object):
        """Camera calibration record for a single device. Temperatures are tracked during calibration because thermal expansion causes
        changes in the optical characteristics of the camera lens assembly. If the camera temperature is not stable this might reduce
        the accuracy of the calibration.

        Members:
            start_temperature < int >: Camera temperature at the start of the calibration operation.
            end_temperature < int >: Camera temperature at the end of the calibration operation.
        """
        def __init__(self):
            """Initialiser for CameraCalibrationDeviceRecord."""
            self.start_temperature = 0
            self.end_temperature = 0

        def __str__(self):
            """Provide JSON string representation for CameraCalibrationDeviceRecord."""
            return SchemaServices.write(self)


    class CameraCalibrationData(object):
        """Data recorded at the time of a camera calibration.

        Members:
            calibration_timestamp < int >: When the initial wand wave was performed (UNIX Epoch timestamp in seconds).
            device_records < [(string,CameraCalibrationServices.CameraCalibrationDeviceRecord)] >: Data for calibrated cameras recorded during the calibration operation, indexed by device URN.
        """
        def __init__(self):
            """Initialiser for CameraCalibrationData."""
            self.calibration_timestamp = 0
            self.device_records = []

        def __str__(self):
            """Provide JSON string representation for CameraCalibrationData."""
            return SchemaServices.write(self)


    def import_camera_calibration(self, file_path):
        """Import a camera calibration from file (*.mcp *.xcp). The file path must be accessible from the remote host.

        Args:
            file_path < string >: Absolute path to camera calibration file.

        Return:
            return < Result >: Ok - On success.
                NotFound - If file does not exist.
                NotSupported - If file extension is not '.mcp' or '.xcp'.
                FileIOFailure - If file could not be loaded.
        """
        return self.client.send_command("CameraCalibrationServices.ImportCameraCalibration", file_path)

    def export_camera_calibration(self, file_path):
        """Export a camera calibration to an XCP file (*.xcp). The file path must be accessible from the remote host.

        Args:
            file_path < string >: Absolute path to desired location of camera calibration file.

        Return:
            return < Result >: Ok - On success.
                NotSupported - If file extension is not '.xcp'.
                FileIOFailure - If file could not be saved.
        """
        return self.client.send_command("CameraCalibrationServices.ExportCameraCalibration", file_path)

    def clear_camera_calibration(self):
        """Clear the current camera calibration.

        Return:
            return < Result >: Ok - On success.
        """
        return self.client.send_command("CameraCalibrationServices.ClearCameraCalibration")

    def camera_calibration_folder(self):
        """Get the folder path for camera calibration files.

        Return:
            return < Result >: Ok - On success.
            folder_path < string >: Absolute path to camera calibration folder.
        """
        return self.client.send_command("CameraCalibrationServices.CameraCalibrationFolder")

    def start_masking(self):
        """Start masking out unwanted infra-red light sources in all cameras.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If the system isn't able to start this operation.
            camera_calibration_session_id < int >: Id for the new camera calibration session.
        """
        return self.client.send_command("CameraCalibrationServices.StartMasking")

    def stop_masking(self, camera_calibration_session_id):
        """Stop masking and save the camera masks in the camera masks.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If session is not in progress or is not a masking session.
        """
        return self.client.send_command("CameraCalibrationServices.StopMasking", camera_calibration_session_id)

    def cancel_masking(self, camera_calibration_session_id):
        """Cancel masking. No changes will be made to the camera masks.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If session is not in progress or is not a masking session.
        """
        return self.client.send_command("CameraCalibrationServices.CancelMasking", camera_calibration_session_id)

    def start_wand_wave(self):
        """Start a wand wave to compute the relative position, orientation and lens parameters of all cameras in the system.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If the system isn't able to start this operation.
            camera_calibration_session_id < int >: Id for the new camera calibration session.
        """
        return self.client.send_command("CameraCalibrationServices.StartWandWave")

    def start_wand_wave_selected(self, camera_device_urns):
        """Start a wand wave to compute the relative position, orientation and lens parameters of selected cameras in the system.

        Args:
            camera_device_urns < [string] >: Camera device URNs to calibrate.

        Return:
            return < Result >: Ok - On success.
                InvalidArgument - If no valid camera device URNs were specified.
                NotPermitted - If the system isn't able to start this operation.
            camera_calibration_session_id < int >: Id for the new camera calibration session.
        """
        return self.client.send_command("CameraCalibrationServices.StartWandWaveSelected", camera_device_urns)

    def stop_wand_wave(self, camera_calibration_session_id):
        """Stop the wand wave and save the new camera calibration.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If session is not in progress or is not a wand wave session.
        """
        return self.client.send_command("CameraCalibrationServices.StopWandWave", camera_calibration_session_id)

    def cancel_wand_wave(self, camera_calibration_session_id):
        """Cancel the wand wave. No changes will be made to the camera calibration.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If session is not in progress or is not a wand wave session.
        """
        return self.client.send_command("CameraCalibrationServices.CancelWandWave", camera_calibration_session_id)

    def wand_wave_progress(self, camera_calibration_session_id):
        """Get the current wand wave progress.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotAvailable - If session is not the latest wand wave session.
            state < CameraCalibrationServices.ECameraCalibrationState >: Current calibration session state.
            percentage_complete < int >: Percentage towards completion of current state.
            camera_wand_wave_progress < [CameraCalibrationServices.WandWaveProgressData] >: Wand wave progress data for each camera.
        """
        return self.client.send_command("CameraCalibrationServices.WandWaveProgress", camera_calibration_session_id)

    def start_set_origin(self):
        """Prepare to set the camera calibration origin.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If the system isn't able to start this operation.
            camera_calibration_session_id < int >: Id for the new camera calibration session.
        """
        return self.client.send_command("CameraCalibrationServices.StartSetOrigin")

    def set_origin(self, camera_calibration_session_id):
        """Set the camera calibration origin to the calibration object pose, and save the new camera calibration.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If session is not in progress or is not a set origin session.
                Failed - If the system was not ready to set origin.
        """
        return self.client.send_command("CameraCalibrationServices.SetOrigin", camera_calibration_session_id)

    def cancel_set_origin(self, camera_calibration_session_id):
        """Cancel setting the camera calibration origin. No changes will be made to the camera calibration.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If session is not in progress or is not a set origin session.
        """
        return self.client.send_command("CameraCalibrationServices.CancelSetOrigin", camera_calibration_session_id)

    def set_origin_progress(self, camera_calibration_session_id):
        """Get the current set origin progress.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotAvailable - If session is not the latest set origin session.
            calibration_state < CameraCalibrationServices.ECameraCalibrationState >: Current camera calibration session state.
            set_origin_ready_state < CameraCalibrationServices.ESetOriginReadyState >: State of set origin readiness.
        """
        return self.client.send_command("CameraCalibrationServices.SetOriginProgress", camera_calibration_session_id)

    def start_set_floor_plane(self):
        """Prepare to set the camera calibration floor plane, using 3 or more markers placed on the floor.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If the system isn't able to start this operation.
            camera_calibration_session_id < int >: Id for the new camera calibration session.
        """
        return self.client.send_command("CameraCalibrationServices.StartSetFloorPlane")

    def set_floor_plane(self, camera_calibration_session_id):
        """Set the camera calibration floor plane from the marker positions, and save the new camera calibration.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If session is not in progress or is not a set origin session.
                Failed - If floor plane could not be computed from marker detections.
        """
        return self.client.send_command("CameraCalibrationServices.SetFloorPlane", camera_calibration_session_id)

    def cancel_set_floor_plane(self, camera_calibration_session_id):
        """Cancel setting the camera calibration origin. No changes will be made to the camera calibration.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If session is not in progress or is not a set origin session.
        """
        return self.client.send_command("CameraCalibrationServices.CancelSetFloorPlane", camera_calibration_session_id)

    def set_floor_extents(self):
        """Set the floor extents of the volume, based on camera coverage.

        Return:
            return < Result >: Ok - On success.
        """
        return self.client.send_command("CameraCalibrationServices.SetFloorExtents")

    def auto_number_cameras(self):
        """Assign numbers to the cameras automatically, in order of their position in the volume.

        Return:
            return < Result >: Ok - On success.
        """
        return self.client.send_command("CameraCalibrationServices.AutoNumberCameras")

    def start_recover_camera_position(self, camera_device_urns):
        """Recalibrate the position and orientation of the selected cameras, using tracks generated from moving markers. For best results,
        this should be a small fraction of the cameras, ideally one or two at a time.

        Args:
            camera_device_urns < [string] >: Camera device URNs to recover.

        Return:
            return < Result >: Ok - On success
                InvalidArgument - If no valid camera device URNs were specified.
                NotPermitted - If the system isn't able to start this operation.
            camera_calibration_session_id < int >: Id for the new camera calibration session.
        """
        return self.client.send_command("CameraCalibrationServices.StartRecoverCameraPosition", camera_device_urns)

    def stop_recover_camera_position(self, camera_calibration_session_id):
        """Stop camera position recovery.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success
                NotPermitted - If session is not in progress or is not a recover camera pose session.
        """
        return self.client.send_command("CameraCalibrationServices.StopRecoverCameraPosition", camera_calibration_session_id)

    def cancel_recover_camera_position(self, camera_calibration_session_id):
        """Cancel camera position recovery. No changes will be made to the camera calibration.

        Args:
            camera_calibration_session_id < int >: Camera calibration session id.

        Return:
            return < Result >: Ok - On success.
                NotPermitted - If session is not in progress or is not a recover camera pose session.
        """
        return self.client.send_command("CameraCalibrationServices.CancelRecoverCameraPosition", camera_calibration_session_id)

    def latest_camera_calibration_state(self):
        """Get the latest camera calibration state.

        Return:
            return < Result >: Ok - On success.
            camera_calibration_session_id < int >: Latest camera calibration session id.
            type < CameraCalibrationServices.ECameraCalibrationType >: Latest camera calibration session type.
            state < CameraCalibrationServices.ECameraCalibrationState >: Latest camera calibration session state.
        """
        return self.client.send_command("CameraCalibrationServices.LatestCameraCalibrationState")

    def add_latest_camera_calibration_changed_callback(self, function):
        """Callback issued whenever the latest calibration changes.

        Args:
            camera_calibration_session_id < int >: Latest camera calibration session id.
            type < CameraCalibrationServices.ECameraCalibrationType >: Current camera calibration session type.
            state < CameraCalibrationServices.ECameraCalibrationState >: Current camera calibration session state.
        """
        return self.client.add_callback("CameraCalibrationServices.LatestCameraCalibrationChangedCallback", function)

    def active_camera_calibration_data(self):
        """Get the active camera calibration data. This may be from the latest camera calibration operation or loaded camera calibration
        file.

        Return:
            return < Result >: Ok - On success.
                NotFound - If no active camera calibration was found.
            camera_calibration_data < CameraCalibrationServices.CameraCalibrationData >: Camera calibration data.
        """
        return self.client.send_command("CameraCalibrationServices.ActiveCameraCalibrationData")

    def add_active_camera_calibration_data_changed_callback(self, function):
        """Callback issued whenever the active camera calibration data changes."""
        return self.client.add_callback("CameraCalibrationServices.ActiveCameraCalibrationDataChangedCallback", function)

    def remove_callback(self, callback_id):
        """Remove callback of any type using the id supplied when it was added."""
        return self.client.remove_callback(callback_id)



SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "TypeName": "CameraCalibrationServices"}""")
SchemaServices.register_json_schema(CameraCalibrationServices.WandWaveProgressData, """{"Type": "NamedTuple", "TypeName": "CameraCalibrationServices.WandWaveProgressData", "SubSchemas": [["DeviceURN", {"Type":
                                                                                       "String"}], ["WandCount", {"Type": "UInt32"}], ["ImageError", {"Type": "Float32"}], ["IsCalibrated", {"Type": "Bool"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices.ECameraCalibrationState, """{"Type": "Enum32", "TypeName": "CameraCalibrationServices.ECameraCalibrationState", "EnumValues": [["None", 0], ["Collecting",
                                                                                          1], ["Processing", 2], ["Completed", 3], ["Canceling", 4], ["Canceled", 5]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices.ESetOriginReadyState, """{"Type": "Enum32", "TypeName": "CameraCalibrationServices.ESetOriginReadyState", "EnumValues": [["Ready", 0], ["NotReadyLabeledDataNotDetected",
                                                                                       1], ["NotReadyInsufficientFramesCollected", 2], ["NotReadyMotionDetected", 3], ["NotReadyInternalError", 4], ["NotReadyNoCalibrationObject",
                                                                                       5], ["NotReadyMultipleSubjectsDetected", 6], ["NotReadyCalibrationObjectChanged", 7], ["NotReadyInsufficentConsistentCameras",
                                                                                       8]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices.ECameraCalibrationType, """{"Type": "Enum32", "TypeName": "CameraCalibrationServices.ECameraCalibrationType", "EnumValues": [["Masking", 0], ["WandWaveCalibration",
                                                                                         1], ["SetOrigin", 2], ["SetFloorPlane", 3], ["RecoverCameraPosition", 4]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices.CameraCalibrationDeviceRecord, """{"Type": "NamedTuple", "TypeName": "CameraCalibrationServices.CameraCalibrationDeviceRecord", "SubSchemas": [["StartTemperature",
                                                                                                {"Type": "UInt32"}], ["EndTemperature", {"Type": "UInt32"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices.CameraCalibrationData, """{"Type": "NamedTuple", "TypeName": "CameraCalibrationServices.CameraCalibrationData", "SubSchemas": [["CalibrationTimestamp",
                                                                                        {"Type": "Int64"}], ["DeviceRecords", {"Type": "List", "SubSchemas": [["", {"Type": "Tuple", "SubSchemas": [["", {"Type":
                                                                                        "String"}], ["", {"Type": "Ref", "TypeName": "CameraCalibrationServices.CameraCalibrationDeviceRecord"}]]}]]}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.ImportCameraCalibration", "SubSchemas":
                                                                  [["Return", {"Type": "UInt32", "Role": "Result"}], ["FilePath", {"Type": "String", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.ExportCameraCalibration", "SubSchemas":
                                                                  [["Return", {"Type": "UInt32", "Role": "Result"}], ["FilePath", {"Type": "String", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.ClearCameraCalibration", "SubSchemas":
                                                                  [["Return", {"Type": "UInt32", "Role": "Result"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.CameraCalibrationFolder", "SubSchemas":
                                                                  [["Return", {"Type": "UInt32", "Role": "Result"}], ["FolderPath", {"Type": "String", "Role": "Output"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.StartMasking", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Output"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.StopMasking", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.CancelMasking", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.StartWandWave", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Output"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.StartWandWaveSelected", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Output"}], ["CameraDeviceURNs",
                                                                  {"Type": "List", "Role": "Input", "SubSchemas": [["", {"Type": "String"}]]}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.StopWandWave", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.CancelWandWave", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.WandWaveProgress", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}], ["State", {"Type":
                                                                  "Ref", "Role": "Output", "TypeName": "CameraCalibrationServices.ECameraCalibrationState"}], ["PercentageComplete", {"Type":
                                                                  "UInt32", "Role": "Output"}], ["CameraWandWaveProgress", {"Type": "List", "Role": "Output", "SubSchemas": [["", {"Type":
                                                                  "Ref", "TypeName": "CameraCalibrationServices.WandWaveProgressData"}]]}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.StartSetOrigin", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Output"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.SetOrigin", "SubSchemas": [["Return", {"Type":
                                                                  "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.CancelSetOrigin", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.SetOriginProgress", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}], ["CalibrationState",
                                                                  {"Type": "Ref", "Role": "Output", "TypeName": "CameraCalibrationServices.ECameraCalibrationState"}], ["SetOriginReadyState",
                                                                  {"Type": "Ref", "Role": "Output", "TypeName": "CameraCalibrationServices.ESetOriginReadyState"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.StartSetFloorPlane", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Output"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.SetFloorPlane", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.CancelSetFloorPlane", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.SetFloorExtents", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.AutoNumberCameras", "SubSchemas": [["Return",
                                                                  {"Type": "UInt32", "Role": "Result"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.StartRecoverCameraPosition", "SubSchemas":
                                                                  [["Return", {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Output"}],
                                                                  ["CameraDeviceURNs", {"Type": "List", "Role": "Input", "SubSchemas": [["", {"Type": "String"}]]}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.StopRecoverCameraPosition", "SubSchemas":
                                                                  [["Return", {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.CancelRecoverCameraPosition", "SubSchemas":
                                                                  [["Return", {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.LatestCameraCalibrationState", "SubSchemas":
                                                                  [["Return", {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Output"}],
                                                                  ["Type", {"Type": "Ref", "Role": "Output", "TypeName": "CameraCalibrationServices.ECameraCalibrationType"}], ["State", {"Type":
                                                                  "Ref", "Role": "Output", "TypeName": "CameraCalibrationServices.ECameraCalibrationState"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Callback", "TypeName": "CameraCalibrationServices.LatestCameraCalibrationChangedCallback",
                                                                  "SubSchemas": [["CameraCalibrationSessionId", {"Type": "UInt32", "Role": "Input"}], ["Type", {"Type": "Ref", "Role": "Input",
                                                                  "TypeName": "CameraCalibrationServices.ECameraCalibrationType"}], ["State", {"Type": "Ref", "Role": "Input", "TypeName":
                                                                  "CameraCalibrationServices.ECameraCalibrationState"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Function", "TypeName": "CameraCalibrationServices.ActiveCameraCalibrationData", "SubSchemas":
                                                                  [["Return", {"Type": "UInt32", "Role": "Result"}], ["CameraCalibrationData", {"Type": "Ref", "Role": "Output", "TypeName":
                                                                  "CameraCalibrationServices.CameraCalibrationData"}]]}""")
SchemaServices.register_json_schema(CameraCalibrationServices, """{"Type": "NamedTuple", "Role": "Callback", "TypeName": "CameraCalibrationServices.ActiveCameraCalibrationDataChangedCallback"}""")
