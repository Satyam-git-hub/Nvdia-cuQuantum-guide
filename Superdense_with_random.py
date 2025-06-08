import cudaq
import random

# Mapping of classical bits to gate operations (standard in superdense coding)
# def apply_encoding(alice_qubit, message):
#     if message == '00':
#         pass  # Do nothing
#     elif message == '01':
#         z(alice_qubit)  # Phase flip
#     elif message == '10':
#         x(alice_qubit)  # Bit flip
#     elif message == '11':
#         z(alice_qubit)
#         x(alice_qubit)


@cudaq.kernel
def superdense_kernel(message: int):
    qubits = cudaq.qvector(2)  # qubits[0] = Alice, qubits[1] = Bob

    # Create Bell pair (entangled state)
    h(qubits[0])
    cx(qubits[0], qubits[1])

    # Alice encodes classical bits based on `message` (0 to 3)
    if message == 1:       # 01
        x(qubits[0])
    elif message == 2:     # 10
        z(qubits[0])
    elif message == 3:     # 11
        z(qubits[0])
        x(qubits[0])

    # Bob decodes
    cx(qubits[0], qubits[1])
    h(qubits[0])

    # Measure both qubits
    mz(qubits[0])  # Most significant bit
    mz(qubits[1])  # Least significant bit


# Choose a random 2-bit message for Alice to send
message = random.choice(['00', '01', '10', '11'])
#print(f"\n🧠 Alice sends: {message}")
message_map = {
    '00': 0,
    '01': 1,
    '10': 2,
    '11': 3
}
# Run the kernel 1000 times to verify result
for message_bits, encoded_value in message_map.items():
    if message == message_bits:
        print(f"\n🧠 Alice sends: {message_bits}")
        print(f"\n🧠 Alice sends ev: {encoded_value}")

        result = cudaq.sample(superdense_kernel, encoded_value, shots_count=1000)
        print(f"📦 Bob receives: {result}")
# result = cudaq.sample(superdense_coding, message, shots_count=1000)

# # Decode result
# print(f"📦 Bob receives: {dict(result)}")
