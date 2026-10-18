from flask import Flask, request
import sqlite3
from pathlib import Path
app=Flask(__name__); DB=Path(__file__).with_name("challenge.db")
FLAG="FLAG{parameterize_every_query}"
def init():
    with sqlite3.connect(DB) as c:
        c.execute("CREATE TABLE IF NOT EXISTS assets(id INTEGER,name TEXT,owner TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS secrets(id INTEGER,name TEXT,value TEXT)")
        c.execute("DELETE FROM assets"); c.execute("DELETE FROM secrets")
        c.executemany("INSERT INTO assets VALUES(?,?,?)",[(1,"WS-014","Ops"),(2,"SRV-022","Infra")])
        c.execute("INSERT INTO secrets VALUES(1,'migration_note',?)",(FLAG,))
@app.route("/",methods=["GET","POST"])
def index():
    q=request.args.get("q",""); rows=[]; error=""
    if q:
        try:
            sql=f"SELECT id,name,owner FROM assets WHERE name LIKE '%{q}%'"
            with sqlite3.connect(DB) as c: rows=c.execute(sql).fetchall()
        except sqlite3.Error as e: error=str(e)
    out="<h1>Query Quake</h1><form><input name='q' placeholder='Asset search'><button>Search</button></form>"
    if error: out+="<p>"+error.replace("<","&lt;")+"</p>"
    if rows: out+="<pre>"+repr(rows)+"</pre>"
    out+="<form action='/submit' method='post'><input name='flag' placeholder='Submit flag'><button>Submit</button></form>"
    return out
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

if __name__=="__main__": init(); app.run(host="127.0.0.1",port=5003,debug=False)
