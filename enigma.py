
import json
import sys

# ============ ENIGMA ============

class Enigma:

    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.wheels = wheels
        self.reflector_map = reflector_map


    def encrypt(self, message):
        original_wheels = self.wheels.copy()
        encrypted_count = 0
        encrypted_message = ""
        for letter in message:
            if letter.islower():
                encrypted_message += encrypt_lowercase_letter(self, letter)
                encrypted_count += 1
            else:
                encrypted_message += letter
            update_wheels(encrypted_count)
        self.wheels = original_wheels.copy()
        return encrypted_message


    def update_wheels(self,encrypted_count):
        # update W1
        if self.wheels[0] + 1 > 8:
            self.wheels[0] = 1
        else:
            self.wheels[0] += 1
        # update W2
        if encrypted_count % 2 == 0:
            self.wheels[1] *= 2
        else:
            self.wheels[1] -= 1
        # update W3
        if encrypted_count % 10 == 0:
            self.wheels[2] = 10
        elif encrypted_count % 3 == 0:
            self.wheels[2] = 5
        else:
            self.wheels[2] = 0


# ============ JSONFileException ============

class JSONFileException(Exception):
    pass


# ============ OTHER FUNCTIONS ============

def load_enigma_from_path(path):
    try:
        with open(path, 'r') as json_file:
            json_dict = json.load(json_file)
            return Enigma(json_dict["hash_map"], json_dict["wheels"], json_dict["reflector_map"])
    except Exception:
        raise JSONFileException


def encrypt_lowercase_letter(enigma, letter):
    i = enigma.hash_map(letter)
    wheels_value = ((2 * enigma.wheels[0]) - enigma.wheels[1] + enigma.wheels[2]) % 26
    if wheels_value != 0:
        i += wheels_value
    else:
        i += 1

    i %= 26
    c1 = enigma.hash_map(i)
    c2 = enigma.reflector_map[c1]

    i = enigma.hash_map(c2)
    if wheels_value == 0:
        i -= 1
    else:
        i -= wheels_value
    i %= 26
    c3 = enigma.hash_map(i)
    return c3

def get_params():
    params = sys.argv
    for i in range(1, len(args), 2):
        if i + 1 >= len(args):
            raise ###
        if args[i] == '-c':
            config_path = args[i + 1]
        elif args[i] == '-i':
            input_path = args[i + 1]
        elif args[i] == '-o':
            output_path == args[i + 1]
        else:
            raise ###
    if not config_path or not input_path:
        raise
    if not output_path:
        output_path = sys.stdout
    return config_path, input_path, output_path
    
    
def terminate():
    