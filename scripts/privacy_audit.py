"""Fail CI if common secret or personal-data patterns enter the repository."""
from __future__ import annotations
import re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKIP={"privacy_audit.py"}
PATTERNS={
 "private_key":re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
 "cloud_token":re.compile(r"(?i)(?:api[_-]?key|secret|bearer|password)\s*[:=]\s*['\"][^'\"]{8,}"),
 "email":re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
 "windows_user_path":re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\\s]+"),
 "cloudflare_id":re.compile(r"(?i)\b[0-9a-f]{32}\b"),
}
ALLOW_EMAIL={"person@example.test"}
def files():
    try:
        names=subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True).splitlines()
    except Exception:
        names=[str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    return [ROOT/n for n in names if Path(n).name not in SKIP]
def main():
    hits=[]
    for path in files():
        if not path.exists() or path.suffix.lower() in {".png",".jpg",".xlsx"}: continue
        text=path.read_text(encoding="utf-8",errors="ignore")
        for name,rx in PATTERNS.items():
            for m in rx.finditer(text):
                if name=="email" and m.group(0) in ALLOW_EMAIL: continue
                hits.append((str(path.relative_to(ROOT)),name,m.start()))
    if hits:
        for p,n,pos in hits: print(f"{p}: {n} near character {pos}")
        raise SystemExit(1)
    print("privacy audit passed: no blocked patterns in repository files")
if __name__=="__main__": main()

