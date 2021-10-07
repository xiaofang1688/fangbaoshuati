from flask import Flask,render_template,request
# import tkinter as tk
# from tkinter import filedialog
import re,time,random,json

app = Flask(__name__)

class CustomFlask(Flask):
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
		variable_start_string='%%', 
		variable_end_string='%%',
	))

app = CustomFlask(__name__)

@app.route('/test',methods=["GET", "POST"])
def test():
	q= request.args.get("content")
	# root = tk.Tk()
	# root.withdraw()
	data=q.replace('．','.')
	# 不同题目分割
	pattern = re.compile(r'(?:^|\n\s*)\d+?[\.\。]')
	data = pattern.split(data)
	# 将每个题目分为题目、选项、答案
	result = []
	for i in data:
		pattern = re.compile(r'\n')
		# 题目
		title = pattern.split(i)[0]
		# 选项
		option = re.findall(r'[A-E][\.\。]?(.+?)\s+[\n]?', i)
		# 答案
		daan = re.findall(r'答案[:：]([A-E]+)[\n]?', i)
		analysis = ''
		if len(daan) == 0:
			daan = re.findall(r'答案[:：]([\s\S]+)', i)
			if len(daan):
				pattern = re.compile(r'解析[:：]')
				daanList=pattern.split(daan[0])
				if len(daanList)>1:
					analysis=daanList[1]
					daan=[daanList[0]]
		else:
			# 选择题获取解析
			jiexi = re.findall(r'解析[:：]([\s\S]+)', i)
			analysis = jiexi[0] if len(jiexi) else ''
		daan = daan[0] if len(daan) else ''

# 格式化成2016-03-20 11:45:39形式
		result.append({
			'id': time.strftime("%Y%m%d%H%M", time.localtime())+str(random.randint(0,1000000)),
			'title': title,
			'option': option,
			'answer': daan,
			'analysis': analysis
		})

	del(result[0])
	filename=time.strftime("%Y%m%d%H%M%S", time.localtime())+'.json'
	f = open("static/json/"+filename, 'w',encoding = 'utf-8')
	# print(result)
	f.write(json.dumps(result,ensure_ascii=False,indent = 4))
	f.close()
	print("执行完成")
	# print(data)	
	return filename

@app.route('/edit',methods=["GET", "POST"])
def edit():
	return render_template("edit.html")

@app.route('/edit1',methods=["GET", "POST"])
def edit1():
	return render_template("edit1.html")

@app.route('/getedit',methods=["GET", "POST"])
def getedit():
	con=request.args.get("content")
	with open('static/js/public.js','w',encoding = 'utf-8') as f:
		f.write(con)
	return "修改成功，请登录首页"


@app.route('/',methods=["GET", "POST"])
def index():
	return render_template("index.html")

@app.route('/tpye',methods=["GET", "POST"])
def type():
	return render_template("type.html")

@app.route('/timu',methods=["GET", "POST"])
def timu():
	return render_template("timu.html")

if __name__ == '__main__':
	app.run(debug=True)