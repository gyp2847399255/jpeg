cdef extern from "Huffman.cpp":
    pass

# Declare the class with cdef
cdef extern from "Huffman.h" namespace "compress":
    cdef cppclass Huffman:
        Huffman() except +
        Huffman(char*, char*, char*, char*) except +
        void saveTree(char*, char*)
        void encode1()
        void encode2(char*, char*)
        void decode1()
        void decode2(char*, char*)
        void decode3(int, char*)
        void decode4(int, char*, char*, char*)
