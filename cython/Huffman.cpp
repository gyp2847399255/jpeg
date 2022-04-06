// ConsoleApplication2.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include "Huffman.h"

namespace compress {

    Huffman::Huffman() {}

    Huffman::Huffman(char* img_code_name, char* img_huff_name,
        char* compress_file_name, char* decompress_file_name)
    {

        this->img_code_name = img_code_name;
        this->img_huff_name = img_huff_name;
        this->compress_file_name = compress_file_name;
        this->decompress_file_name = decompress_file_name;
    }

    Huffman::~Huffman() {}

    // 从python输入文件读取int数组
    void Huffman::readRawData() {
        std::ifstream img_code;
        img_code.open(img_code_name);
        //std::cout << "Huffman::r  eadRawData" << std::endl;
        std::string number;
        //std::cout << "read number" << std::endl;
        while (img_code >> number) {
            raw_numbers.push_back(number);
            if (num2freq.count(number) == 0)
                num2freq[number] = 1;
            else
                num2freq[number] ++;
        }
        raw_numbers.push_back("EOF");
        num2freq["EOF"] = 1;
        nodes = num2freq.size();
        totalnodes = 2 * nodes - 1;
        //std::cout << "read number size " << raw_numbers.size() << std::endl;
        img_code.close();
    }

    void Huffman::occurrence() {
        for (int i = 0; i < raw_numbers.size(); i++)
        {
            if (num2freq.count(raw_numbers[i]) == 0)
                num2freq[raw_numbers[i]] = 1;
            else
                num2freq[raw_numbers[i]] ++;
        }

        nodes = num2freq.size();
        totalnodes = 2 * nodes - 1;

        float p = 1.0, ptemp;
        std::map<std::string, int>::iterator it;
        for (it = num2freq.begin(); it != num2freq.end(); it++)
        {
            ptemp = (it->second / (float)(raw_numbers.size()));
            if (ptemp > 0 && ptemp <= p)
                p = ptemp;
        }
    }


    void Huffman::preOrder(TREE_NODE* node)
    {
        if (node == nullptr) return;
        if (node->left != nullptr) {
            node->left->code = node->code + "0";
            preOrder(node->left);
        }
        if (node->right != nullptr) {
            node->right->code = node->code + "1";
            preOrder(node->right);
        }
        if (node->left == nullptr && node->right == nullptr) {
            num2code[node->number] = node->code;
        }
    }


    void Huffman::createTree()
    {
        //最小堆初始化
        for (auto it = num2freq.begin(); it != num2freq.end(); it++) {
            TREE_NODE* new_node = new TREE_NODE();
            new_node->number = it->first;
            new_node->freq = it->second;
            minHeap.push(new_node);
        }

        //创建霍夫曼树
        while (minHeap.size() != 1) {
            TREE_NODE* node1 = minHeap.top();
            minHeap.pop();
            TREE_NODE* node2 = minHeap.top();
            minHeap.pop();
            TREE_NODE* new_node = new TREE_NODE();
            new_node->freq = node1->freq + node2->freq;
            new_node->left = node1;
            new_node->right = node2;
            minHeap.push(new_node);
        }
    }

    void Huffman::saveNode(TREE_NODE* node, std::ofstream* tree_file)
    {
        bool isleaf = 0;
        if (node->left == nullptr && node->right == nullptr)
        {
            isleaf = 1;
            int n = 0;
            bool isend = 0;
            (*tree_file).write((char*)&isleaf, sizeof(isleaf));
            if (node->number == "EOF") isend = 1;
            else {
                std::stringstream ss;
                ss << node->number;
                ss >> n;
            }
            (*tree_file).write((char*)&isend, sizeof(isend));
            (*tree_file).write((char*)&n, sizeof(n));
        }
        else
        {
            (*tree_file).write((char*)&isleaf, sizeof(isleaf));
            saveNode(node->left, tree_file);
            saveNode(node->right, tree_file);
        }
    }

    void Huffman::readNode(TREE_NODE* node, std::ifstream* tree_file)
    {
        if (node == nullptr) {
            node = new TREE_NODE();
            minHeap.push(node);
        }
        bool isleaf;
        (*tree_file).read((char*)&isleaf, sizeof(isleaf));
        //std::cout << "isleaf " << isleaf << std::endl;
        if (isleaf == 1)
        {
            int n = 0;
            bool isend = 0;
            (*tree_file).read((char*)&isend, sizeof(isend));
            (*tree_file).read((char*)&n, sizeof(n));
            //std::cout << "isend " << isend << std::endl;
            //std::cout << "n " << n << std::endl;
            if (isend) node->number = "EOF";
            else {
                std::stringstream ss;
                ss << n;
                ss >> node->number;
            }
        }
        else
        {
            TREE_NODE* left = new TREE_NODE();
            TREE_NODE* right = new TREE_NODE();
            node->left = left;
            node->right = right;
            readNode(left, tree_file);
            readNode(right, tree_file);
        }
    }

    void Huffman::saveTree(char* num2freq_file_name, char* tree_file_name)
    {
        std::ofstream num2freq_file;
        num2freq_file.open(num2freq_file_name, std::ios::binary | std::ios::out);
        std::ofstream tree_file;
        tree_file.open(tree_file_name, std::ios::binary | std::ios::out);

        for (auto it = num2freq.begin(); it != num2freq.end(); it++)
        {
            num2freq_file.write((char*)(&(it->first)), sizeof(it->first));
            num2freq_file.write((char*)(&(it->second)), sizeof(it->second));
        }

        saveNode(minHeap.top(), &tree_file);

        num2freq_file.close();
        tree_file.close();
    }

