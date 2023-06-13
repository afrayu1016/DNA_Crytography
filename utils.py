from PIL import Image
import tkinter as tk
from tkinter import filedialog
import hashlib 
import binascii
import textwrap
import cv2
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from importlib import reload  
from bisect import bisect_left as bsearch
import os
import random
import re
import math
import binascii

# delimiters
# use smaller delimiters encoding for saving space (e.g. <key> -> <k>)
key_del = "<key>"
no_rounds_del = "<no_rounds>"
round_del = "<round>"
reshape_del = "<reshape>"
crossover_del = "<crossover>"
crossover_type_del = "<type>"
single_point_crossover_del = "<single_point>"
rotate_crossover_del = "<rotate>"
rotation_offset_del = "<rotation_offset>"
rotation_types_del = "<rotation_types>"
mutation_del = "<mutation>"
complement_mutation_del = "<complement_mutation>"
alter_mutation_del = "<alter_mutation>"
mutation_table_del = "<mutation_table>"
chromosome_del = "<chromosome>"

dna = {}
dna['00'] = 'A'
dna['01'] = 'C'
dna['10'] = 'G'
dna['11'] = 'T'

dna['A'] = '00'
dna['C'] = '01'
dna['G'] = '10'
dna['T'] = '11'

# generate encoding tables domains
two_bit_list = ['00', '01', '10', '11']
dna_bases = ['A', 'C', 'G', 'T']

four_bit_list = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100',
                 '1101', '1110', '1111']
two_dna_bases = ['TA', 'TC', 'TG', 'TT', 'GA', 'GC', 'GG', 'GT', 'CA', 'CC', 'CG', 'CT', 'AA', 'AC', 'AG', 'AT']

# encoding tables and their reversal
two_bits_to_dna_base_table = None
dna_base_to_two_bits_table = None

four_bits_to_two_dna_base_table = None
two_dna_base_to_four_bits_table = None

key_filename = "key.txt"
original_filename = "original.npz"
encrypted_filename = "encrypt.npz"
decrypted_filename = "decrypt.npz"

def get_filepath():
    t_type = ['jpg', 'jpeg', 'png']
    filepath = './img/'
#     print(filepath)
    all_file = os.listdir(filepath)
    
    for f in all_file:
        if f.split('.')[-1].lower() in t_type:
            return filepath + f

        
def decompose_matrix(iname):
    image = cv2.imread(iname)
    blue, green, red = split_into_rgb_channels(image)
    for values, channel in zip((red, green, blue), (2, 1, 0)):
        img = np.zeros((values.shape[0], values.shape[1]), dtype = np.uint8)
        img[:,:] = (values)
        if channel == 0:
            B = np.asmatrix(img)
        elif channel == 1:
            G = np.asmatrix(img)
        else:
            R = np.asmatrix(img)
    return B, G, R  


def split_into_rgb_channels(image):
    red = image[:,:,2]
    green = image[:,:,1]
    blue = image[:,:,0]
    return red, green, blue


def dna_encode(b, g, r):
    b = np.unpackbits(b, axis=1)
    g = np.unpackbits(g, axis=1)
    r = np.unpackbits(r, axis=1)
#     print(b)
#     print(b.shape)

    m, n = b.shape
    r_enc = np.chararray((m, int(n/2)))
    g_enc = np.chararray((m, int(n/2)))
    b_enc = np.chararray((m, int(n/2)))
#     print(b_enc.shape)
    
    for color, enc in zip((b, g, r), (b_enc, g_enc, r_enc)):
        idx = 0
        for j in range(0, m):
            for i in range(0, n, 2):
                enc[j, idx] = dna["{0}{1}".format(color[j, i], color[j, i + 1])]
                idx += 1
                if (i == n-2):
                    idx = 0
                    break

    b_enc = b_enc.astype(str)
    g_enc = g_enc.astype(str)
    r_enc = r_enc.astype(str)
    return b_enc, g_enc, r_enc


def dna_decode(b, g, r): 
    m, n = len(b), len(b[0])
    print(m, n)
    r_dec = np.ndarray((m, int(n*2)), dtype = np.uint8)
    g_dec = np.ndarray((m, int(n*2)), dtype = np.uint8)
    b_dec = np.ndarray((m, int(n*2)), dtype = np.uint8)
    
    for color, dec in zip((b, g, r), (b_dec, g_dec, r_dec)):
        for j in range(0, m):
            for i in range(0, n):
                dec[j, 2*i] = dna["{0}".format(color[j][i])][0]
                dec[j, 2*i+1] = dna["{0}".format(color[j][i])][1]
                
    b_dec = (np.packbits(b_dec, axis = -1))
    g_dec = (np.packbits(g_dec, axis = -1))
    r_dec = (np.packbits(r_dec, axis = -1))
    return b_dec, g_dec, r_dec


