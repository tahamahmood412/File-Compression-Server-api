import gzip
import hashlib
from PIL import Image

def compress_file(file_name):
    try:
        with open(file_name, 'rb') as file:
            with gzip.open(file_name + '.gz', 'wb') as compressed_file:
                compressed_file.writelines(file)
        
        print(f"File '{file_name}' compressed successfully as '{file_name}.gz'")

        with open(file_name, 'rb') as original_file:
            sha256_hash = hashlib.sha256()
            while chunk := original_file.read(8192):
                sha256_hash.update(chunk)
            file_hash = sha256_hash.hexdigest()

        print(f"SHA-256 hash of original file '{file_name}': {file_hash}")

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def compress_image(file_name):
    try:
        image = Image.open(file_name)
        max_width = 800
        max_height = 600
        image.thumbnail((max_width, max_height), Image.ANTIALIAS)

        compressed_image_name = f"compressed_{file_name}"
        image.save(compressed_image_name, optimize=True, quality=85)

        with open(compressed_image_name, 'rb') as compressed_file:
            sha256_hash = hashlib.sha256()
            while chunk := compressed_file.read(8192):
                sha256_hash.update(chunk)
            file_hash = sha256_hash.hexdigest()

        print(f"SHA-256 hash of compressed image '{compressed_image_name}': {file_hash}")

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def decompress_file(compressed_file_name):
    try:
        with gzip.open(compressed_file_name, 'rb') as compressed_file:
            decompressed_data = compressed_file.read()
            original_file_name = compressed_file_name[:-3]
            with open(original_file_name, 'wb') as decompressed_file:
                decompressed_file.write(decompressed_data)
        
        print(f"File '{compressed_file_name}' decompressed successfully as '{original_file_name}'")

        with open(original_file_name, 'rb') as decompressed_file:
            sha256_hash = hashlib.sha256()
            while chunk := decompressed_file.read(8192):
                sha256_hash.update(chunk)
            file_hash = sha256_hash.hexdigest()

        print(f"SHA-256 hash of decompressed file '{original_file_name}': {file_hash}")

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        print("\n------ File Compression Tool ------")
        print("1. Compress File")
        print("2. Compress Image")
        print("3. Decompress File")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 4:
                break
            elif choice not in [1, 2, 3]:
                print("Invalid input. Please enter a valid choice (1-4).")
                continue

            file_name = input("Enter file name: ")

            if choice == 1:
                compress_file(file_name)
            elif choice == 2:
                compress_image(file_name)
            elif choice == 3:
                decompress_file(file_name)
        
        except ValueError:
            print("Invalid input. Please enter a number (1-4) as your choice.")


main()