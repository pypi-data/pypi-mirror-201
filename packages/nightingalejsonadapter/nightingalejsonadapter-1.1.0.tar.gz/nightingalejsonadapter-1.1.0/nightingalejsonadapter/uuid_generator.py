import os

class UUIDGenerator(object):
    def __init__(self):
        pass
        
    def generate_uuid(self):
        randombytes = os.urandom(16)
        return randombytes.hex()
        
    def generate_uuid_pretty(self):
        uuid = self.generate_uuid()
        pretty_uuid = uuid[:8] + "-" + uuid[8:12] + "-" + uuid[12:16] + "-" + uuid[16:20] + "-" + uuid[20:]
        # self.set_last_generated_uuid(uuid)
        return pretty_uuid
        
    if __name__ == '__main__':
        generate_uuid_pretty()