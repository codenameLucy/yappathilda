import obsws_python as obs


class OBSWebsocket:
    def __init__(self, credentials):
        self.credentials = credentials
        self.obs_ws = obs.ReqClient(host=self.credentials['host'], port=self.credentials['port'],
                                    password=self.credentials['password'], timeout=3)

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
        return self.obs_ws.get_scene_item_id(scene_name, source_name).scene_item_id
