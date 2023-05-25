def clean_string(string):
    if string in ["", " "]:
        return ""
    
    if string[-1] == " ":
        string = string[:-1]

    if string[0] == " ":
        string = string[1:]
    if len(string) >= 2:
        if string[-1].lower() == "s" and string[-2].lower() != "s":
            string = string[:-1]

    return string

def stem(string):
    A = string.split('&')
    A = [b.split(',') for b in A]

    flat_list = [item for sublist in A for item in sublist]


    return [clean_string(string) for string in flat_list if string != '']
    