# encription of user credentials.. use separately to store encripted credentials in config file
import credentials
import base64
import hashlib
import json
from cryptography.fernet import Fernet


def encode_user(user_email, user_password):
    md5_password = hashlib.md5(user_password.encode()).hexdigest()
    encoded_credentials = base64.b64encode(
        f"{user_email}:{md5_password}".encode()
    ).decode()

    encrypted_credentials = encrypt(encoded_credentials).decode()

    # Store the encrypted credentials in the configuration file as JSON
    config = {
        #'credentials': f'{str(encrypted_credentials)[2:-1]}' # Remove the leading 'b' from the byte string
        "credentials": f"{encrypted_credentials}"  # Remove the leading 'b' from the byte string
    }

    with open("eniscope_api.conf", "w") as config_file:
        json.dump(config, config_file)


def encrypt(data):
    cipher_suite = Fernet(credentials.encryption_key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data


# encode_user('webapi@refactorenergy.es', '3DPtbMsGpfKj4Q==')
user_email = input("Enter user email: ")
user_password = input("Enter user password: ")
encode_user(user_email, user_password)
print("Credentials encrypted and stored in eniscope_api.conf")

# check read of encrypted credentials
# with open('eniscope_api.conf', 'r') as config_file:
#         config = json.load(config_file)
# encrypted_credentials = config.get('credentials').encode()
# cipher_suite = Fernet(credentials.encryption_key)

# decrypted_data = cipher_suite.decrypt(encrypted_credentials)
# decrypted_data.decode()
