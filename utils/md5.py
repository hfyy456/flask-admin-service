import hashlib
def str2md5(str):
    str=str.encode(encoding='utf-8')
    md5=hashlib.md5(str).hexdigest()
    return md5