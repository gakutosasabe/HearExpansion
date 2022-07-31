import webrtcvad
import numpy as np
from mic_array import MicArray
from pixel_ring import pixel_ring

RATE = 16000
CHANNELS = 4
VAD_FRAMES = 10     # ms
DOA_FRAMES = 200    # ms

def get_direction():
    sound_direction = None
    vad = webrtcvad.Vad(3)

    speech_count = 0
    chunks = []
    doa_chunks = int(DOA_FRAMES / VAD_FRAMES)

    with MicArray(RATE, CHANNELS, RATE * VAD_FRAMES / 1000)  as mic:
        for chunk in mic.read_chunks():
            # Use single channel audio to detect voice activity
            if vad.is_speech(chunk[0::CHANNELS].tobytes(), RATE):
                speech_count += 1

            chunks.append(chunk)
            if len(chunks) == doa_chunks:
                if speech_count > (doa_chunks / 2):
                    frames = np.concatenate(chunks)
                    direction = mic.get_direction(frames)
                    pixel_ring.set_direction(direction)
                    print('\n{}'.format(int(direction)))
                sound_direction = int(direction)
                speech_count = 0
                chunks = []
                    
    pixel_ring.off()
    return sound_direction