
import json
import sys

W1 = 0
W2 = 1
W3 = 2
W1_UPDATE_FLAG = 8
W3_UPDATE_FLAG_1 = 10
W3_UPDATE_FLAG_2 = 3
W3_UPDATE_VALUE_1 = 10
W3_UPDATE_VALUE_2 = 5
WHEELS_VALUE_MOD = 26
GET_PARAMS_EXIT_MESSEGE = "Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>"
SCRIPT_EXIT_MESSEGE = "The enigma script has encountered an error"

# ==================== ENIGMA ==================== #

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
                encrypted_message += self.encrypt_lowercase_letter(letter)
                encrypted_count += 1
            else:
                encrypted_message += letter
            enigma.update_wheels(encrypted_count)
        self.wheels = original_wheels.copy()
        return encrypted_message


    def update_wheels(self,encrypted_count):
        # update W1
        if self.wheels[W1] + 1 > W1_UPDATE_FLAG:
            self.wheels[W1] = 1
        else:
            self.wheels[W1] += 1
        # update W2
        if encrypted_count % 2 == 0:
            self.wheels[W2] *= 2
        else:
            self.wheels[W2] -= 1
        # update W3
        if encrypted_count % W3_UPDATE_FLAG_1 == 0:
            self.wheels[W3] = W3_UPDATE_VALUE_1
        elif encrypted_count % W3_UPDATE_FLAG_2 == 0:
            self.wheels[W3] = W3_UPDATE_VALUE_2
        else:
            self.wheels[W3] = 0
            
            
    def encrypt_lowercase_letter(self, c):
        reversed_hash_map = {value: key for key, value in self.hash_map.items()}
        i = self.hash_map[c]
        wheels_value = ((2 * self.wheels[W1]) - self.wheels[W2] + self.wheels[W3]) % WHEELS_VALUE_MOD
        if wheels_value != 0:
            i += wheels_value
        else:
            i += 1
        i %= WHEELS_VALUE_MOD
        c1 = reversed_hash_map[i]
        c2 = self.reflector_map[c1]
        i = self.hash_map[c2]
        if wheels_value != 0:
            i -= wheels_value
        else:
            i -= 1
        i %= WHEELS_VALUE_MOD
        c3 = reversed_hash_map[i]
        return c3


# ==================== JSONFileException ==================== #

class JSONFileException(Exception):
    pass


# ==================== OTHER FUNCTIONS ==================== #

def load_enigma_from_path(path):
    try:
        with open(path, 'r') as json_file:
            json_dict = json.load(json_file)
            return Enigma(json_dict["hash_map"], json_dict["wheels"], json_dict["reflector_map"])
    except Exception:
        raise JSONFileException


def get_params():
    params = sys.argv
    config_path = None
    input_path = None
    output_path = sys.stdout
    for i in range(1, len(params), 2):
        if i + 1 >= len(params):
            terminate(GET_PARAMS_EXIT_MESSEGE)
        if params[i] == '-c':
            config_path = params[i + 1]
        elif params[i] == '-i':
            input_path = params[i + 1]
        elif params[i] == '-o':
            output_path = params[i + 1]
        else:
            terminate(GET_PARAMS_EXIT_MESSEGE)
    if not config_path or not input_path:
        terminate(GET_PARAMS_EXIT_MESSEGE)
    return config_path, input_path, output_path
    
    
def terminate(message):
    sys.stderr.write(message)
    exit(1)


# ==================== SCRIPT ==================== #

if __name__ == "__main__":
    config_file, input_path, output_path = get_params()
    try:
        enigma = load_enigma_from_path(config_file)
        with open(input_path, 'r') as input:
            encrypted_str = ""
            for line in input:
                encrypted_str += enigma.encrypt(line)
    except Exception:
        terminate(SCRIPT_EXIT_MESSEGE)
    if output_path == sys.stdout:
        print(encrypted_str)
    else:
        try:
            with open(output_path, 'w') as output:
                output.write(encrypted_str)
        except Exception:
            terminate(SCRIPT_EXIT_MESSEGE)
