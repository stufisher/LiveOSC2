# -----------------------------------------------------------------
# LiveOSC2
# Live 9 Compatible version of LiveOSC using _Framework
# Stu Fisher <st8@q3f.org>
# -----------------------------------------------------------------

from _Framework.SubjectSlot import SubjectSlot, CallableSlotMixin
from _Framework.Util import mixin
from functools import wraps, partial
import types
import OSC


# -----------------------------------------------------------------
# This decorator allows us to inject code into framework listeners
# without having to subclass and super each one. This is important
# for subject_slots where these methods are already decorated
#
# It will iterate through the class methods searching for ones
# beginning _lo2_<FrameworkListener>
def _decorate(fn, child, name):
    def wrap(*a, **kw):
        LO2Mixin.log_message('calling LO2 wrapper: '+name)
    
        ret = fn(*a, **kw)
        child(*a, **kw)
        
        return ret

    return wrap


def wrap_init(fn):
    def decorate(self, *a, **kw):
        fn(self, *a, **kw)
        
        if not hasattr(self, 'liveosc'):
            for m in dir(self):
                if m.startswith('_lo2_'):
                    method = getattr(self, m.replace('_lo2_', ''))
                    child = getattr(self, m)
                    
                    # If its a subject slot replace the listener
                    if hasattr(method, 'function'):
                        #method.function = _decorate(method.function, child, m)
                        method.listener = _decorate(method.function, child, m)
                    
                    # If its a normal method just overwrite it
                    else:
                        setattr(self, m.replace('_lo2_', ''), _decorate(method, child, m))

            self.liveosc = True

    return decorate


# -----------------------------------------------------------------
# Various Helpers
class LO2Mixin:

    _track_types = ['track/', 'return/', 'master/']
    _default_args = []
    _subject_slots = []
    _is_enabled_ovr = True
    _registered_callbacks = []
    
    @staticmethod
    def set_log(func):
        LO2Mixin.log_message = func

    
    @staticmethod
    def set_osc_handler(handler):
        LO2Mixin._osc_handler = handler
    
    @staticmethod
    def release_attributes():
        LO2Mixin._osc_handler = None
        LO2Mixin.log_message = None

    
    
    def set_is_enabled(self, val):
        self._is_enabled_ovr = val
    
    
    def bundle(self):
        return OSC.OSCBundle()
    
    
    def send(self, addr, *msg):
        if self._is_enabled_ovr:
            self._osc_handler.send(addr, tuple(msg))

    def sendb(self, bundle):
        self._osc_handler.send_message(bundle)
    
    
    def disconnect(self):
        self.log_message('Disconnecting instance' + str(self))
        for cb in self._registered_callbacks:
            self._osc_handler._callback_manager.rem(cb)

        self.log_message(str(self._osc_handler._callback_manager.callbacks))

    def add_callback(self, msg, func):
        """ Add a callback for an osc message """
        if self._osc_handler:
            self._osc_handler._callback_manager.add(msg, func)
            self._registered_callbacks.append(func)
    

    def add_default_callback(self, addr, subject, property, type):
        """ Add a simple one argument osc setter / getter
          eg.  
            self.add_default_callback('/live/tempo', self.song(), 'tempo', float)
        """
        def cb(msg, src):
            if self.has_arg(msg):
                setattr(subject, property, msg[2])
            else:
                self.send(addr, type(getattr(subject, property)))
    
        self.add_callback(addr, cb)


    def add_function_callback(self, addr, fn, *a):
        """ Add a simple callback that just calls a function """

        def cb(msg, src):
            if callable(fn):
                fn(*a)
        
        self.add_callback(addr, cb)
    
    
    def add_simple_callback(self, addr, obj, property, check, fn):
        """ Add a simple setter / getter callback based on default args """
        
        def cb(msg, src):
            if check(msg):
                if len(msg) == len(self._default_args) + 2 or (len(msg) == len(self._default_args) + 3 and msg[-1] == 'query'):
                    fn()
                else:
                    setattr(self._get_object(obj), property, msg[len(self._default_args) + 2])
                            
        self.add_callback(addr, cb)
    
                            
    def _get_object(self, obj):
        objs = obj.split('.')
                   
        current = getattr(self, objs[0])
        if len(objs) > 1:
            for o in objs[1:]:
                current = getattr(current, o)
                            
        return current
            
                            
    
    def set_default(self, *a):
        self._default_args = a
    
    def send_default(self, addr, *ar):
        args = []
        for a in self._default_args:
            args.append(getattr(self, a))
        args.extend(ar)
        self.send(addr, *args)
    

    def add_listener(self, addr, property, obj, value, *a):
        """ Dynamically add a subject slot and callback """
        def fn(self):
            self.log_message('listener called: ' + addr + ' ' + property)
            
            args = []
            for arg in a:
                args.append(getattr(self, arg))
            args.append(getattr(self._get_object(obj), value))
            
            self.send(addr, *args)
    
        fn = wraps(fn)(mixin(SubjectSlot, CallableSlotMixin)(event=property, listener=partial(fn,self), function=partial(fn,self)))
        self.register_slot(fn)
        
        self._subject_slots.append('_on_'+property+'_changed')
        
        if not hasattr(self, '_on_'+property+'_changed'):
            setattr(self, '_on_'+property+'_changed', fn)
    
    
    def track_id_type(self, t):
        """ Returns the track type and id for a given track """
        
        if t in self.song().visible_tracks:
            id = list(self.song().visible_tracks).index(t)
            type = 0
        elif t in self.song().return_tracks:
            id = list(self.song().return_tracks).index(t)
            type = 1
        elif t == self.song().master_track:
            id = 0
            type = 2
        else:
            id = None
            type = None

        return id, type


    def has_arg(self, msg):
        return not (len(msg) == 2 or (len(msg) == 3 and msg[2] == 'query'))





