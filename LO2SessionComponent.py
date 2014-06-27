from _Framework.SessionComponent import SessionComponent
from _Framework.SceneComponent import SceneComponent

from LO2SceneComponent import LO2SceneComponent
from LO2Mixin import LO2Mixin, wrap_init

class LO2SessionComponent(SessionComponent, LO2Mixin):

    scene_component_type = LO2SceneComponent
    
    @wrap_init
    def __init__(self, *args, **kwargs):
        self._scene_count = -1
        self._scenes_count = 0
        super(LO2SessionComponent, self).__init__(*args, **kwargs)

        #self._selected_scene.disconnect()
        #self._selected_scene = None
        self._selected_scene.set_is_enabled(False)
        
        self._reassign_scenes()
        
        self.add_callback('/live/scene/name/block', self._scene_name_block)
        self.add_callback('/live/clip/name/block', self._clip_name_block)

        self.add_function_callback('/live/scenes', self._lo2_on_scene_list_changed)

    
    
    def _create_scene(self):
        #obj = SceneComponent if self._scene_count == -1 else self.scene_component_type
        sc = self.scene_component_type(num_slots=self._num_tracks, tracks_to_use_callback=self.tracks_to_use, id=self._scene_count)
        
        self._scene_count += 1
        return sc
    
    
    def on_scene_list_changed(self):
        self._reassign_scenes()
    
    
    def _reassign_scenes(self):
        self.log_message('reassigning scenes')
        diff = len(self.song().scenes) - len(self._scenes)
        
        if diff > 0:
            for i in range(diff):
                self._scenes.append(self._create_scene())
        
        if diff < 0:
            for i in range(len(self._scenes)-1, len(self.song().scenes)-1, -1):
                self._scene[i].disconnect()
                self._scene.remove(self._scene[i])
        
        for i,sc in enumerate(self._scenes):
            sc.set_scene(self.song().scenes[i])

    
    
    # Listeners
    def _lo2_on_scene_list_changed(self):
        if len(self.song().scenes) != self._scenes_count:
            self.send('/live/scenes', len(self.song().scenes))
            self._scenes_count = len(self.song().scenes)


    def _lo2_on_selected_scene_changed(self):
        idx = list(self.song().scenes).index(self.song().view.selected_scene)
        self.send('/live/scene/select', idx)



    # Scene Callbacks
    def _scene_name_block(self, msg, src):
        """ Gets block of scene names
        """
        b = []
        for i in range(msg[2], msg[2]+msg[3]):
            if i < len(self._scenes):
                s = self.scene[i]
                b.append(i, s.scene_name)
            else:
                b.append(i, '')

        self.send('/live/scene/name/block', b)
    
    
    def _scene_selected(self, msg, src):
        """  Selects a scene to view
            /live/scene/selected (int track) """
        if self.has_arg(msg):
            if msg[2] < len(self.song().scenes):
                self.song().view.selected_scene = self.song().scenes[msg[2]]
        else:
            idx = list(self.song().scenes).index(self.song().view.selected_scene)
            self.send('/live/scene/selected', idx)





    # Clip Callbacks
    def _clip_name_block(self, msg, src):
        """ Gets a block of clip names
        """
        b = []
        for i in range(msg[2], msg[2]+msg[3]):
            if i < len(self._scenes):
                s = self.scene[i]
                for j in range(msg[4], msg[4]+msg[5]):
                    if j < len(s._clip_slots):
                        c = s.clip_slots(j)
                        b.append(i, j, c.clip_name)
                    else:
                        b.append(i, j, '')
            else:
                b.append(i, j, '')
        
        self.send('/live/clip/name/block', b)

    
    
