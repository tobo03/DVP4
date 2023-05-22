def replaceChar(string):
    to_empty = '''"`,.@/$;'!:*#+\n\t?=~[]()'''
    for char in list(to_empty):
        string = string.replace(char, '')
    
    to_underscore = ''' |^\\-'''
    for char in list(to_underscore):
        string = string.replace(char, "_")

    string = string.replace("&","and")
    string = string.replace("%","percent")

    return string