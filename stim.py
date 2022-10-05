#!/usr/bin/python3
#########################################################################################
# GENERAL PURPOSE ICMS SCRIPT FOR INTAN CONTROLLER
# Thomas Makin
#
# MIT License
# Copyright (c) 2022, Thomas Makin All rights reserved.
#
# Intan TCP Sample Code
# Public Domain
# Copyright (c) 2022, Intan Technologies
#
#########################################################################################

import argparse, datetime, os, sys, time, socket
from dotenv import load_dotenv

# Read unsigned 32-bit int--Credit Intan RHX Example TCP Client
def readUint32(array, arrayIndex):
    variableBytes = array[arrayIndex : arrayIndex + 4]
    variable = int.from_bytes(variableBytes, byteorder='little', signed=False)
    arrayIndex = arrayIndex + 4
    return variable, arrayIndex

# Read signed 32-bit int--Credit Intan RHX Example TCP Client
def readInt32(array, arrayIndex):
    variableBytes = array[arrayIndex : arrayIndex + 4]
    variable = int.from_bytes(variableBytes, byteorder='little', signed=True)
    arrayIndex = arrayIndex + 4
    return variable, arrayIndex

# Read unsigned 16-bit int--Credit Intan RHX Example TCP Client
def readUint16(array, arrayIndex):
    variableBytes = array[arrayIndex : arrayIndex + 2]
    variable = int.from_bytes(variableBytes, byteorder='little', signed=False)
    arrayIndex = arrayIndex + 2
    return variable, arrayIndex

# TCP connection initialization--Credit Intan RHX Example TCP Client
def tcpInit(recording):
    # Query runmode from RHX software
    scommand.sendall(b'get runmode')
    commandReturn = str(scommand.recv(COMMAND_BUFFER_SIZE), "utf-8")
    isStopped = commandReturn == "Return: RunMode Stop"

    # If controller is running, stop it
    if not isStopped:
        scommand.sendall(b'set runmode stop')
        time.sleep(0.1) # Allow time for RHX software to accept this command before the
                        # next one comes

    if recording == True:
        # Send command to RHX software to set baseFileName
        scommand.sendall(b'set filename.basefilename recording-' + 
                         timestamp.encode('utf-8') + b'.rhs')
        time.sleep(0.1)

        # Send command to RHX software to set path
        scommand.sendall(b'set filename.path ' + RECORDING_PATH)
        time.sleep(0.1)

# Configure stimulation parameters--Credit Intan RHX Example TCP Client
def initStim():
    numPulse = str(STIM_FREQ * STIM_TOTAL).encode('utf-8')

    # Note all strings sent must be in UTF-8 byte encoding (b before strings, 
    # .encode(<string>, 'utf-8'), bytes(<thing>, 'utf-8'))
    scommand.sendall(b'set usefastsettle true')
    time.sleep(0.1)
    scommand.sendall(b'set ' + STIM_CHANNEL + b'.stimenabled true')
    time.sleep(0.1)
    scommand.sendall(b'set ' + STIM_CHANNEL + b'.source keypressf1')
    time.sleep(0.1)
    scommand.sendall(b'set ' + STIM_CHANNEL + b'.shape ' + STIM_TYPE)
    time.sleep(0.1)

    # Only apply interphase parameter if stim type actually uses an interphase
    if b"interphase" in STIM_TYPE:
        scommand.sendall(b'set ' + STIM_CHANNEL + b'.interphasedelaymicroseconds ' + 
                         STIM_INTERPHASE)
        time.sleep(0.1)

    scommand.sendall(b'set ' + STIM_CHANNEL + b'.pulseortrain PulseTrain')
    time.sleep(0.1)
    scommand.sendall(b'set ' + STIM_CHANNEL + b'.polarity ' + STIM_POLARITY)
    time.sleep(0.1)
    scommand.sendall(b'set ' + STIM_CHANNEL + b'.numberofstimpulses ' + numPulse)
    time.sleep(0.1)
    scommand.sendall(b'set ' + STIM_CHANNEL + b'.firstphaseamplitudemicroamps ' + 
                     STIM_CURRENT)
    time.sleep(0.1)
    scommand.sendall(b'set ' + STIM_CHANNEL + b'.firstphasedurationmicroseconds ' + 
                     STIM_DURATION)
    time.sleep(0.1)
    scommand.sendall(b'set ' + STIM_CHANNEL + b'.secondphaseamplitudemicroamps ' + 
                     STIM_CURRENT)
    time.sleep(0.1)
    scommand.sendall(b'set ' + STIM_CHANNEL + b'.secondphasedurationmicroseconds ' + 
                     STIM_DURATION)
    time.sleep(0.1)
    scommand.sendall(b'execute uploadstimparameters ' + STIM_CHANNEL)
    time.sleep(1)

    if args.record == True:
        # Send command to RHX software to begin recording
        scommand.sendall(b'set runmode record')    
    else:
        # Send command to RHX software to start without recording
        scommand.sendall(b'set runmode start')

# ENTRY
if __name__ == '__main__':
    # Parse timestamp
    timestamp = datetime.datetime.now().strftime("%m%d%y-%H%M")

    # Parse -r or --record to enable recording
    parser = argparse.ArgumentParser(
        description='General-purpose ICMS program for Intan boards')
    parser.add_argument('-r', '--record', action='store_true', 
                        help='Record neural data to file')
    parser.set_defaults(record=False)

    args = parser.parse_args()

    # Load env from file (.env)
    load_dotenv()

    # NOTE: This may not be the most efficient way of doing this :)

    # Grab TCP params
    COMMAND_BUFFER_SIZE = os.environ.get('COMMAND_BUFFER_SIZE')
    TCP_ADDRESS         = os.environ.get('TCP_ADDRESS')
    COMMAND_PORT        = os.environ.get('COMMAND_PORT')

    # Grab recording param
    RECORDING_PATH = str(os.environ.get('RECORDING_PATH')).encode('utf-8')

    # Grab stim params
    STIM_CHANNEL    = str(os.environ.get('STIM_CHANNEL')).encode('utf-8')
    STIM_CURRENT    = str(os.environ.get('STIM_CURRENT')).encode('utf-8')
    STIM_DURATION   = str(os.environ.get('STIM_DURATION')).encode('utf-8')
    STIM_INTERPHASE = str(os.environ.get('STIM_INTERPHASE')).encode('utf-8')
    STIM_POLARITY   = str(os.environ.get('STIM_POLARITY')).encode('utf-8')
    STIM_TOTAL      = int(os.environ.get('STIM_TOTAL')) # Parsed for doing math, not
                                                        # part of TCP command
    STIM_FREQ       = int(os.environ.get('STIM_FREQ'))  # ^
    STIM_TYPE       = str(os.environ.get('STIM_TYPE')).encode('utf-8')

    # Connect to TCP command server
    print('Connecting to TCP command server...')
    scommand = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scommand.connect((args.ip, COMMAND_PORT))

    # Handle keyboard interrupts gracefully
    try:
        # Init TCP connection
        tcpInit()
        initStim()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            scommand.sendall(b'set runmode stop') # Stop recording
            scommand.close()                      # Close TCP socket

            sys.exit(0)
        except SystemExit:
            os._exit(0)
