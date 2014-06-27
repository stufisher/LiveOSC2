from __future__ import with_statement
from _Framework.ControlSurface import ControlSurface

from LO2SessionComponent import LO2SessionComponent
from LO2MixerComponent import LO2MixerComponent
from LO2TransportComponent import LO2TransportComponent

from LO2Mixin import LO2Mixin
from LO2OSC import LO2OSC


class LiveOSC2(ControlSurface):


    def __init__(self, c_instance):
        super(LiveOSC2, self).__init__(c_instance)
        
        with self.component_guard():
            LO2OSC.set_log(self.log_message)
            self.osc_handler = LO2OSC()
            
            LO2Mixin.set_osc_handler(self.osc_handler)
            LO2Mixin.set_log(self.log_message)
            
            self._mixer = LO2MixerComponent(1)
            self._session = LO2SessionComponent(1,1)
            self._session.set_mixer(self._mixer)
            self._transport = LO2TransportComponent()
            
            self.parse()

        
        self.show_message('LiveOSC2 loaded')
        self.osc_handler.send('/live/startup', 1)


    def disconnect(self):
        self.osc_handler.shutdown()


    def parse(self):
        self.osc_handler.process()
        self.schedule_message(1, self.parse)