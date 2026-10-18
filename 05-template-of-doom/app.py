from flask import Flask, request, render_template_string
app=Flask(__name__); app.config["CTF_FLAG"]="FLAG{templates_must_not_evaluate_user_input}"
@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST": return "Correct flag!" if request.form.get("flag","").strip()==app.config["CTF_FLAG"] else ("Incorrect flag",400)
    return '''<h1>Template of Doom</h1><form action="/preview"><input name="name" placeholder="Preview input"><button>Render</button></form>
    <form method="post"><input name="flag" placeholder="Submit flag"><button>Submit</button></form>'''
@app.route("/preview")
def preview():
    name=request.args.get("name","analyst")
    result=render_template_string("Preview for: "+name)
    return "<h1>Preview</h1><pre>"+result.replace("<","&lt;").replace(">","&gt;")+"</pre>"
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

if __name__=="__main__": app.run(host="127.0.0.1",port=5005,debug=False)
