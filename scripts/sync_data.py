#!/usr/bin/env python3
"""Fetch all 42 public ASI NIC-2008 tables. Exit nonzero on any failure."""
import concurrent.futures, json, pathlib, urllib.request, time, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; DATA.mkdir(exist_ok=True)
BASE="https://measure.thisindianlife.today/data/"
STATES="andaman-nicobar-islands andhra-pradesh arunachal-pradesh assam bihar chandigarh chattisgarh dadra-nagar-haveli dadra-nagar-havelli-and-daman-diu daman-diu delhi goa gujarat haryana himachal-pradesh jammu-kashmir jharkhand karnataka kerala ladakh lakshadweep madhya-pradesh maharashtra manipur meghalaya mizoram nagaland odisha puducherry punjab rajasthan sikkim tamil-nadu telangana tripura uttar-pradesh uttarakhand west-bengal".split()
FILES=["asi-nic2","asi-nic3","asi-nic4","asi-states-all"]+["asi-state-nic2-"+s for s in STATES]
DATES=[f"{y}-04-01" for y in range(2008,2024)]
def run(name):
    error=None
    for attempt in range(4):
        try:
            request=urllib.request.Request(BASE+name+".json",headers={"User-Agent":"IndiaIndustryAtlas/1.0"})
            with urllib.request.urlopen(request,timeout=90) as response: raw=response.read()
            obj=json.loads(raw)
            if obj.get("meta",{}).get("base")!="NIC 2008" or obj.get("dates")!=DATES or not isinstance(obj.get("series"),dict) or not obj["series"]:
                raise ValueError("Invalid year/base/series metadata")
            for key,s in obj["series"].items():
                if not isinstance(s.get("data"),list) or len(s["data"])!=16: raise ValueError("Invalid series "+key)
            (DATA/(name+".json")).write_bytes(raw)
            return name,len(obj["series"]),None
        except Exception as exc:
            error=str(exc);time.sleep(min(2**attempt,8))
    return name,0,error
if __name__=="__main__":
    print("Downloading",len(FILES),"published ASI tables",flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor: results=list(executor.map(run,FILES))
    failures=[(name,err) for name,_,err in results if err]
    print(json.dumps({"files":len(FILES),"downloaded":len(FILES)-len(failures),"series":sum(n for _,n,_ in results),"errors":failures},indent=2))
    if failures: sys.exit("Download incomplete: publication blocked")
