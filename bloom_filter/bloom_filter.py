from bitarray import bitarray
import hashlib
import time
from sortedcontainers import SortedSet

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
        # Use sorted set - O(logn) for lookups as opposed to O(n)
        self.db = SortedSet()

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
                return False
        return True

    def check_membership(self, plain: str) -> bool:
        return plain in self.db

if __name__ == '__main__':
    # Set up the filter
    bf = BloomFilter()
    # Read in the rockyou file
    now_time = time.time()
    with open("rockyou.ISO-8859-1.txt") as f:
        # Filter it
        count = 0
        for x in f:
            x = x.replace("\n", "")
            bf.insert_into_bit_array(x)
            bf.db.add(x)
            count += 1
    print(
        f'Processed {count} elements from rockyou in {round(time.time() - now_time, 4)} seconds'
        )
    now_time = time.time()
    with open("dictionary.txt", encoding="ISO-8859-1") as f:
        # Check membership of each item
        count = 0
        true_pos, false_pos, false_neg, true_neg = 0, 0, 0, 0
        for x in f:
            count += 1
            x = x.replace("\n", "")
            # Case 1: In db, pass bloom filter (true positive)
            # Case 3: Not in db, pass bloom filter (false positive)
            if bf.check_bit_array(x):
                if bf.check_membership(x):
                    true_pos += 1
                else:
                    false_pos += 1
            # Case 2: In db, don't pass bloom filter (false negative)
            # Case 4: Not in db, don't pass bloom filter (true negative)
            else:
                if bf.check_membership(x):
                    false_neg += 1
                else:
                    true_neg += 1
    print(
        f'Processed {count} elements from dictionary in {round(time.time() - now_time, 4)} seconds'
    )
    print(f'TP, FP, FN, TN = {true_pos, false_pos, false_neg, true_neg}')
