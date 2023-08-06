def arop(Function, List):
    array = map(Function, List)
    array = list(array)
    return array

def star(String):
    array = []
    for i in range(len(String)):
        array.append(String[i])
    return array

def arst(List):
    string = ""
    for i in range(len(List)):
        string += str(List[i])
    return string

def rale(List):
    return range(len(List))