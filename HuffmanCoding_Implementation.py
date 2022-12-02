
import heapq
# This module provides an implementation of the heap queue algorithm, also known as the priority queue algorithm.
import os
# Module to interact with the underlying operating system.

# A Huffman Tree Node


class TheTree:
    def __init__(self, symbol, freq):
        # symbol name (character)
        self.symbol = symbol
        # frequency of symbol
        self.freq = freq
        # node left of current node
        self.left = None
        # node right of current node
        self.right = None

    # Make the comparison
    def __lt__(self, nxt):
        return self.freq < nxt.freq

    # Make the comparison
    def __eq__(self, nxt):
        return self.freq == nxt.freq


class Huffmancode:

    def __init__(self, path):
        # file path
        self.path = path
        # store heap
        self.heap_data = []
        # store char and code
        self.huffman_code = {}
        # store decoded info
        self.reverse_code = {}

    # To count the number of each character
    def text_frequency(self, text):
        frequ_dict = {}
        # This iteration is to check if char is in dict adding freq+1 if not = 0
        for char in text:
            if char not in frequ_dict:
                frequ_dict[char] = 0
            frequ_dict[char] += 1
        return frequ_dict

    # prepare information for building the three
    def pre_heap(self, freqs_sorted):
        for key in freqs_sorted:
            frequency = freqs_sorted[key]
            tree_node = TheTree(key, frequency)
            heapq.heappush(self.heap_data, tree_node)

    # making the tree
    def make_the_tree(self):
        while len(self.heap_data) > 1:
            # Find node 1,2 and make newnode with combination
            tree_node1 = heapq.heappop(self.heap_data)
            tree_node2 = heapq.heappop(self.heap_data)
            sum_of_freq = tree_node1.freq + tree_node2.freq
            newnode = TheTree(None, sum_of_freq)
            newnode.left = tree_node1
            newnode.right = tree_node2
            heapq.heappush(self.heap_data, newnode)
        return

    # find the string and return the code
    def pre_get_code(self, root, code):
        if root is None:
            return
        if root.symbol is not None:
            # make huffman code dict
            self.huffman_code[root.symbol] = code
            # make reverse huffman code dict
            self.reverse_code[code] = root.symbol
            return
        # left child add bit 0 right child add bit 1
        self.pre_get_code(root.left, code+'0')
        self.pre_get_code(root.right, code+'1')

    def get_code(self):
        root = heapq.heappop(self.heap_data)
        self.pre_get_code(root, '')

    # replace characters with the code
    def make_encoded_text(self, text):
        # store encoded text
        encoded_text = ''
        for char in text:
            encoded_text += self.huffman_code[char]

        return encoded_text

    # adding 0 bit to the last part of text to make last group equal to 8 bits
    def padded_text(self, encoded_text):
        # finding how many 0 bit to add
        padding_symbol = 8 - (len(encoded_text) % 8)
        # adding 0 bit equal to padding symbol
        for i in range(padding_symbol):
            encoded_text += '0'

        # 08 mean 8 bit format
        # b mean binary format
        # 0 mean part 0
        padded_info = "{0:08b}".format(padding_symbol)
        padded_encoded_text = padded_info + encoded_text
        return padded_encoded_text

    def make_byte_array(self, padded_text):
        array = []
        for i in range(0, len(padded_text), 8):
            # slicing by 8
            byte = padded_text[i:i+8]
            # store each slicing 8 bits value
            array.append(int(byte, 2))
        return array

    def compression(self):

        # To access the file
        filename, file_extension = os.path.splitext(self.path)
        # output with .bin
        output_path = filename + '.bin'
        # r mean read
        # wb mean write with binary
        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            # read text from file
            text = file.read()
            # remove the space
            text = text.rstrip()
            # Calculate frequency of each text
            freqs_sorted = self.text_frequency(text)
            # Create Min heap
            build_heap = self.pre_heap(freqs_sorted)
            # Make the tree
            self.make_the_tree()
            # Make the code
            self.get_code()
            # Make the coded text
            encoded_text = self.make_encoded_text(text)
            # Make padding
            padded_text = self.padded_text(encoded_text)
            # Make 8 bits array to make bytes info
            bytes_array = self.make_byte_array(padded_text)
            # output file with bytes format
            final_bytes = bytes(bytes_array)
            output.write(final_bytes)
        print("Finish compressed")
        return output_path

    def remove_padding(self, text):
        # find padding info with first 8 bits
        padded_info = text[:8]
        # converted 8 bits to int to find how many 0 bit adding in the last part
        extra_padding = int(padded_info, 2)
        # remove first 8 bits
        text = text[8:]
        # remove 0 bits padding in the last part
        padding_removed_text = text[:-1*extra_padding]
        return padding_removed_text

    def decompressed_text(self, text):
        # stored decoded text
        decoded_text = ''
        # store bit to check if it is in reverse huffman dict or not
        current_bits = ''
        for bit in text:
            current_bits += bit
            if current_bits in self.reverse_code:
                character = self.reverse_code[current_bits]
                decoded_text += character
                current_bits = ""
        return decoded_text

    def decompression(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + '_decompressed' + '.txt'
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            # store bit string
            bit_string = ''
            # read the byte 1 by 1
            byte = file.read(1)
            while byte:
                # converted to integer
                byte = ord(byte)
                # converted to binary remove first 2 letters and make 8 bits
                bits = bin(byte)[2:].rjust(8, '0')
                # create bit string
                bit_string += bits
                byte = file.read(1)

            actual_text = self.remove_padding(bit_string)
            decompressed_text = self.decompressed_text(actual_text)
            output.write(decompressed_text)
        print("Finish decompressed")
        return


path = input("Please enter the path... ")
huffman_exe = Huffmancode(path)
output_path = huffman_exe.compression()
huffman_exe.decompression(output_path)