def dna_decode_2(b, g, r): 
    result_b, result_g, result_r = [], [], []

    for i in b:
        tmp = [int(s) for s in i]
        print(len(tmp))
        print(np.packbits(tmp))
        result_b.append(np.packbits(tmp))
    for i in g:
        tmp = [int(s) for s in i]
        print(len(tmp))
        print(np.packbits(tmp))
        result_g.append(np.packbits(tmp))
    for i in r:
        tmp = [int(s) for s in i]
        print(len(tmp))
        print(np.packbits(tmp))
        result_r.append(np.packbits(tmp))
    return result_b, result_g, result_r


def str2bin(sstring):
    """
    Transform a string (e.g. 'Hello') into a string of bits
    """
    bs = ''
    for c in sstring:
        bs = bs + bin(ord(c))[2:].zfill(8)
    return bs


def bin2str(bs):
    """
      Transform a binary string into an ASCII string
    """
    n = int(bs, 2)
    return binascii.unhexlify('%x' % n)


def byte2bin(byte_val):
    """
    Transform a byte (8-bit) value into a bitstring
    """
    return bin(byte_val)[2:].zfill(8)


def divisors(n):
    """
    Get the divisors of a natural number.
    :param n: the number
    :return: list of divisors
    """
    divs = []
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs.extend([i, n / i])

    divs = [int(d) for d in divs]
    return list(set(divs))


def bitxor(a, b):
    """
    Xor two bit strings (trims the longer input)
    """
    return "".join([str(int(x) ^ int(y)) for (x, y) in zip(a, b)])


def binarized_data(data):
    # convert every char to ASCII and then to binary
    byte_data = [byte2bin(ord(c)) for c in data]
    return generate_bits(byte_data)


def bits_to_dna(data, conversion_table):
    # convert binary sequence to DNA sequence
    return "".join([conversion_table[bits] for bits in data])


def dna_to_bits(data, conversion_table):
    # convert DNA sequence to binary sequence
    return "".join([conversion_table[dna_base] for dna_base in data])
    
    
def generate_pre_processing_tables():
    """
    Generate the 2 bits to dna bases encoding table (e.g. '01'->C)
    """
    global two_bits_to_dna_base_table
    global dna_base_to_two_bits_table

    # if you want random table
    # random.shuffle(dna_bases)
    two_bits_to_dna_base_table = dict(zip(two_bit_list, dna_bases))
    dna_base_to_two_bits_table = dict(zip(two_bits_to_dna_base_table.values(), two_bits_to_dna_base_table.keys()))


def generate_mutation_tables():
    """
    Generate the 4 bits to 2 dna bases encoding table (e.g. '0101'->CG)
    """
    global four_bits_to_two_dna_base_table
    global two_dna_base_to_four_bits_table

    # if you want random table
    # random.shuffle(two_dna_bases)
    four_bits_to_two_dna_base_table = dict(zip(four_bit_list, two_dna_bases))
    two_dna_base_to_four_bits_table = dict(
        zip(four_bits_to_two_dna_base_table.values(), four_bits_to_two_dna_base_table.keys()))
    
    
def group_bits(byte, step=2):
    """
    Group the bits from a byte / bigger sequence of bits into groups by length "step"
    :return: a list of groups
    """
    bits_groups = []
    for i in range(0, len(byte), step):
        bits_groups.append(byte[i:i + step])
    return bits_groups


def group_bases(dna_seq, step=2):
    """
    Group the DNA base from a sequence into groups by length "step"
    :return: a list of groups
    """
    bases_groups = []
    for i in range(0, len(dna_seq), step):
        bases_groups.append(dna_seq[i:i + step])
    return bases_groups


def generate_bits(byte_data):
    """
    Take every byte for sequence and group its bits
    :return:
    """
    grouped_bits_data = []

    for byte in byte_data:
        grouped_bits_data.extend(group_bits(byte))
    return grouped_bits_data    


def get_pattern(delimiter, s):
    """
    Get the pattern info between delimiters from the string
    """
    regex = "%s(.*?)%s" % (delimiter, delimiter)
    return re.findall(regex, s)


def recover_image(b, g, r, iname):
    p, q = len(b), len(b[0])
    img = np.zeros((p, q, 3), dtype = np.uint8)
    img[:, :, 2] = r
    img[:, :, 1] = g
    img[:, :, 0] = b
    cv2.imwrite((iname + '.jpg'), img)
    print('saved ecrypted image as encrypt.jpg')
    return img
