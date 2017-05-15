import OSC
import socket
import sys
import errno
import traceback

class LO2OSC(object):

    @staticmethod
    def set_log(func):
        LO2OSC.log_message = func

    @staticmethod
    def release_attributes():
        LO2OSC.log_message = None


    def __init__(self, remotehost = '127.0.0.1', remoteport=9000, localhost='127.0.0.1', localport=9001):

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setblocking(0)

        self._local_addr = (localhost, localport)
        self._remote_addr = (remotehost, remoteport)
        
        self._socket.bind(self._local_addr)
        self.log_message('LiveOSC2 starting on: ' + str(self._local_addr) + ', remote addr: '+ str(self._remote_addr))

        self._callback_manager = OSC.CallbackManager()
        self._callback_manager.add('/live/set_peer', self._set_peer)


    def send(self, address, msg):
        oscmsg = OSC.OSCMessage(address, msg)
        self._socket.sendto(oscmsg.getBinary(), self._remote_addr)

    def send_message(self, message):
        self._socket.sendto(message.getBinary(), self._remote_addr)
    
    
    def process(self):
        try:
            while 1:
                self._data, self._addr = self._socket.recvfrom(65536)

                try:
                    self._callback_manager.handle(self._data, self._addr)

                except OSC.NoSuchCallback, e:
                    errmsg = 'Unknown callback: '+str(e.args[0])
                    self.log_message('LiveOSC: '+errmsg)
                    self.send('/live/error', errmsg)

                except Exception, e:
                    errmsg = type(e).__name__+': '+str(e.args[0])
                    tb = sys.exc_info()
                    stack = traceback.extract_tb(tb[2])

                    self.log_message('LiveOSC: error handling message ' + errmsg)
                    self.send('/live/error', errmsg)
                    self.log_message("".join(traceback.format_list(stack)))

        except socket.error, e:
            if e.errno == errno.EAGAIN:
                return
                self.log_message('LiveOSC: Socket unavailable')

        except Exception, e:
            self.log_message('LiveOSC: error handling message '+type(e).__name__+':'+str(e.args[0]))



    def shutdown(self):
        self._socket.close()


    def _set_peer(self, msg, source):
        host = msg[2]
        if host == '':
            host = source[0]
        port = msg[3]
        self.log_message('LiveOSC2: reconfigured to send to ' + host + ':' + str(port))
        self._remote_addr = (host, port)
        