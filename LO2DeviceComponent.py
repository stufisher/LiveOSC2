from _Framework.DeviceComponent import DeviceComponent
from _Framework.SubjectSlot import subject_slot


from LO2ParameterComponent import LO2ParameterComponent
from LO2Mixin import LO2Mixin


class LO2DeviceComponent(DeviceComponent, LO2Mixin):


    def __init__(self):
        self._parameters = []
        super(LO2DeviceComponent, self).__init__()

        self.set_default('_track_id', '_device_id')

        for ty in self._track_types:
            self.add_callback('/live/'+ty+'device/range', self._device_range)
            self.add_callback('/live/'+ty+'device/param', self._device_param)
            self.add_callback('/live/'+ty+'device/select', self._view)


    def _is_device(self, msg):
        if 'return' in msg[0]:
            ty = 1
        elif 'master' in msg[0]:
            ty = 2
        else:
            ty = 0

        d = msg[2] if ty == 2 else msg[3]
        check_id = msg[2] == self._track_id if self._type != 2 else True

        return check_id and self._type == ty and d == self._device_id


    def set_device(self, device):
        self.log_message('set device')
        super(LO2DeviceComponent, self).set_device(device)

        self._track_id, self._type = self.track_id_type(device.canonical_parent)
        self._device_id = list(device.canonical_parent.devices).index(device)

        self._on_parameters_changed.subject = device
        self._on_parameters_changed()


    @subject_slot('parameters')
    def _on_parameters_changed(self):
        self.log_message('params changed')
        diff = len(self._device.parameters) - len(self._parameters)

        if diff > 0:
            for i in range(diff):
                self._parameters.append(LO2ParameterComponent())

        if diff < 0:
            for i in range(len(self._parameters)-1, len(self._device.parameters)-1, -1):
                self._parameters[i].disconnect()
                self._parameters.remove(self._parameters[i])

        for i,pc in enumerate(self._parameters):
            pc.set_parameter(self._device.parameters[i])




    def _device_range(self, msg, src):
        if self._is_device(msg) and self._device is not None:
            if self._type == 2:
                d = msg[2] if len(msg) >= 3 else None
                p = msg[3] if len(msg) >= 4 else None
            else:
                d = msg[3] if len(msg) >= 4 else None
                p = msg[4] if len(msg) >= 5 else None


            if d is not None:
                if p is not None:
                    if p < len(self._device.parameters):
                        prm = self._device.parameters[p]
                        # type 2 = master track
                        if self._type == 2:
                            self.send('/live/'+self._track_types[self._type]+'device/range', self._device_id, p, prm.min, prm.max)
                        else:
                            self.send_default('/live/'+self._track_types[self._type]+'device/range', p, prm.min, prm.max)

                else:
                    prms = []
                    for i,p in enumerate(self._device.parameters):
                        prms.extend([i,p.min,p.max])

                    # type 2 = master track
                    if self._type == 2:
                        self.send('/live/'+self._track_types[self._type]+'device/range', self._device_id, *prms)
                    else:
                        self.send_default('/live/'+self._track_types[self._type]+'device/range', *prms)



    def _device_param(self, msg, src):
        if self._is_device(msg) and self._device is not None:
            if self._type == 2:
                p = msg[3] if len(msg) >= 4 else None
                v = msg[4] if len(msg) >= 5 else None
            else:
                p = msg[4] if len(msg) >= 5 else None
                v = msg[5] if len(msg) >= 6 else None

            if p is not None:
                if p < len(self._device.parameters):
                    prm = self._device.parameters[p]

                    # If a parameter value was passed, set it.
                    if v is not None:
                        prm.value = v

                    # Send the current value of the parameter.
                    # type 2 = master track
                    if self._type == 2:
                        self.send('/live/'+self._track_types[self._type]+'device/param', p, prm.value, prm.name)
                    else:
                        self.send_default('/live/'+self._track_types[self._type]+'device/param', p, prm.value, prm.name)

            # If a parameter id wasn't sent, send all the information about available parameters for this device.
            else:
                prms = []
                for i,p in enumerate(self._device.parameters):
                    prms.extend([i,p.value,p.name])

                # type 2 = master track
                if self._type == 2:
                    self.send('/live/'+self._track_types[self._type]+'device/param', *prms)
                else:
                    self.send_default('/live/'+self._track_types[self._type]+'device/param', *prms)


    def _view(self, msg, src):
        if self._is_device(msg) and self._device is not None:
            self.song().view.selected_track = self._device.canonical_parent
            self.song().view.select_device(self._device)
            self.application().view.show_view('Detail/DeviceChain')



    def _envelope(self, msg, src):
        if self._is_device(msg):
            if self._type == 2:
                p = msg[3] if len(msg) >= 4 else None
                t = msg[4] if len(msg) >= 5 else None
                v = msg[5] if len(msg) >= 6 else None
                l = msg[6] if len(msg) >= 7 else None
            else:
                p = msg[4] if len(msg) >= 5 else None
                t = msg[5] if len(msg) >= 6 else None
                v = msg[6] if len(msg) >= 7 else None
                l = msg[7] if len(msg) >= 8 else None

            if p < len(self._device.parameters) and t is not None:
                prm = self._device.parameters[p]


