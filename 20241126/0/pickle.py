import pickle
b = pickle.dumps(1234567, protocol = 0)
print(pickle.loads(b))
