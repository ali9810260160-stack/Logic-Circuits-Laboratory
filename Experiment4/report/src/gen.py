# -*- coding: utf-8 -*-
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import svgs
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tpl = open(os.path.join(D, "src", "report.tpl.html"), encoding="utf-8").read()
t0, t1 = svgs.tbl_shift_right()
vals = {k: f() for k, f in svgs.ALL.items()}
vals["TBL_SHIFT0"], vals["TBL_SHIFT1"] = t0, t1
for k, v in vals.items():
    tpl = tpl.replace(f"%%{k}%%", v)
assert "%%" not in tpl, re.findall(r"%%\w+%%", tpl)
head, js = tpl.split("<script>", 1)
head = re.sub(r"\[\[(.+?)\]\]", lambda m: f"<span class='en'>{m.group(1)}</span>", head)
head = re.sub(r"\{\{(.+?)\}\}", lambda m: f"<span class='bin'>{m.group(1)}</span>", head)
out = head + "<script>" + js
open(os.path.join(D, "report.html"), "w", encoding="utf-8").write(out)
print("ok", len(out))
