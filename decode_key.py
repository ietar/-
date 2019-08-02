a='Lorem ipsum dolor sit amet'

addcount = 26

while addcount:
    b=''
    for i in a:
        if i == ' ':
            pass
        else:
            if ord(i.lower())+1 > 122:#大写
                temp = ord(i)-26
                i= chr(temp + 1)
            else:#小写
                i=chr(ord(i) + 1)
        b+=i
        a=b
    print(b)
    addcount -= 1


    