    void Huffman::encode2(char* img_code_name, char* img_huff_name)
    {
        this->img_code_name = img_code_name;
        this->img_huff_name = img_huff_name;
        this->encode1();
    }


    // 通过霍夫曼编码压缩
    void Huffman::encode1() {
        std::cout << "Huffman Encode" << std::endl;
        std::ofstream img_huff;
        img_huff.open(img_huff_name, std::ios::binary | std::ios::out);

        //统计出现的字符串频率
        readRawData();

        //创建霍夫曼树
        createTree();

        //前序遍历霍夫曼树建立映射
        preOrder(minHeap.top());

        //编码输入数字为二进制
        std::stringstream ss;
        for (int i = 0; i < raw_numbers.size(); i++)
            ss << num2code[raw_numbers[i]];
        std::string s = "";
        ss >> s;
        while (s.length() > 0) {
            std::stringstream ss_temp;
            std::string s_temp = s.substr(0, 8);
            while (s_temp.length() < 8) s_temp += '0';
            ss_temp << s_temp;
            unsigned int n_2;
            unsigned int mult = 1;
            uint8_t n_10 = 0;
            ss_temp >> n_2;
            while (n_2 > 0) {
                n_10 += (n_2 % 10) * mult;
                n_2 = (int)n_2 / 10;
                mult *= 2;
            }
            //int ttt = n_10;
            //std::cout << s_temp << std::endl;
            //std::cout << ttt << std::endl;
            img_huff.write((char*)&n_10, sizeof(n_10));
            if (s.length() > 8)
                s = s.substr(8);
            else
                s = "";
        }

        img_huff.close();
    }


    void Huffman::decodeWithTree(std::string s_2)
    {
        std::ofstream decompress_file;
        decompress_file.open(decompress_file_name);

        int i = 0;
        TREE_NODE* t = minHeap.top();
        while (i < s_2.size()) {
            if (s_2[i] == '0' && t->left != nullptr) {
                t = t->left;
                i++;
                if (t->left == nullptr && t->right == nullptr) {
                    if (t->number == "EOF") break;
                    decompress_file << t->number << std::endl;
                    t = minHeap.top();
                }
            }
            else if (s_2[i] == '1' && t->right != nullptr) {
                t = t->right;
                i++;
                if (t->left == nullptr && t->right == nullptr) {
                    if (t->number == "EOF") break;
                    decompress_file << t->number << std::endl;
                    t = minHeap.top();
                }
            }
            else {
                std::cout << "Huffman Decode Error" << std::endl;
                break;
            }
        }
        decompress_file.close();
    }


    std::string Huffman::readBinaryData()
    {
        std::ifstream compress_file;
        compress_file.open(compress_file_name, std::ios::binary | std::ios::in);
        //获取二进制编码
        std::string s_2 = "";
        uint8_t t_10;
        while (compress_file.read((char*)&t_10, sizeof(char))) {
            unsigned int t_2 = 0;
            unsigned int mult = 1;
            while (t_10 != 0) {
                t_2 += (t_10 % 2) * mult;
                t_10 /= 2;
                mult *= 10;
            }
            char c[10];
            sprintf(c, "%08d", t_2);
            //std::cout << c << std::endl;
            s_2 += c;
        }
        compress_file.close();
        return s_2;
    }


    void Huffman::decode2(char* compress_file_name, char* decompress_file_name)
    {
        this->compress_file_name = compress_file_name;
        this->decompress_file_name = decompress_file_name;
        decode1();
    }

    void Huffman::decode1()
    {
        std::cout << "Huffman Decode by encode tree" << std::endl;
        //获取二进制编码
        std::string s_2 = readBinaryData();
        //直接根据霍夫曼树解码
        decodeWithTree(s_2);
    }

    void Huffman::decode4(int type, char* tree_file_name, char* compress_file_name, char* decompress_file_name)
    {
        this->compress_file_name = compress_file_name;
        this->decompress_file_name = decompress_file_name;
        decode3(type, tree_file_name);
    }

    void Huffman::decode3(int type, char* tree_file_name)
    {

        //获取二进制编码
        std::string s_2 = readBinaryData();

        //重建霍夫曼树
        std::ifstream tree_file;
        tree_file.open(tree_file_name, std::ios::binary | std::ios::in);

        if (type == 0) {
            std::cout << "Huffman Decode by numToFreq file" << std::endl;
            num2freq.clear();
            while (!minHeap.empty()) minHeap.pop();
            std::string number;
            int frequency;
            while (tree_file.read((char*)&number, sizeof(number))) {
                tree_file.read((char*)&frequency, sizeof(frequency));
                num2freq[number] = frequency;
            }
            createTree();
        }

        //从文件中读取霍夫曼树
        else {
            std::cout << "Huffman Decode by tree file" << std::endl;
            while (!minHeap.empty()) minHeap.pop();
            readNode(nullptr, &tree_file);
        }

        //根据霍夫曼树解码
        decodeWithTree(s_2);
    }
}




int main()
{
    using namespace compress;
    char s1[] = "encode.txt\0";
    char s2[] = "huffman.bin\0";
    char s3[] = "huffman.bin\0";
    char s4[] = "dehuffman.txt\0";

    char s5[] = "num2freq.bin\0";
    char s6[] = "tree.bin\0";

    Huffman* huffman = new Huffman(s1, s2, s3, s4);
    huffman->encode1();
    huffman->saveTree(s5, s6);
    huffman->decode3(0, s5);
}
