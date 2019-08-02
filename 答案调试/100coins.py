import re
s = '''1|B
2|E
3|B
4|E
5|B
6|E
7|B
8|E
9|B
10|E
11|B 00000
12|B
13|E
14|B
15|B
16|E
17|B
18|E
19|E
20|E
21|B
22|E'''

while True:
    temp = s
    s = re.sub(r'\d+\|B\n\d+\|E', '', s)
    s = re.sub(r'\n{2,}', '\n', s).strip('\n')
    if s == temp:
        print(s)
        break
