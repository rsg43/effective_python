# string vs bytes
a = b"h\x65llo"
print(list(a))
print(a)

b = "a\u0300 propos"
print(list(b))
print(b)
