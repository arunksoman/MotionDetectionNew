import requests
import argparse
import sys

msg = {"msg": "success", "name_of_file": sys.argv[1]}
r = requests.post("http://127.0.0.1:5000/", json=msg)