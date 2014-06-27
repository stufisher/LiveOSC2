from _Framework.MixerComponent import MixerComponent

from LO2ChannelStripComponent import LO2ChannelStripComponent
from LO2Mixin import LO2Mixin, wrap_init

class LO2MixerComponent(MixerComponent, LO2Mixin):

    @wrap_init
    def __init__(self, *a, **kw):
        self._track_count = 0
        super(LO2MixerComponent, self).__init__(12, 12, *a, **kw)
        
        self.add_callback('/live/track/name/block', self._track_name_block)
    
        self.add_function_callback('/live/tracks', self._lo2_on_track_list_changed)
        self._selected_strip.set_track(None)
        self._selected_strip.set_is_enabled(False)
    
        self._register_timer_callback(self._update_mixer_vols)


    def _update_mixer_vols(self):
        pass
    
    
    
    def _create_strip(self):
        return LO2ChannelStripComponent()

    
    def _reassign_tracks(self):
        self.log_message('reassigning tracks')
        diff = len(self.tracks_to_use()) - len(self._channel_strips)

        if diff > 0:
            for i in range(diff):
                self._channel_strips.append(self._create_strip())

        if diff < 0:
                for i in range(len(self._channel_strips)-1, len(self.tracks_to_use())-1, -1):
                    self._channel_strips[i].disconnect()
                    self._channel_strips.remove(self._channel_strips[i])
    
        for i,cs in enumerate(self._channel_strips):
            cs.set_track(self.tracks_to_use()[i])


        for i,r in enumerate(self._return_strips):
            if i < len(self.song().return_tracks):
                r.set_track(self.song().return_tracks[i])
            else:
                r.set_track(None)
    
                            
    def _lo2__on_return_tracks_changed(self):
        self._reassign_tracks()
                            
        
    
    # Callbacks
    def _lo2_on_track_list_changed(self):
        if len(self.song().tracks) != self._track_count:
            self.send('/live/tracks', len(self.song().tracks))
            self._track_count = len(self.song().tracks)
    
    def _lo2_on_selected_track_changed(self):
        id, type = self.track_id_type(self.song().view.selected_track)
        
        self.send('/live/track/select', type, id)



    # Track Callbacks
    def _track_name_block(self, msg, src):
        """ Gets block of scene names
            """
        b = []
        for i in range(msg[2], msg[2]+msg[3]):
            if i < len(self._channel_strips):
                t = self.channel_strip(i)
                b.append(i, t.track_name)
            else:
                b.append(i, '')
        
        self.send('/live/track/name/block', b)
    