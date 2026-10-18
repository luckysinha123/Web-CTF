from flask import Flask, request, make_response
app=Flask(__name__)
FLAG="FLAG{client_side_roles_are_not_authorization}"
@app.route("/")
def index():
    return '''<h1>Cookie Crumbs</h1><p>Inspect the role cookie and open /panel.</p>
    <form action="/submit" method="post"><input name="flag" placeholder="Submit flag"><button>Submit</button></form>'''
@app.route("/panel")
def panel():
    if request.cookies.get("role")=="admin": return "<h1>Internal panel</h1><p>"+FLAG+"</p>"
    r=make_response("<h1>Access denied</h1><p>Role required.</p>",403); r.set_cookie("role","guest"); return r
@app.route("/submit",methods=["POST"])
def submit():
    return ("Correct flag!" if request.form.get("flag","").strip()==FLAG else "Incorrect flag",200 if request.form.get("flag","").strip()==FLAG else 400)
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

if __name__=="__main__": app.run(host="127.0.0.1",port=5002,debug=False)
