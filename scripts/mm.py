#!/usr/bin/env python3
"""Tiny Mattermost helper for driving the Handover demo as a human teammate.

  MM_URL=http://localhost:8065 MM_USER=ada MM_PASS=... mm.py read  <channel> [n]
  MM_URL=...                    MM_USER=ada MM_PASS=... mm.py post  <channel> <message> [root_id]
"""
import json, os, sys, urllib.request

URL = os.environ.get("MM_URL", "http://localhost:8065").rstrip("/")
TEAM = os.environ.get("MM_TEAM", "switch")


def call(method, path, body=None, token=None):
    req = urllib.request.Request(URL + "/api/v4" + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"})
    if token:
        req.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(req) as res:
        return res.headers.get("Token"), json.loads(res.read() or "null")


def login():
    token, _ = call("POST", "/users/login", {"login_id": os.environ["MM_USER"], "password": os.environ["MM_PASS"]})
    return token


def channel_id(token, name):
    _, ch = call("GET", f"/teams/name/{TEAM}/channels/name/{name}", token=token)
    return ch["id"]


def main():
    cmd, channel = sys.argv[1], sys.argv[2]
    token = login()
    cid = channel_id(token, channel)
    if cmd == "read":
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 15
        _, users = None, {}
        _, posts = call("GET", f"/channels/{cid}/posts?per_page={n}", token=token)
        for pid in reversed(posts["order"]):
            p = posts["posts"][pid]
            uid = p["user_id"]
            if uid not in users:
                _, u = call("GET", f"/users/{uid}", token=token)
                users[uid] = u["username"]
            thread = f" (reply to {p['root_id'][:6]})" if p.get("root_id") else ""
            print(f"--- {pid[:6]} {users[uid]}{thread}\n{p['message']}")
    elif cmd == "post":
        body = {"channel_id": cid, "message": sys.argv[3]}
        if len(sys.argv) > 4:
            body["root_id"] = sys.argv[4]
        _, p = call("POST", "/posts", body, token=token)
        print(p["id"])


if __name__ == "__main__":
    main()
