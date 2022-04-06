#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import time
from helper import helper
import rect
from rect import PyHuffman

if __name__ == '__main__':

    addr = "images/image.bmp"
    helper = helper(addr, "encode.txt", "dehuffman.txt", "images/out.bmp")
    time0 = time.time()
    helper.encode_from_img()
    print("DCT encode time", time.time() - time0)

    ''' cython start '''
    # help (rect)
    # help (PyHuffman)
    print("cython start")
    name1 = bytes("encode.txt", encoding='utf8')
    name2 = bytes("huffman.bin", encoding='utf8')
    name3 = bytes("huffman.bin", encoding='utf8')
    name4 = bytes("dehuffman.txt", encoding='utf8')
    name5 = bytes("num2freq.bin", encoding='utf8')
    name6 = bytes("tree.bin", encoding='utf8')
    #huffman = huffman.initName(name1, name2, name3, name4)
    huffman = PyHuffman()

    time0 = time.time()
    #huffman.encode1()
    huffman.encode2(name1, name2)
    print("Huffman encode time", time.time() - time0)

    huffman.saveTree(name5, name6)

    time0 = time.time()
    #huffman.decode1()
    huffman.decode2(name3, name4)
    print("Huffman decode time", time.time() - time0)

    time0 = time.time()
    huffman.decode4(0, name5, name3, name4)
    print("Huffman decode time", time.time() - time0)

    time0 = time.time()
    huffman.decode4(1, name6, name3, name4)
    print("Huffman decode time", time.time() - time0)
    ''' cython end '''

    time0 = time.time()
    helper.decode_to_img()
    print("DCT decode time", time.time() - time0)

