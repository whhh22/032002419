from flask import Flask,render_template,request
from scapy.all import *
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login",methods=['POST'])
def login():
    yuzhi1 = request.form.get("yuzhi1")
    yuzhi2 = request.form.get("yuzhi2")

    dpkt = rdpcap(r"C:\Users\86157\Desktop\test.dep")
    vp = []
    vf = []
    strange = []
    c1 = 0
    c2 = 0
    c3 = 0
    dic1 = {}
    dic2 = {}
    length2 = 0
    for cnt in range(len(dpkt)):
        if dpkt[cnt][Ether].type !=2048:
            continue
        if dpkt[cnt][IP].proto == 6:
            proto = "TCP"
        elif dpkt[cnt][IP].proto ==17:
            proto = "UDP"
        else: continue
        ipSrc = dpkt[cnt][IP].src       #源IP
        sport = dpkt[cnt][proto].sport  #源端口号
        ipDst = dpkt[cnt][IP].dst       #目的IP
        dport = dpkt[cnt][proto].dport  #目的端口号
        length = len(dpkt[cnt])         #包长
        tup = (ipSrc,sport,ipDst,dport,proto)
        if length > eval(yuzhi1):
            strange.append(tup)
        counts = dic1.get(tup, 0)
        dic1[tup] = counts + length
        dic2[tup] = counts + 1
        c1 += 1
        length2 += length
        if c3 % 1000 != 0:
            vp[c2] = length2
            vf[c2] = c1
        else:
            c2 += 1
            vp.append(length2)
            vf.append(c1)
    return render_template("hello.html", K1=yuzhi1, K2=yuzhi2,p = vp, f = vf,strange = strange)


if __name__ == "__main__":
    app.run()