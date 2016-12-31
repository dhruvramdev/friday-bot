


def bug(text):
    file = open('bugs.txt', 'a')
    file.write(text + ':::' + '\n')
    file.close()

    

    return 'Thanks For Reporting The Bug'


def suggestion(text):
    file = open('suggestions.txt', 'a')
    file.write(text + ':::' + '\n')
    file.close()

   


    return 'Thanks For Suggesting'
