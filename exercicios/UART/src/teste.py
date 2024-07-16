tx_buffer = bytearray(20)

# Fill the buffer with characters and numbers
for i, value in enumerate(data):
    if isinstance(value, str):
        tx_buffer[i] = ord(value)  # Convert string characters to ASCII codes
    else:
        tx_buffer[i] = value  # Assign numeric values directly

print(tx_buffer)

non_zero_buffer = bytearray()

# Find the first zero index (or len(tx_buffer) if no zeros)
first_zero_index = next((i for i, x in enumerate(tx_buffer) if x == 0), len(tx_buffer))

# Create a new byte array with non-zero elements
a= tx_buffer[:first_zero_index]

print(a)