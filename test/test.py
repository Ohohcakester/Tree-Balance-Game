import os
import random
import string

def encrypt(input):
	arr = []
	for i in input:
		arr.append(ord(i))
	for i in range(1,len(arr)):
		arr[i] += arr[i-1]
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256
	for i in range(len(arr)-2,-1,-1):
		arr[i] += arr[i+1]
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256
	for i in range(0,len(arr)):
		arr[i] += (177*i)%256
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256

	for i in range(0,len(arr)):
		arr[i] += 32
		#print(arr[i])
	for i in range(0,len(arr)):
		arr[i] = chr(arr[i])
	return "".join(arr)

def decrypt(input):
	arr = []
	for i in input:
		arr.append(ord(i))
	for i in range(0,len(arr)):
		arr[i] -= 32

	for i in range(0,len(arr)):
		arr[i] -= (177*i)%256
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256
	for i in range(0,len(arr)-1):
		arr[i] -= arr[i+1]
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256
	for i in range(len(arr)-1,0,-1):
		arr[i] -= arr[i-1]
		arr[i] %= 256
		if arr[i] < 0: arr[i] += 256

	for i in range(0,len(arr)):
		arr[i] = chr(arr[i])
	return "".join(arr)


fileName = "test.dat"
def write(data):
	global fileName
	f = open(fileName, 'w+', encoding='utf-8')
	f.write(data)

def read():
	global fileName
	if os.path.isfile(fileName):
		f = open(fileName, 'r', encoding='utf-8')
		data = f.read()
		return data


value = "aldkjk32r2.@#>@#$2322asdasd123.--.@4234kl14!#$"
value = """ ó×pÜ$³"duXê
ÆHÃ¹ÂÑ¯_â4XO­R^=ëk¾àÔ1ÔÞºiç7ZL§
GT0Þ_¯ÑÆ ÁË¨TÒ#C5úô-5¼8§YîRiÜúë«=¢ÖÜµ"""

value = "-1.-1.-1.-1@-1.-1.-1@7.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1,-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1"
def test(value):
	e = encrypt(value) 
	d = decrypt(e)
	#print(value)
	#print(e)
	#print(d)
	if not (value == d):
		print("Error 1")
		print(value)
		return False

	d2 = decrypt(value)
	e2 = encrypt(d2)
	#print(value)
	#print(d2)
	#print(d)
	if not (value == e2):
		print("Error 2")
		print(value)
		return False

	write(value)
	r2 = read()
	if not (value == r2):
		print("Error 3")
		print(value)
		return False

	write(encrypt(value))
	r = decrypt(read())
	#print(r)
	if not (value == r):
		print("Error 4")
		print(value)
		return False
	return True


for i in range(0,1000):
	asd = ''.join([random.choice(string.digits + "-.@......--") for n in range(120)])
	print(asd)
	test(asd)
print(test("194051835904143q;r3rf%@$%34fipo5345fi34%@FOD@$%#$i"))