from xiezuocat import sm3

def signature_sm3_str(data):
    key_array = list(data.keys())
    key_array.sort()
    sm3_str = ''
    for key in key_array:
        value = data[key]
        if value:
            if isinstance(value, int) or isinstance(value, str) or isinstance(value, float):
                sm3_str += f'{key}={value}'

    return sm3_str

def signature_sm3(data, key):
    signature_sm3_string = signature_sm3_str(data)
    signature_sm3_string += f'secretKey={key}'
    sm3Str = sm3.sm3(signature_sm3_string)

    return sm3Str


