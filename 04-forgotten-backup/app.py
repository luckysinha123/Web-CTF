from flask import Flask, request, Response
app=Flask(__name__); FLAG="FLAG{forgotten_backups_leak_data}"
@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST": return "Correct flag!" if request.form.get("flag","").strip()==FLAG else ("Incorrect flag",400)
    return '''<h1>The Forgotten Backup</h1><p>Find the exposed legacy backup.</p>
    <form method="post"><input name="flag" placeholder="Submit flag"><button>Submit</button></form>'''
@app.route("/static/backups/legacy_config.bak")
def backup(): return Response("environment=training\nmigration_flag="+FLAG+"\n",mimetype="text/plain")
@app.after_request
def add_challenge_styles(response):
    if response.mimetype == "text/html":
        try:
            html = response.get_data(as_text=True)
            link = '<link rel="stylesheet" href="/static/style.css">'
            if link not in html:
                html = link + html
                response.set_data(html)
        except Exception:
            pass
    return response

if __name__=="__main__": app.run(host="127.0.0.1",port=5004,debug=False)
