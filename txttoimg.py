def txttoimg(s):
	from PIL import Image
	f=open(s,'r').read()
	f=f.split('\n')
	l=[int(i) for i in f[:len(f)-1]]
	f=f[-1:][0]
	f=f[1:len(f)-1]
	size=f.split(', ')
	size=tuple([int(i) for i in size])
	im=Image.new('L',size)
	im.putdata(l)
	im.save('test.jpg')