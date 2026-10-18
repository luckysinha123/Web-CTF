from flask import Flask, request
app=Flask(__name__)
FLAG="FLAG{source_maps_reveal_secrets}"
@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="POST":
        return "Correct flag!" if request.form.get("flag","").strip()==FLAG else ("Incorrect flag",400)
    return '''<h1>View From the Shadows</h1><p>Support portal operational.</p>
    <!-- Exposed test token: FLAG{source_maps_reveal_secrets} -->
    <form method="post"><input name="flag" placeholder="Submit flag"><button>Submit</button></form>'''
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

if __name__=="__main__": app.run(host="127.0.0.1",port=5001,debug=False)
