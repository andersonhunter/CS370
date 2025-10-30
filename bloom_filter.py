from bitarray import bitarray
import hashlib

# Define k - the number of hash functions
K = 13

# Define M - number of bits in bit array
M = 291102973

class BloomFilter:
    # Create a bit array of 291,102,973 bits based off approximate length of file
    # Bit array with 0.0001 probability of collisions determined using:
    # https://hur.st/bloomfilter/
    def __init__(self):
        self.bit_array = bitarray(M)
        self.bit_array.setall(0)


    def insert_into_bit_array(self, plain: str) -> None:
        # Use double hashing (loop from i = 0 - k-1, calculate h1 and h2, 
        # then index = h1 + i * h2) % len(bitarray), 
        # then set bit at that index and keep moving
        digest = hashlib.sha256(plain.encode('utf-8')).digest()
        h1, h2 = int.from_bytes(digest[16:]), int.from_bytes(digest[:16])
        for i in range(K):
            index = (h1 + i * h2) % M
            self.bit_array[index] = 1

    def check_bit_array(self, plain: str) -> bool:
        # Check if value in filter
        # Return True if possible, False otherwise
        digest = hashlib.sha256(plain.encode('utf-8')).digest()
        h1, h2 = int.from_bytes(digest[16:]), int.from_bytes(digest[:16])
        for i in range(K):
            index = (h1 + i * h2) % M
            if not self.bit_array[index]:
                print("no")
                return False
        print("maybe")
        return True


if __name__ == '__main__':
    # Set up the filter
    bf = BloomFilter()
    
