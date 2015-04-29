def dictSoftMerge(object1, object2):
    for key in object2:
        # If the property is a dictionary
        if type(key) is dict:
            object1 = dictSoftMerge(object1, key)
        # If the property is a list, merge the lists without duplication
        elif type(key) is list:
            object1 = listSoftMerge(object1, key)
        elif type(key) is tuple:
            object1 = tupleSoftMerge(object1, key)
        else:
            object1[key] = object2[key]
    return object1

def listSoftMerge(object1, object2):
    # Iterate through the list in object2
    for item in object2:
        # If there is a property in object2 not in object1, add it to object1
        if item not in object1[object2]:
            object1[object2].append(item)
    object1[object2] = object2
    return object1

def tupleSoftMerge(object1, object2):
    # Iterate through the list in object2
    for item in object2:
        # If there is a property in object2 not in object1, add it to object1
        if item not in object1:
            object1 = item + object1
    object1[object2] = object2
    return object1