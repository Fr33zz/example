#!/usr/bin/env python3

''' 
# +     # gst-launch-1.0 udpsrc port=5200 !
#  how? # ---application/x-rtp, encoding-name=H264,payload=96 ! 
# +     # -------rtph264depay ! 
# +     # ----------h264parse !
# +     # -------------avdec_h264 !
# +     # ----------------videoconvert  !
# +     # -------------------autovideosink sync=false

'''

import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst


# message handler
def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error %s: %s\n" %(err, debug))
        loop.quit()
    return True

def main(args):
    GObject.threads_init()
    Gst.init(None)

    # Creating elements
    udpsrc = Gst.ElementFactory.make('udpsrc')
    if not udpsrc:
        sys.stdout.write('"udpsrc" crashed')
        sys.exit(1)
    udpsrc.set_property('port',5200)

    app_xrtp = Gst.ElementFactory.make('application/x-rtp')
    if not app_xrtp:
        sys.stdout.write('"application/x-rtp" crashed')
        sys.exit(1)
    app_xrtp.set_property('encoding-name', 'H264')
    app_xrtp.set_property('payload', 96)

    rtph264depay = Gst.ElementFactory.make('rtph264depay')
    if not rtph264depay:
        sys.stdout.write('"rtph264depay" crashed')
        sys.exit(1)

    h264parse = Gst.ElementFactory.make('h264parse')
    if not h264parse:
        sys.stdout.write('"h264parse" crashed')
        sys.exit(1)

    avdec_h264 = Gst.ElementFactory.make('avdec_h264')
    if not avdec_h264:
        sys.stdout.write('"avdec_h264" crashed')
        sys.exit(1)

    videoconvert = Gst.ElementFactory.make('videoconvert')
    if not videoconvert:
        sys.stdout.write('"videoconvert" crashed')
        sys.exit(1)

    autovideosink = Gst.ElementFactory.make('autovideosink')
    if not autovideosink:
        sys.stdout.write('"autovideosink" crashed')
        sys.exit(1)
    autovideosink.set_property('sync','false')

    # Creating pipeline
    pipeline = Gst.Pipeline.new('dynamic')

    pipeline.add(udpsrc)
    pipeline.add(app_xrtp)
    pipeline.add(rtph264depay)
    pipeline.add(h264parse)
    pipeline.add(avdec_h264)
    pipeline.add(videoconvert)
    pipeline.add(autovideosink)


    # Linking
    udpsrc.link(app_xrtp)
    app_xrtp.link(rtph264depay)
    rtph264depay.link(h264parse)
    h264parse.link(avdec_h264)
    avdec_h264.link(videoconvert)
    videoconvert.link(autovideosink)

    # pdata = ProbeData(pipe, src)

    loop = GObject.MainLoop()

    # GLib.timeout_add_seconds(1, timeout_cb, pdata)

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)
    
    # start play back and listen to events
    pipeline.set_state(Gst.State.PLAYING)
    try:
      loop.run()
    except:
      pass
    
    # cleanup
    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    sys.exit(main(sys.argv))