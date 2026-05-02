import sys

# Complete the 'sequence_generator' class below.
#
# The class should be a context manager and expose a 'generate' method.

class sequence_generator:
    def __init__(self, start, step):
        """Initializes the sequence with start and step."""
        # Implementation here
        pass

    def generate(self):
        """Yields numbers in the sequence starting from 'start' incrementing by 'step'."""
        # Implementation here
        pass

    def __enter__(self):
        """Return the generator object when entering the context."""
        # Implementation here
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        """Cleanup logic if needed."""
        # Implementation here
        pass

def main():
    input_data = sys.stdin.read().splitlines()
    if len(input_data) < 3:
        return
        
    try:
        start = int(input_data[0].strip())
        step = int(input_data[1].strip())
        num = int(input_data[2].strip())
        
        with sequence_generator(start, step) as gen:
            for _ in range(num):
                # Fetch next value from generator
                print(next(gen))
                
    except Exception as e:
        # Traceback will be captured by driver
        raise e

if __name__ == "__main__":
    main()
