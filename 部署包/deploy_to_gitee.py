import urllib.request, urllib.parse, json, os, sys, zipfile, io, base64

TOKEN = sys.argv[1] if len(sys.argv) > 1 else ""
if not TOKEN:
    print("请提供 Gitee 访问令牌")
    sys.exit(1)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_NAME = "wuren-kongjian"
USER_NAME = "xingyuan456"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0"
}

def api_call(method, path, data=None):
    url = f"https://gitee.com/api/v5/{path}"
    req = urllib.request.Request(url, method=method)
    for k, v in HEADERS.items():
        req.add_header(k, v)
    if data:
        req.data = json.dumps(data).encode()
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read()) if resp.read() else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  API Error {e.code}: {body[:200]}")
        return None

print("1. 创建仓库...")
result = api_call("POST", "user/repos", {
    "name": REPO_NAME,
    "description": "五人拼图协作空间",
    "public": "true"
})
if not result:
    print("   仓库已存在，尝试直接上传文件...")
    result = api_call("GET", f"repos/{USER_NAME}/{REPO_NAME}")

if not result:
    print("   无法创建仓库，请检查令牌权限")
    sys.exit(1)

print(f"   仓库: {result.get('html_url', 'unknown')}")

print("2. 上传文件...")
files_to_upload = []
for root, dirs, files in os.walk(PROJECT_DIR):
    for fname in files:
        if fname.endswith(".py") or fname.endswith(".bat") or fname == "deploy_to_gitee.py":
            continue
        fpath = os.path.join(root, fname)
        relpath = os.path.relpath(fpath, PROJECT_DIR)
        with open(fpath, "rb") as f:
            content = f.read()
        files_to_upload.append({"path": relpath, "content": base64.b64encode(content).decode()})

# Create or update files via API
for i, f in enumerate(files_to_upload):
    print(f"   [{i+1}/{len(files_to_upload)}] {f['path']}")
    result = api_call("POST", f"repos/{USER_NAME}/{REPO_NAME}/contents/{f['path']}", {
        "content": f["content"],
        "message": f"Add {f['path']}",
        "branch": "master"
    })
    if not result:
        print(f"   上传失败，尝试更新...")
        api_call("PUT", f"repos/{USER_NAME}/{REPO_NAME}/contents/{f['path']}", {
            "content": f["content"],
            "message": f"Update {f['path']}",
            "branch": "master"
        })

print("3. 开启 Gitee Pages...")
# Gitee Pages API - try to enable
try:
    pages_data = json.dumps({
        "domain": f"{USER_NAME}.gitee.io",
        "branch": "master",
        "directory": "/"
    }).encode()
    req = urllib.request.Request(
        f"https://gitee.com/api/v5/repos/{USER_NAME}/{REPO_NAME}/pages",
        data=pages_data, method="POST"
    )
    for k, v in HEADERS.items():
        req.add_header(k, v)
    resp = urllib.request.urlopen(req, timeout=30)
    print("   Gitee Pages 开启成功!")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    if "already" in body.lower():
        print("   Pages 已经开启")
    else:
        print(f"   需要手动开启 Pages: {e.code}")
        print(f"   请访问仓库 Settings → Pages 页面手动开启")

print(f"\n✅ 完成!")
print(f"访问地址: https://{USER_NAME}.gitee.io/{REPO_NAME}")
