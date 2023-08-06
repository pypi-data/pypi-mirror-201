def start(data):
    n={}
    for i in data[:-1]:
        if not i == data[-1]:
            n[i]=data[i]
    return n