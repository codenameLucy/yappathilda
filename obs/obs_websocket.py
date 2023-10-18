import obsws_python as obs
from obsws_python.error import OBSSDKError


class OBSSceneMissingException(Exception):
    pass


class OBSConnectionFailedException(Exception):
    pass


class OBSWebsocket:
    def __init__(self, credentials):
        self.credentials = credentials
        try:
            self.obs_ws = obs.ReqClient(host=self.credentials['host'], port=self.credentials['port'],
                                        password=self.credentials['password'], timeout=3)
        except OBSSDKError as e:
            raise OBSConnectionFailedException("Connection with websocket to obs failed,"
                                               " did you enable your websocket in OBS?") from e

    def change_visibility_tts_scene(self, visible: bool):
        self.obs_ws.set_scene_item_enabled(
            self.credentials['scene_name'],
            enabled=visible,
            item_id=self._get_scene_item_id(
                scene_name=self.credentials['scene_name'],
                source_name=self.credentials['source_name']
            )
        )

    def _get_scene_item_id(self, scene_name: str, source_name: str) -> int:
        try:
            scene_item_id = self.obs_ws.get_scene_item_id(scene_name, source_name).scene_item_id
        except OBSSDKError as e:
            raise OBSSceneMissingException(
                "There is a high likelihood your scenes are"
                " missing in obs or the names mismatch the ones in your config") from e
        return scene_item_id
