from collections import OrderedDict
import sys

# Complete the 'TopKCache' class below.
#
# The system keeps all data but classifies keys into HOT (top K recently used) 
# or COLD (all other stored keys) based on usage recency.

class TopKCache:
    def __init__(self, k):
        """Initializes the cache with a HOT capacity of K key-value pairs."""
        self.k = k
        # Implementation here
        pass

    def put(self, key, value):
        """Stores the key-value pair and marks it as the most recently used."""
        # Implementation here
        pass

    def get(self, key):
        """Returns value for key and marks as most recently used. Returns None if missing."""
        # Implementation here
        return None

    def get_status(self, key):
        """Returns 'HOT' if key is in top K recently used, 'COLD' if not, or 'None' if missing.
        Does not modify the recency order.
        """
        # Implementation here
        return None

def process_cache_ops():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    try:
        q = int(input_data[0])
    except:
        return

    cache = None
    
    for i in range(1, q + 1):
        if i >= len(input_data): break
        line = input_data[i].split()
        if not line: continue
        
        cmd = line[0]
        try:
            if cmd == "init":
                cache = TopKCache(int(line[1]))
            elif cmd == "put":
                cache.put(line[1], line[2])
            elif cmd == "get":
                res = cache.get(line[1])
                print(res if res is not None else "None")
            elif cmd == "status":
                print(cache.get_status(line[1]))
        except Exception as e:
            # Propagate detailed error for debugging
            raise e

if __name__ == "__main__":
    process_cache_ops()
