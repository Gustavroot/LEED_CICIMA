#!/usr/bin/env python

import datetime
import os
import re
import subprocess
import sys

#Most part of this script was taken from a Nils Maier work written in 2013,
#and more about associated copyright http://creativecommons.org/publicdomain/zero/1.0/
def which(program):
    def is_executable(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    if is_executable(program):
        return program
    path, program = os.path.split(program)
    if path:
        return None
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        exe = os.path.join(path, program)
        if is_executable(exe):
            return exe
        exe = os.path.join(path, "{}.exe".format(program))
        if is_executable(exe):
            return exe
    return None

def thumb_with_ffmpeg(infile, position=0.5, executable=None):

    ffmpeg = which(executable or "ffmpeg")
    if not ffmpeg:
        raise RuntimeError(
            "Failed to find ffmpeg executable: {}".format(executable))
    if position < 0 or position >= 1.0:
        raise ValueError(
            "Position {} is not between 0.0 and 1.0".format(position))
    proc = subprocess.Popen([ffmpeg, "-i", infile], stderr=subprocess.PIPE)
    _, result = proc.communicate()
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+)\.(\d+)", result)
    if not m:
        raise KeyError("Cannot determine duration")
    #Avoiding strptime here because it has some issues handling milliseconds.
    m = [int(m.group(i)) for i in range(1, 5)]
    duration = datetime.timedelta(hours=m[0],
                                  minutes=m[1],
                                  seconds=m[2],
                                  # * 10 because truncated to 2 decimal places
                                  milliseconds=m[3] * 10
                                  ).total_seconds()
    target = max(0, min(duration * position, duration - 0.1))
    target = "{:.3f}".format(target)
    args = [ffmpeg,
            "-ss", target,
            "-i", infile,
            "-map", "v:0",     # first video stream
            "-frames:v", "1",  # 1 frame
            "-f", "mjpeg",     # motion jpeg (aka. jpeg since 1 frame) output
            "pipe:"            # pipe output to stdout
            ]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    output, _ = proc.communicate()
    if proc.returncode:
        raise subprocess.CalledProcessError(proc.returncode, args)
    if not output:
        raise subprocess.CalledProcessError(-2, args)
    return output

if __name__ == "__main__":
    from argparse import ArgumentParser, ArgumentTypeError
    def percentage(x):
        x = float(x)
        if x < 0.0 or x >= 1.0:
            raise ArgumentTypeError(
                "{} not in percentage range [0.0, 1.0)".format(x))
        return x
    parser = ArgumentParser(
        description="Extract a thumbnail from a media file using ffmpeg")
    parser.add_argument("infile", type=str, help="Input file")
    parser.add_argument("outfile", type=str, help="Output file")
    parser.add_argument("-f", "--ffmpeg", type=str, default=None,
                        help="use this ffmpeg binary, "
                             "default: check $PATH for ffmpeg")
    parser.add_argument("-p", "--position", type=percentage, default=0.5,
                        help="thumbnail at this position (percentage), "
                             "default: 0.5")
    args = parser.parse_args()
    try:
        output = thumb_with_ffmpeg(args.infile, args.position, args.ffmpeg)
        with open(args.outfile, "wb") as op:
            op.write(output)
    except Exception as ex:
        print >>sys.stderr, "Error:", ex
        sys.exit(ex.returncode or 1)
