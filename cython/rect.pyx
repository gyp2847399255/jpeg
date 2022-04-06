# distutils: language = c++

from Huffman cimport Huffman
from libc.stdio cimport printf


cdef class PyHuffman:
    cdef Huffman*c_rect  # hold a pointer to the C++ instance which we're wrapping

    def __cinit__(self):
        self.c_rect = new Huffman()

    def initName(self, bytes py_name1, bytes py_name2, 
                    bytes py_name3, bytes py_name4):
        cdef char* c_name1  =  py_name1
        cdef char* c_name2  =  py_name2
        cdef char* c_name3  =  py_name3
        cdef char* c_name4  =  py_name4
        self.c_rect = new Huffman(c_name1, c_name2, c_name3, c_name4)
	
    def encode1(self):
        self.c_rect.encode1()

    def encode2(self, bytes py_name1, bytes py_name2):
        cdef char* c_name1  =  py_name1
        cdef char* c_name2  =  py_name2
        self.c_rect.encode2(c_name1, c_name2)
    
    def saveTree(self, bytes py_name1, bytes py_name2):
        cdef char* c_name1  =  py_name1
        cdef char* c_name2  =  py_name2
        self.c_rect.saveTree(c_name1, c_name2)

    def decode1(self):
        self.c_rect.decode1()

    def decode2(self, bytes py_name1, bytes py_name2):
        cdef char* c_name1  =  py_name1
        cdef char* c_name2  =  py_name2
        self.c_rect.decode2(c_name1, c_name2)

    def decode3(self, int py_type, bytes py_name1):
        cdef int c_type = py_type
        cdef char* c_name1  =  py_name1
        self.c_rect.decode3(c_type, c_name1)

    def decode4(self, int py_type, bytes py_name1, bytes py_name2, bytes py_name3):
        cdef int c_type = py_type
        cdef char* c_name1  =  py_name1
        cdef char* c_name2  =  py_name2
        cdef char* c_name3  =  py_name3
        self.c_rect.decode4(c_type, c_name1, c_name2, c_name3)


    def __dealloc__(self):
        del self.c_rect


