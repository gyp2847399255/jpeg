#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <bitset>
#include <vector>
#include <queue>
#include <map>

#ifndef HUFFMAN_H
#define HUFFMAN_H

namespace compress {

    typedef struct tree_node
    {
        std::string number = "";
        std::string code = "";
        unsigned int freq = 0;
        struct tree_node* left = nullptr;
        struct tree_node* right = nullptr;
        tree_node() {
            number = "";
            code = "";
            freq = 0;
            left = nullptr;
            right = nullptr;
        }
    }TREE_NODE;

    struct compareByFreq {
        bool operator()(const TREE_NODE* a, const TREE_NODE* b) { return (a->freq > b->freq); }
    };

    class Huffman {
    private:
        int nodes = 0;
        int totalnodes = 0;
        char* img_code_name;
        char* img_huff_name;
        char* compress_file_name;
        char* decompress_file_name;

        void readRawData();
        void occurrence();
        void createTree();
        std::string readBinaryData();
        void preOrder(TREE_NODE* node);
        void decodeWithTree(std::string s_2);
        void saveNode(TREE_NODE* node, std::ofstream* tree_file);
        void readNode(TREE_NODE* node, std::ifstream* tree_file);

    public:
        std::vector<std::string> raw_numbers;
        std::map<std::string, int> num2freq;
        std::map<std::string, std::string> num2code;
        std::priority_queue<TREE_NODE*, std::vector<TREE_NODE*>, compareByFreq> minHeap;

        Huffman();
        Huffman(char* img_code_name, char* img_huff_name,
            char* compress_file_name, char* decompress_file_name);
        ~Huffman();
        void saveTree(char* num2freq_file_name, char* tree_file_name);
        void encode1();
        void encode2(char* img_code_name, char* img_huff_name);
        void decode1();
        void decode2(char* compress_file_name, char* decompress_file_name);
        void decode3(int type, char* tree_file_name);
        void decode4(int type, char* tree_file_name, char* compress_file_name, char* decompress_file_name);
    };

}

#endif