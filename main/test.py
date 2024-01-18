import cassiopeia as cass

def getAPI_key():
    f = open("key.txt", "r")
    return f.read()