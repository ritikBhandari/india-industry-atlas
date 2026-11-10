#!/usr/bin/env python3
"""Fail publication unless 42 real tables cover the full period and 60k+ series."""
import json,pathlib,sys
from sync_data import FILES,DATA,DATES
errors=[];series=0;numeric=0;nulls=0;counts={}
for name in FILES:
    path=DATA/(name+".json")
    if not path.is_file():errors.append(name+": missing");continue
    try:
        o=json.loads(path.read_text())
        if o.get("meta",{}).get("base")!="NIC 2008" or o.get("meta",{}).get("mock") is True or o.get("dates")!=DATES: raise ValueError("invalid base, dates or mock data")
        d=o.get("series")
        if not isinstance(d,dict) or not d:raise ValueError("no series")
        for key,s in d.items():
            values=s.get("data")
            if not isinstance(values,list) or len(values)!=16:raise ValueError(key+" has invalid length")
            if not s.get("unit"):raise ValueError(key+" missing unit")
            for v in values:
                if v is None:nulls+=1
                elif isinstance(v,(int,float)) and not isinstance(v,bool):numeric+=1
                else:raise ValueError(key+" nonnumeric values")
        series+=len(d);counts[name]=len(d)
    except (ValueError,TypeError,OSError,AttributeError) as exc:errors.append(name+": "+str(exc))
if series<60000:errors.append("Series count "+str(series)+" below 60000")
report={"verified":not errors,"files_present":len(counts),"files_expected":42,"series":series,"numeric_observations":numeric,"missing_observations":nulls,"years":DATES,"errors":errors,"per_file":counts}
DATA.mkdir(exist_ok=True)
(DATA/"coverage-report.json").write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!="per_file"},indent=2))
if errors:sys.exit(1)
