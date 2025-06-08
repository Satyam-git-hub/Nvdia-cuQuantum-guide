import cudaq

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


# CUDA-Q kernel
@cudaq.kernel
def superdense_coding(message: int):
    # Allocate two qubits: qubit[0] for Alice, qubit[1] for Bob
    qubits = cudaq.qvector(2)

    # Step 1: Create entanglement (Bell pair)
    h(qubits[0])
    cx(qubits[0], qubits[1])

    # Step 2: Alice encodes her message on her qubit
    if message == 1:
        z(qubits[0])
    elif message == 2:
        x(qubits[0])
    elif message == 3:
        z(qubits[0])
        x(qubits[0])

    # Step 3: Alice sends her qubit to Bob.
    # Bob now owns both qubits.

    # Step 4: Bob decodes
    cx(qubits[0], qubits[1])
    h(qubits[0])

    # Step 5: Bob measures both qubits
    mz(qubits[0])
    mz(qubits[1])

# Map classical messages to numbers
message_map = {
    '00': 0,
    '01': 1,
    '10': 2,
    '11': 3
}

# Run the kernel for each possible 2-bit message
for message_bits, encoded_value in message_map.items():
    print(f"\n🧠 Alice sends: {message_bits}")
    print(f"\n🧠 Alice sends ev: {encoded_value}")
    result = cudaq.sample(superdense_kernel, encoded_value, shots_count=1000)
    print(f"📦 Bob receives: {result}")
