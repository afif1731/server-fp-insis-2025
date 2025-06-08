import bcrypt

async def hash_pass(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))

async def compare(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))