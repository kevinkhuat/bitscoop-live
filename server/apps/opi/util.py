def dict_soft_merge(object1, object2):
    for key in object2:
        # If the property is a dictionary
        if type(key) is dict:
            object1 = dict_soft_merge(object1, key)
        # If the property is a list, merge the lists without duplication
        elif type(key) is list:
            object1 = list_soft_merge(object1, key)
        elif type(key) is tuple:
            object1 = tuple_soft_merge(object1, key)
        else:
            object1[key] = object2[key]

    return object1


def list_soft_merge(object1, object2):
    # Iterate through the list in object2
    for item in object2:
        # If there is a property in object2 not in object1, add it to object1
        if item not in object1[object2]:
            object1.append(item)

    return object1


def tuple_soft_merge(object1, object2):
    # Iterate through the list in object2
    for item in object2:
        # If there is a property in object2 not in object1, add it to object1
        if item not in object1:
            object1 = (item,) + object1

    return object1