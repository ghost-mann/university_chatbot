import hashlib

h = hashlib.new("SHA256")
h.update(b"Hello world!")

print(h.hexdigest())
print(h.digest())