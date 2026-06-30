import urllib.request, json, io, zipfile, os, uuid

project_dir = "D:\\workspace\\五人协作"
with open(os.path.join(project_dir, "index.html"), "rb") as f:
    html_content = f.read()
print(f"index.html: {len(html_content)} bytes")

uuid_str = str(uuid.uuid4()).replace("-", "")
boundary = "----" + uuid_str

video_path = os.path.join(project_dir, "samoyed.mp4")
total_zip = io.BytesIO()
with zipfile.ZipFile(total_zip, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            fp = os.path.join(root, file)
            arcname = os.path.relpath(fp, project_dir)
            if file.endswith(".py"):
                continue
            zf.write(fp, arcname)
total_zip.seek(0)
print(f"Project zip: {len(total_zip.read())} bytes")
print("Ready. Now trying deployment...")

# Strategy: Use Gitee API with password auth
# First get an access token
import urllib.parse

login_data = urllib.parse.urlencode({
    "user[login]": "xingyuan456",
    "user[password]": "xuhao123"
}).encode()

from http.cookiejar import CookieJar
from urllib.request import HTTPCookieProcessor, build_opener

cj = CookieJar()
opener = build_opener(HTTPCookieProcessor(cj))

req = urllib.request.Request("https://gitee.com/login",
    data=login_data, method="POST")
req.add_header("Content-Type", "application/x-www-form-urlencoded")
req.add_header("User-Agent", "Mozilla/5.0")
resp = opener.open(req, timeout=15)
print(f"Login: {resp.status}")

# Check if logged in
req2 = urllib.request.Request("https://gitee.com/api/v5/user")
req2.add_header("User-Agent", "Mozilla/5.0")
resp2 = opener.open(req2, timeout=10)
user_data = json.loads(resp2.read())
print(f"User: {user_data.get('login')} (id: {user_data.get('id')})")

# Create repo via web form
# First get the new project page for CSRF
req3 = urllib.request.Request("https://gitee.com/projects/new")
req3.add_header("User-Agent", "Mozilla/5.0")
resp3 = opener.open(req3, timeout=15)
html = resp3.read().decode("utf-8", errors="replace")

import re
auth_match = re.search(r'name="authenticity_token"[^>]*value="([^"]+)"', html)
auth_token = auth_match.group(1) if auth_match else ""
print(f"Auth token: {auth_token[:30]}...")

# Create repo
create_data = urllib.parse.urlencode({
    "project[name]": "wuren-kongjian",
    "project[path]": "wuren-kongjian",
    "project[description]": "五人拼图协作空间 - 许灏/赵恩京/袁淑星/孙铭瑞/赵淑雅",
    "project[visibility_level]": "0",
    "authenticity_token": auth_token
}).encode()

try:
    req4 = urllib.request.Request("https://gitee.com/projects",
        data=create_data, method="POST")
    req4.add_header("Content-Type", "application/x-www-form-urlencoded")
    req4.add_header("User-Agent", "Mozilla/5.0")
    resp4 = opener.open(req4, timeout=15)
    print(f"Create repo: {resp4.status}")
    print(f"Repo URL: {resp4.url}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Error {e.code}")
    if "already" in body.lower():
        print("Repo already exists! Going to update files...")
        repo_url = "https://gitee.com/xingyuan456/wuren-kongjian"
    else:
        print(body[:500])
        repo_url = None

print(f"\nDone! Repo at: {repo_url if 'repo_url' in dir() else 'unknown'}")
