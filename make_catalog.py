import os, json
from datetime import datetime
from urllib.parse import quote

USER = "Esamarhb"
REPO = "docs"
BASE = f"https://{USER}.github.io/{REPO}/"
ROOT = "files"
CATS = {
    "students": "مستندات الطلاب",
    "teachers": "مستندات المعلمين",
    "admin": "المستندات الإدارية",
    "ministry": "المستندات الوزارية",
    "certificates": "الشهادات",
    "lists": "الكشوفات",
}
TYPES = {".pdf": "pdf", ".docx": "docx", ".doc": "doc",
         ".xlsx": "xlsx", ".xls": "xls"}

old = {}
if os.path.exists("catalog.json"):
    try:
        for d in json.load(open("catalog.json", encoding="utf-8"))["documents"]:
            old[d["path"]] = d
    except Exception:
        pass

docs, n = [], 0
for cat in CATS:
    folder = os.path.join(ROOT, cat)
    for dp, _, fs in os.walk(folder):
        for f in sorted(fs):
            ext = os.path.splitext(f)[1].lower()
            if ext not in TYPES:
                continue
            full = os.path.join(dp, f)
            rel = full.replace(os.sep, "/")
            n += 1
            p = old.get(rel, {})
            docs.append({
                "id": f"doc-{n:04d}",
                "title": p.get("title") or os.path.splitext(f)[0].replace("-", " ").replace("_", " "),
                "category": cat,
                "description": p.get("description", ""),
                "file_name": f,
                "path": rel,
                "url": BASE + quote(rel),
                "file_type": TYPES[ext],
                "size_mb": round(os.path.getsize(full) / 1048576, 2),
                "updated_at": datetime.fromtimestamp(os.path.getmtime(full)).strftime("%Y-%m-%d"),
            })

out = {
    "version": 1,
    "updated_at": datetime.now().strftime("%Y-%m-%d"),
    "categories": [{"id": k, "name": v} for k, v in CATS.items()],
    "documents": docs,
}
json.dump(out, open("catalog.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"تم: {len(docs)} مستند")
