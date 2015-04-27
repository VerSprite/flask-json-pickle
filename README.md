# flask-json-pickle
This is a vulnerable Flask web application that calls loads() from jsonpickle on untrusted data through HTTP cookies.  This vulnerability allows an attacker to create a malicious pickle, encode it with jsonpickle, and send it to the web application to exploit the vulnerability.
