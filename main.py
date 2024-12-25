#---------------------------------Global Variables--------------------------------------------------#
import random
S_BOX = (
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
)

RCON = (
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
)
# -------------------------------------Encryption----------------------------------------------------#
def substitute_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = S_BOX[state[i][j]]
    return state

def shift_rows(state):
    for i in range(1, 4):
        state[i] = state[i][i:] + state[i][:i]
    return state

def mix_columns(state):
    for i in range(4):
        s0 = state[0][i]
        s1 = state[1][i]
        s2 = state[2][i]
        s3 = state[3][i]
        
        state[0][i] = multiply(s0, 2) ^ multiply(s1, 3) ^ s2 ^ s3
        state[1][i] = s0 ^ multiply(s1, 2) ^ multiply(s2, 3) ^ s3
        state[2][i] = s0 ^ s1 ^ multiply(s2, 2) ^ multiply(s3, 3)
        state[3][i] = multiply(s0, 3) ^ s1 ^ s2 ^ multiply(s3, 2)
    return state

def multiply(a, b):
    
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B  
        b >>= 1
    return result

def add_round_key(state, round_key):
    
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    return state


def key_expansion(key, round_constants, Q):
    round_keys = [key[i:i+4] for i in range(0, len(key), 4)]
    
    for i in range(Q):
        for j in range(4):
            
            new_key = [round_keys[-4][k] ^ round_keys[-3][k] ^ round_keys[-2][k] for k in range(4)]
            new_key = complex_operation(new_key, round_constants[i])
            random_word = generate_random_word()
            new_key = [new_key[k] ^ random_word[k] for k in range(4)]
            round_keys.extend([new_key])
    
    return round_keys

def complex_operation(word, round_constant):
    
    word = word[1:] + [word[0]]
    word = [S_BOX[b] for b in word]
    word[0] ^= round_constant
    
    return word

def generate_random_word():
    
    return [random.randint(0, 255) for _ in range(4)]


def aes_encrypt(plaintext, key):
    
    padding_length = 16 - len(plaintext) % 16
    plaintext += bytes([padding_length]) * padding_length
    state = [[plaintext[i + 4 * j] for i in range(4)] for j in range(4)]
    
    
    round_keys = key
    
    
    state = add_round_key(state, round_keys[:4])
    
    
    for i in range(1, 10):
        state = substitute_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)  
        state = add_round_key(state, round_keys[4*i:4*(i+1)])
    
    
    state = substitute_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[40:])
    
    return state


# ------------------------------------------------------------Decryption-------------------------------#
INV_S_BOX = (
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    )
def inverse_substitute_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = INV_S_BOX[state[i][j]]
    return state
def inverse_shift_rows(state):
    for i in range(1, 4):
        state[i] = state[i][-i:] + state[i][:-i]
    return state
def inverse_mix_columns(state):
    
    transformation_matrix = [
        [0x0e, 0x0b, 0x0d, 0x09],
        [0x09, 0x0e, 0x0b, 0x0d],
        [0x0d, 0x09, 0x0e, 0x0b],
        [0x0b, 0x0d, 0x09, 0x0e]
    ]
    
    
    new_state = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            new_state[i][j] = (
                multiply(transformation_matrix[i][0], state[0][j]) ^
                multiply(transformation_matrix[i][1], state[1][j]) ^
                multiply(transformation_matrix[i][2], state[2][j]) ^
                multiply(transformation_matrix[i][3], state[3][j])
            )
    return new_state
def aes_decrypt(ciphertext, round_key):
    
    state = [[ciphertext[i + 4 * j] for i in range(4)] for j in range(4)]
    
   
    round_keys = round_key
    
    
    state = add_round_key(state, round_keys[40:])
    
    
    for i in range(9, 0, -1):
        state = inverse_shift_rows(state)
        state = inverse_substitute_bytes(state)
        state = add_round_key(state, round_keys[4*i:4*(i+1)])
        state = inverse_mix_columns(state)  
    
    
    state = inverse_shift_rows(state)
    state = inverse_substitute_bytes(state)
    state = add_round_key(state, round_keys[:4])
    
    return state


# ---------------------------------------------------Test Advanced AES-----------------------------------------#

def main():
    # Encryption main function 1 maybe work if so keep , else go check for ver 2
    plaintext = 'Yes, will launch'
    key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x97, 0x21, 0x09, 0x9d, 0x8f, 0x62]  
    round_keys=key_expansion(key,RCON,10)
    
    encrypted_state = aes_encrypt(plaintext.encode(),round_keys)

    
    decrypted_state = aes_decrypt([byte for sublist in encrypted_state for byte in sublist], round_keys)

    
    decrypted_plaintext = ''.join([chr(byte) for sublist in decrypted_state for byte in sublist])

    
    print("Original plaintext:", plaintext)
    print(encrypted_state)
    print(decrypted_state)
    print("Decrypted plaintext:", decrypted_plaintext)

# ---------------------------------------------------------------------------------------------------------------------------#
    # Original master key
    original_master_key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x97, 0x21, 0x09, 0x9d, 0x8f, 0x62]
    
if __name__ == "__main__":
    main()
