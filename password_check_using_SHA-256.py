import hashlib

def generate_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_file_integrity(original_hash, filepath):
    current_hash = generate_file_hash(filepath)
    if original_hash == current_hash:
        print("File integrity intact.")
    else:
        print("Warning: File integrity compromised!")

if __name__ == "__main__":
    filepath = input("Enter the file path: ")
    original_hash = input("Enter the original SHA-256 hash: ")
    
    check_file_integrity(original_hash, filepath)
