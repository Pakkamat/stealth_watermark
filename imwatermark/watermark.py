import struct
import uuid
import copy
import base64
import cv2
import numpy as np
from .maxDct import EmbedMaxDct
import pprint

pp = pprint.PrettyPrinter(indent=2)

class WatermarkEncoder(object):
    def __init__(self, content=b''):
        seq = np.array([n for n in content], dtype=np.uint8)
        self._watermarks = list(np.unpackbits(seq))
        self._wmLen = len(self._watermarks)
        self._wmType = 'bytes'

    def set_by_bytes(self, content):
        self._wmType = 'bytes'
        seq = np.array([n for n in content], dtype=np.uint8)
        self._watermarks = list(np.unpackbits(seq))
        self._wmLen = len(self._watermarks)


    def set_watermark(self, wmType='bytes', content=''):
        if wmType == 'bytes':
            self.set_by_bytes(content)
        else:
            raise NameError('%s is not supported' % wmType)

    def get_length(self):
        return self._wmLen

    def encode(self, cv2Image, method='dwtDct', **configs):
        (r, c, channels) = cv2Image.shape
        if r*c < 256*256:
            raise RuntimeError('image too small, should be larger than 256x256')

        if method == 'dwtDct':
            embed = EmbedMaxDct(self._watermarks, wmLen=self._wmLen, **configs)
            return embed.encode(cv2Image)
        else:
            raise NameError('%s is not supported' % method)

class WatermarkDecoder(object):
    def __init__(self, wm_type='bytes', length=0):
        self._wmType = wm_type
        if wm_type == 'bytes':
            self._wmLen = length
        else:
            raise NameError('%s is unsupported' % wm_type)


    def reconstruct_bytes(self, bits):
        nums = np.packbits(bits)
        bstr = b''
        for i in range(self._wmLen//8):
            bstr += struct.pack('>B', nums[i])
        return bstr

    def reconstruct(self, bits):
        if len(bits) != self._wmLen:
            raise RuntimeError('bits are not matched with watermark length')

        if self._wmType == 'bytes':
            return self.reconstruct_bytes(bits)

    def decode(self, cv2Image, method='dwtDct', **configs):
        (r, c, channels) = cv2Image.shape
        if r*c < 256*256:
            raise RuntimeError('image too small, should be larger than 256x256')

        bits = []
        if method == 'dwtDct':
            embed = EmbedMaxDct(watermarks=[], wmLen=self._wmLen, **configs)
            bits = embed.decode(cv2Image)
        else:
            raise NameError('%s is not supported' % method)
        return self.reconstruct(bits)
