"""Offline estimate of tool schema tokens, not billed model usage."""
import argparse, json
import tiktoken
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("catalog",type=Path,help="JSON object with mcp and utcp arrays of normalized model-facing tool definitions")
    p.add_argument("--encoding",default="o200k_base")
    p.add_argument("--selected",nargs="+",required=True)
    a=p.parse_args()
    enc=tiktoken.get_encoding(a.encoding)
    data=json.loads(a.catalog.read_text())
    def canonical(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)
    def count(x): return len(enc.encode(canonical(x)))
    def index(tools):
        result={t["function"]["name"]:t for t in tools}
        if len(result)!=len(tools): raise ValueError("Duplicate tool names")
        return result
    m,u=index(data["mcp"]),index(data["utcp"])
    if m!=u: raise ValueError("Model-facing catalogs differ; normalize before isolating selection effect")
    selected=set(a.selected)
    if not selected <= m.keys(): raise ValueError("Unknown selected tool")
    rows=[]
    for protocol,tools in [("MCP",m),("UTCP",u)]:
        for strategy in ["full","selected"]:
            subset=[tools[k] for k in sorted(tools) if strategy=="full" or k in selected]
            rows.append({"protocol":protocol,"strategy":strategy,"tools":len(subset),"estimated_schema_tokens":count(subset)})
    print(json.dumps({"measurement":"offline serialized schema estimate, not provider usage","encoding":a.encoding,"results":rows},indent=2))
if __name__=="__main__": main()
