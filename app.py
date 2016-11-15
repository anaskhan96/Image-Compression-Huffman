import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import imgtotxt
import txttoimg
from flask import Flask,render_template,request,redirect,send_from_directory,make_response
from werkzeug import secure_filename
app=Flask(__name__)
s=dict()

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html',u="Upload Image",c="COMPRESS!",ul='/compressed')

@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
	if request.method=='POST':
		f = request.files['fileToUpload']
		imgname=secure_filename(f.filename)
		f.save(imgname)
		imgtotxt.imgtotxt(imgname)
		return render_template('index.html',u="Image Uploaded!",l="Upload Text")

@app.route('/compressed',methods=['GET','POST'])
def compress():
	if request.method=='POST':
		os.system('gcc huffman.c')
		v=os.popen('./a.out')
		v=v.read().split('\n')
		v=v[:len(v)-1]
		keys,data=[int(i.split(': ')[0]) for i in v],[i.split(': ')[1] for i in v]
		global s
		s=dict(zip(keys,data))
		dtbw=[]
		with open('test1.txt') as f:
			for i in f:
				try:
					dtbw.append(s[int(i)])
				except:
					dtbw.append(i)
		dtbw=[str(i)+'\n' for i in dtbw]
		open('compressed.txt','w').writelines(dtbw)
		response=make_response(send_from_directory('/Users/anask/DSFlask','compressed.txt'))
		response.headers["Content-Disposition"]="attachment; filename=compressed.txt"
		os.system('rm compressed.txt')
		return response
		#return render_template('index.html',u="Image Uploaded!",c="DECOMPRESS!",ul='/decompressed')
	return "TEEHEE"

@app.route('/decomupload',methods=['GET','POST'])
def decom():
	if request.method=='POST':
		f = request.files['txtToUpload']
		txtname=secure_filename(f.filename)
		f.save(txtname)
		return render_template('index.html',u="Image Uploaded!",l="Text Uploaded!")

@app.route('/decompressed',methods=['GET','POST'])
def decompress():
	if request.method=='POST':
		global s
		d=[]
		with open('compressed.txt','r') as f:
			l=[]
			f=f.read().split('\n')
			f=f[:len(f)-1]
			l,size=[i for i in f[:len(f)-1]],f[-1:][0]
			for i in l:
				for key,value in s.iteritems():
					if value==i:
						d.append(key)
			d=[str(i)+'\n' for i in d]
			d.append(str(size))
			open('decompressed.txt','w').writelines(d)
			txttoimg.txttoimg('decompressed.txt')
			response=make_response(send_from_directory('/Users/anask/DSFlask','test.jpg'))
			response.headers["Content-Disposition"]="attachment; filename=your_image.jpg"
			return response
		return "Heyy"
	return "TEEHEE"
if __name__=='__main__':
	app.run(host='0.0.0.0',port=5000)