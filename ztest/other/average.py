l = [10,5,10,10,7]
print reduce(lambda x, y: x + y, l) / float(len(l))

