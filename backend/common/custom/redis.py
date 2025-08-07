def key_maker(key, key_prefix, version):
    return ":".join([key_prefix, str(version), key])
