import re


s1 = "background-image:url(https://apps.rhs.org.uk/plantselectorimages/detail/GWIS951.jpg);"
s2 = "background-image:url('https://apps.rhs.org.uk/plantselectorimages/detail/visi72972.jpg');"
pattern = re.compile(r"https.*?jpg")
s = pattern.findall(s1)
print(s)
s = pattern.findall(s2)
print(s)