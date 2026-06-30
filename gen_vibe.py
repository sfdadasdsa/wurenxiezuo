import json
with open("D:/workspace/五人协作/data.json","r",encoding="utf-8") as f:
    d = json.load(f)
MS, WP, TN, DW, CL = d["MS"], d["WP"], d["TN"], d["DW"], d["CL"]

cards = []
for i,m in enumerate(MS):
    deg = i*72
    cards.append("<div class=card data-id=\""+m["id"]+"\" style=\"--deg:"+str(deg)+";--clr:"+CL[i]+"\"><div class=card-avatar id=av-"+m["id"]+">"+m["name"][0]+"</div><div class=card-name>"+m["name"]+"</div><div class=card-role>"+(m["role"].split("与")[0] if "与" in m["role"] else m["role"][:4])+"</div></div>")

wp_opts = []
for w in WP:
    cols = ",".join(w["c"])
    wp_opts.append("<div class=wo data-cols=\""+cols+"\" style=\"background:linear-gradient(135deg,"+cols+")\"><span class=wn>"+w["n"]+"</span></div>")

wp_types = ["<button class=ft data-id=all>\u5168\u90e8</button>"]
for t,tn in TN.items():
    wp_types.append("<button class=ft data-id="+t+">"+tn+"</button>")

cards_html = "".join(cards)
wp_opts_html = "".join(wp_opts)
wp_types_html = "".join(wp_types)

MS_JSON = json.dumps(MS, ensure_ascii=False)
WP_JSON = json.dumps(WP, ensure_ascii=False)
TN_JSON = json.dumps(TN, ensure_ascii=False)
DW_JSON = json.dumps(DW, ensure_ascii=False)

with open("D:/workspace/五人协作/template.html","r",encoding="utf-8") as f:
    tpl = f.read()

html = tpl
html = html.replace("{{CARDS}}", cards_html)
html = html.replace("{{WP_OPTS}}", wp_opts_html)
html = html.replace("{{WP_TYPES}}", wp_types_html)
html = html.replace("{{MS_JSON}}", MS_JSON)
html = html.replace("{{WP_JSON}}", WP_JSON)
html = html.replace("{{TN_JSON}}", TN_JSON)
html = html.replace("{{DW_JSON}}", DW_JSON)
html = html.replace("{{DW0}}", DW[0])
html = html.replace("{{DW1}}", DW[1])
html = html.replace("{{DW2}}", DW[2])

with open("D:/workspace/五人协作/index.html","w",encoding="utf-8") as f:
    f.write(html)
print("DONE!", len(html), "bytes")
