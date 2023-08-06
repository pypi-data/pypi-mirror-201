import string, random, hashlib



__all__=['get_random_string', 'get_md5']
def get_random_string(l=10):
    letters = string.digits + string.ascii_letters
    return ''.join(random.choice(letters) for i in range(l))


def get_md5(txt):
    md5hash = hashlib.md5(str(txt).encode('utf-8'))
    return md5hash.hexdigest()
