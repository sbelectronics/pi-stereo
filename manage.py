#!/usr/bin/env python
import os
import sys
import stereocontroller

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stereo.settings")

    from django.core.management import execute_from_command_line

    print "starting up stereo"
    args = list(sys.argv)
    if ("--nohardware" in args):
        args.remove("--nohardware")
        stereocontroller.startup(noHardware=True)
    else:
        if ("runserver" in args) and ("--noreload" not in args):
            print >> sys.stderr, "please use --noreload after runserver"
            sys.exit(-1)
        stereocontroller.startup(noHardware=False)
    print "finished starting up stereo"

    execute_from_command_line(args)
