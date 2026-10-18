from flask import Flask, request, jsonify, make_response
app=Flask(__name__); FLAG="FLAG{authorize_every_object_access}"
CASES={1001:{"id":1001,"owner":"analyst","title":"Suspicious login","details":"Review test logins."},1002:{"id":1002,"owner":"director","title":"Restricted incident","details":FLAG}}
@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST": return "Correct flag!" if request.form.get("flag","").strip()==FLAG else ("Incorrect flag",400)
    return '''<h1>Zero Trust</h1><p><a href="/login">Sign in as demo analyst</a></p>
    <p>Compare /api/cases/1001 and /api/cases/1002.</p>
    <form method="post"><input name="flag" placeholder="Submit flag"><button>Submit</button></form>'''
@app.route("/login")
def login():
    r=make_response("<h1>Signed in as analyst</h1><p>Now inspect /api/cases/1001 and /api/cases/1002.</p>")
    r.set_cookie("lab_user","analyst",httponly=True,samesite="Lax"); return r
@app.route("/api/cases/<int:case_id>")
def get_case(case_id):
    if request.cookies.get("lab_user")!="analyst": return jsonify({"error":"authentication_required"}),401
    if case_id not in CASES: return jsonify({"error":"not_found"}),404
    return jsonify(CASES[case_id]) # intentionally missing object-level authorization
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

if __name__=="__main__": app.run(host="127.0.0.1",port=5006,debug=False)
