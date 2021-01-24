#!/usr/bin/env python

""" Tool to convert audiobooks into easy digestable mp3s for my mp3 player.

    sudo apt install ffmpeg mp3splt
"""
import glob
import optparse
import os
import subprocess


if __name__ == '__main__':

    parser = optparse.OptionParser('%prog [options] file1.mp3 [file2.mp3 ...]')

    parser.add_option('-o',
                      '--output',
                      dest='prefix',
                      action='store',
                      type='string',
                      default='output',
                      help='output prefix [output]')

    parser.add_option('-t',
                      '--time',
                      dest='time',
                      action='store',
                      type='string',
                      default='25.00',
                      help='time segment [mm.ss], [25.00]')

    parser.add_option('-k',
                      '--keep',
                      dest='keep',
                      action='store_true',
                      default=False,
                      help='keep work-in-progress files')

    options, args = parser.parse_args()

    prefix = options.prefix
    time = options.time
    keep = options.keep

    # Copy input .mp3 files.
    for idx, filename in enumerate(args, 1):
        command = f'cp "{filename}" "{prefix}_{idx:02d}.mp3"'
        try:
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError:
            pass

    # Split .mp3s
    inputs = glob.glob(f'{prefix}_??.mp3')
    for input in inputs:
        command = f'mp3splt -t "{time}" -a -d "{prefix}" -o "@f_@n" "{input}"'
        subprocess.check_call(command, shell=True)

        if not keep:
            os.remove(input)

