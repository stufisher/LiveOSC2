from _Framework.SceneComponent import SceneComponent
from _Framework.Util import nop
from _Framework.SubjectSlot import subject_slot

from LO2ClipSlotComponent import LO2ClipSlotComponent
from LO2Mixin import LO2Mixin, wrap_init

from functools import wraps

class LO2SceneComponent(SceneComponent, LO2Mixin):

    clip_slot_component_type = LO2ClipSlotComponent
    
    def with_id(fn):
        @wraps(fn)
        def wrap(self, *a, **k):
            if self._scene_id > -1:
                return fn(*a, **k)
    
        return wrap
    
    
    @wrap_init
    def __init__(self, id = -1, *a, **k):
        self._scene = None
        self._scene_id = id
        super(LO2SceneComponent, self).__init__(*a, **k)

        self.set_default('_scene_id')
        
        callbacks = {'color': 'color', 'name': 'name'}
        for n,p in callbacks.iteritems():
            self.add_simple_callback('/live/scene/'+n, '_scene', p, self._is_scene, getattr(self, '_on_scene_'+n+'_changed'))
        
        self.add_callback('/live/scene/play', self._fire)
        self.add_callback('/live/scene/select', self._view)
    
    
    
    def _is_scene(self, msg):
        if len(msg) >= 3:
            return msg[2] == self._scene_id



    # Properties
    @property
    def id(self):
        return self._scene_id


    def _get_name(self):
        if self._scene is not None:
            return self._scene.name
        else:
            return ''

    def _set_name(self, name):
        if self._scene is not None:
            self._scene.name = name
    
    scene_name = property(_get_name, _set_name)


    def _get_color(self):
        if self._scene is not None:
            return self._scene.color
        else:
            return 0

    def _set_color(self, color):
        if self._scene is not None:
            self._scene.color = color
    
    color = property(_get_color, _set_color)
    

    
    # Overrides
    def _create_clip_slot(self):
        return self.clip_slot_component_type(len(self._clip_slots), self._scene_id)


    def _lo2_set_scene(self, scene):
        self._on_scene_name_changed.subject = scene
        self._on_scene_color_changed.subject = scene
    
    
    def update(self):
        if self._allow_updates:
            if self._scene != None and self.is_enabled():
                self.log_message('reassigning clips')
                if self._scene is not None:
                    diff = len(self._scene.clip_slots) - len(self._clip_slots)
                    
                    if diff > 0:
                        for i in range(diff):
                            self._clip_slots.append(self._create_clip_slot())
                    
                    if diff < 0:
                        for i in range(len(self._clip_slots)-1, len(self._scene.clip_slots)-1, -1):
                            self._clip_slots[i].disconnect()
                            self._clip_slots.remove(self._clip_slots[i])
                    
                    for i,c in enumerate(self._clip_slots):
                        c.set_clip_slot(self._scene.clip_slots[i])


    
    # Listeners
    @subject_slot('name')
    def _on_scene_name_changed(self):
        self.send('/live/scene/name', self._scene_id, self._scene.name)
    
    @subject_slot('color')
    def _on_scene_color_changed(self):
        self.send_default('/live/scene/color', self._scene.color)



    def _lo2__on_is_triggered_changed(self):
        self.send('/live/scene/state', self._scene_id, self._scene.is_triggered)




    # Callback
    def _fire(self, msg, src):
        if self._is_scene(msg):
            if self._scene is not None:
                self._scene.fire()


    def _view(self, msg, src):
        if self._is_scene(msg) and self._scene is not None:
            self.song().view.selected_scene = self._scene
