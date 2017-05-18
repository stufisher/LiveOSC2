LiveOSC2
========

New version of LiveOSC for Live 9. Added various new functionality from L9, like the ability to create / delete clips. Assign devices from the browser, more detailed manipulation of midi clip, as well as various new listeners

I have tidied up most of the calls to group them by type, as well as removing what i believe to be redundant calls. If you think things are missing please get in touch.

LiveOSC binds to localhost by default receiving OSC on 9000 and sending on 9001  
You can change this dyncamically using:
    /live/set_peer [host] [port]


Calls without an argument can be passed the dummy argument 'query' for systems that dont support sending osc messages without arguments.


* Denotes this is sent automatically from Live upon change  
[int arg] Optional argument


Installation
------------
* Checkout the master branch
* Rename LiveOSC2-master to LiveOSC2
* Move the folder to /Applications/Live xxxx/Contents/App-Resources/MIDI Remote Scripts


Song
----

create midi, audio, return
create scene

duplicate scene
duplicate track

/live/selection (int track_id, int scene_id, int width, int height)  
    Set the position of the "red ring" in Live


Transport
---------
/live/tempo (float tempo)  
    Sets the tempo, no argument returns tempo

/live/time  
    Returns the current song time

groove

cue points
set / delete cue

/live/cue/next  
/live/cue/prev  
    Jumps to the next and previous cue points in arrangement view
    
/live/play  
    Starts playing  
/live/play/continue  
    Restarts playing from the current point  
/live/play/select  
    Starts playing the current selection in arrangement view  


/live/undo  
/live/redo  

/live/overdub  
/live/metronome  


/live/loop  
/live/signature  


Scenes
------
/live/scenes  
    Returns the number of scenes in the live set  
    
/live/scene/name (int scene_id, [string name])  
    Sets / gets the name for scene_id.  
    *** LiveOSC no longer returns all scene names when scene_id is ommitted, use scene/block instead ***  
/live/scene/name/block (int scene_id, int height)  
    Returns a block of scene names  

/live/scene/color (int scene_id, [int color])  
    Sets / gets the color for scene_id.  

/live/scene/state (int scene_id)  
    Returns the state for scene_id (1 = triggered, 0 = stopped)  

/live/scene/select (int scene_id)  
    Selects scene_id



Tracks
------
/live/tracks
    Returns the number of tracks and returns in the live set

/live/track/arm (int track_id, [int state])  
/live/return/arm (int track_id, [int state])  
/live/master/arm ([int state])  
    Sets / gets the arm state of track_id  

/live/track/mute (int track_id, [int state])  
/live/return/mute (int track_id, [int state])  
/live/master/mute ([int state])  
    Sets / gets the mute state of track_id  

/live/track/solo (int track_id, [int state])  
/live/return/solo (int track_id, [int state])  
/live/master/solo ([int state])  
    Sets / gets the solo state of track_id  


/live/track/volume (int track_id, [float volume])  
/live/return/volume (int track_id, [float volume])  
/live/master/volume ([float volume])  
    Sets / gets the mixer volume of track_id  

/live/track/panning (int track_id, [float panning])  
/live/return/panning (int track_id, [float panning])  
/live/master/panning ([float panning])  
    Sets / gets the mixer panning of track_id  

/live/track/send (int track_id, int send_id, [float value])  
/live/return/send (int track_id, int send_id, [float value])  
/live/master/send (int send_id, [float value])  
    Sets / gets the mixer send_id of track_id  


/live/track/select (int track_id)  
/live/return/select (int track_id)  
/live/master/select  
    Selects the track

/live/track/crossfader (int track_id, [int state])  
/live/return/crossfader (int track_id, [int state])  
    Sets / gets the crossfader assignment of track_id (0=None, 1=A, 2=B)  

/live/master/crossfader  
    Sets / gets the master crossfader position


/live/track/name (int track_id, [string name])  
/live/return/name (int track_id, [string name])  
    Sets / gets the name of track_id  

/live/track/color (int track_id, [int color])  
/live/return/color (int track_id, [int color])  
    Sets / gets the color of track_id  


/live/track/stop (int track_id, [int state])  
/live/track/state (int track_id, [int state])  


collapse

routing
sub routing

Devices
-------

/live/track/devices (int track_id, [int device_id])  
/live/return/devices (int track_id, [int device_id])  
/live/master/devices ([int device_id])  

/live/track/device/range  
/live/return/device/range  
/live/master/device/range  


/live/track/device/param  
/live/return/device/param  
/live/master/device/param  


/live/track/device/select  
/live/return/device/select  
/live/master/device/select  




Clips
-----

/live/clip/state (int track_id, int scene_id)

/live/clip/play (int track_id, int scene_id)

/live/clip/stop (int track_id, int scene_id)

/live/clip/view (int track_id, int scene_id)

/live/clip/name (int track_id, int scene_id)

/live/clip/name/block (int track_id, int scene_id, int width, int height)

/live/clip/color (int track_id, int scene_id)


/live/clip/looping (int track_id, int scene_id)  
/live/clip/loopstart (int track_id, int scene_id)  
/live/clip/loopend (int track_id, int scene_id)  
/live/clip/loopjump (int track_id, int scene_id)  
/live/clip/start (int track_id, int scene_id)  
/live/clip/end (int track_id, int scene_id)  
/live/clip/warping (int track_id, int scene_id)  
/live/clip/pitch (int track_id, int scene_id)  


/live/clip/create (int track_id, int scene_id)  
/live/clip/delete (int track_id, int scene_id)  

warping mode
gain




Browser
-------

