#!/usr/bin/env python3

'''
# done|not_tested # raspivid -t 0 -b 1200000 -w 1280 -h 720 -fps 60 -o - | 
# done|not_tested # gst-launch-1.0 fdsrc ! 
# done|not_tested # ----h264parse ! 
# done|not_tested # --------rtph264pay config-interval=1 pt=96 ! 
# done|not_tested # ------------udpsink host=192.168.168.146 port=5200
'''

import sys, os, subprocess
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
    
    # Expirimental part:
    #======================================================================

    #creating a pipe to raspivid,
    # r_fd and w_fd closed at the end of function main
    read_fd, write_fd = os.pipe()
    
    command = 'raspivid -t 0 -b 1200000 -w 1280 -h 720 -fps 60 -o - '
    subprocess.run(command,check=True,stdout=write_fd)
    
    #======================================================================    
    fdsrc = Gst.ElementFactory.make('fdsrc')
    if not fdsrc:
        sys.stdout.write('"fdsrc" crashed')
        sys.exit(1)
    fdsrc.set_property('fd',read_fd)

    fdsrc.set_property()
    h264parse = Gst.ElementFactory.make('h264parse')
    if not h264parse:
        sys.stdout.write('"h264parse" crashed')
        sys.exit(1)

    rtph264pay = Gst.ElementFactory.make('rtph264pay')
    if not rtph264pay:
        sys.stdout.write('"rtph264pay" crashed')
        sys.exit(1)
    rtph264pay.set_property('config-interval',1)
    rtph264pay.set_property('pt',96)

    udpsink = Gst.ElementFactory.make('udpsink')
    if not udpsink:
        sys.stdout.write('"udpsink" crashed')
        sys.exit(1)
    udpsink.set_property('host','192.168.168.146')
    udpsink.set_property('port',5200)

    # Creating pipeline
    pipeline = Gst.Pipeline.new('dynamic')

    pipeline.add(fdsrc)
    pipeline.add(h264parse)
    pipeline.add(rtph264pay)
    pipeline.add(udpsink)

    # Linking
    fdsrc.link(h264parse)
    h264parse.link(rtph264pay)
    rtph264pay.link(udpsink)

    # pdata = ProbeData(pipeline, src)

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
    os.close(write_fd)
    os.close(read_fd)


if __name__ == '__main__':
    sys.exit(main(sys.argv))