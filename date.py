DATE = 'prop("Date")'
NOW = "now()"

bases = {
    "milliseconds": {
        "between": f'dateBetween({DATE}, {NOW}, "milliseconds")',
        "modulo": 1000,
        "index": 0,
        "previous": None,
        "next": "seconds",
    },
    "seconds": {
        "between": f'dateBetween({DATE}, {NOW}, "seconds")',
        "modulo": 60,
        "index": 1,
        "previous": "milliseconds",
        "next": "minutes",
    },
    "minutes": {
        "between": f'dateBetween({DATE}, {NOW}, "minutes")',
        "modulo": 60,
        "index": 2,
        "previous": "seconds",
        "next": "hours",
    },
    "hours": {
        "between": f'dateBetween({DATE}, {NOW}, "hours")',
        "modulo": 24,
        "index": 3,
        "previous": "minutes",
        "next": "days",
    },
    "days": {
        "between": f'dateBetween({DATE}, {NOW}, "days")',
        "modulo": 7,
        "index": 4,
        "previous": "hours",
        "next": "weeks",
    },
    "weeks": {
        "between": f'dateBetween({DATE}, {NOW}, "weeks")',
        "modulo": 4,
        "index": 5,
        "previous": "days",
        "next": None,
    },
    "months": {
        "between": f'dateBetween({DATE}, {NOW}, "months")',
        "modulo": 12,
        "index": 6,
        "previous": "weeks",
        "next": "years",
    },
    "years": {
        "between": f'dateBetween({DATE}, {NOW}, "years")',
        "modulo": None,
        "index": 7,
        "previous": "months",
        "next": None,
    },
}


# Example: 15 minutes, 1 minute
def format(base, modulo=True):
    if modulo:
        return f'if({bases[base]["between"]} % {str(bases[base]["modulo"])} > 1, format({bases[base]["between"]} % {str(bases[base]["modulo"])}) + "&nbsp; {base}", "1 &nbsp; {base[:-1]}")'
    else:
        return f'if({bases[base]["between"]} > 1, format({bases[base]["between"]}) + " &nbsp; {base}", "1 &nbsp; {base[:-1]}")'


def format_raw(base):
    return f'format({bases[base]["between"]}) + "&nbsp; {base}"'


def handle_zero_one(base):
    if base == "weeks":
        return f'if({bases[base]["between"]} == 0, $NEXT$, if({bases[base]["between"]} == 1, if({bases["days"]["between"]} == 7, "1 &nbsp; {base[:-1]}", "1 &nbsp; {base[:-1]}, &nbsp;" + {format(bases[base]["previous"])}), {format(base)}))'
    if base == high:
        return f'if({bases[base]["between"]} == 0, $NEXT$, if({bases[base]["between"]} == 1, if({bases[bases[base]["previous"]]["between"]} == 0, "1 &nbsp; {base[:-1]}", "1 &nbsp; {base[:-1]}, &nbsp; " + {format(bases[base]["previous"])}), {format(base, modulo=False)}))'
    elif base == low:
        return f'if({bases[base]["between"]} == 0, "Due", if({bases[base]["between"]} == 1, "1 &nbsp; {base[:-1]}",{format_raw(base)}))'
    else:
        return f'if({bases[base]["between"]} == 0, $NEXT$, if({bases[base]["between"]} == 1, if({bases[bases[base]["previous"]]["between"]} == 0, "1 &nbsp; {base[:-1]}", "1 &nbsp; {base[:-1]}, &nbsp;" + {format(bases[base]["previous"])}), {format(base)}))'


high = "years"
low = "minutes"

exp = []

exp.append(f'if(empty({DATE}), "", $NEXT$)')

exp.append(f'if({bases[low]["between"]} < 0, "Due", $NEXT$)')

for base in list(bases.keys())[
    bases[low]["index"] : bases[high]["index"] + 1
].__reversed__():
    exp.append(handle_zero_one(base))

for i in range(len(exp) - 2, -1, -1):
    exp[i] = exp[i].replace("$NEXT$", exp[i + 1])

print(exp[0].replace(" ", "").replace("\n", "").replace("&nbsp;", " "))

# current minified version

# if(empty(prop("Date")),"",if(dateBetween(prop("Date"),now(),"minutes")<0,"Due",if(dateBetween(prop("Date"),now(),"years")==0,if(dateBetween(prop("Date"),now(),"months")==0,if(dateBetween(prop("Date"),now(),"weeks")==0,if(dateBetween(prop("Date"),now(),"days")==0,if(dateBetween(prop("Date"),now(),"hours")==0,if(dateBetween(prop("Date"),now(),"minutes")==0,"Due",if(dateBetween(prop("Date"),now(),"minutes")==1,"1 minute",format(dateBetween(prop("Date"),now(),"minutes"))+" minutes")),if(dateBetween(prop("Date"),now(),"hours")==1,if(dateBetween(prop("Date"),now(),"minutes")==0,"1 hour","1 hour, "+if(dateBetween(prop("Date"),now(),"minutes")%60>1,format(dateBetween(prop("Date"),now(),"minutes")%60)+" minutes","1 minute")),if(dateBetween(prop("Date"),now(),"hours")%24>1,format(dateBetween(prop("Date"),now(),"hours")%24)+" hours","1 hour"))),if(dateBetween(prop("Date"),now(),"days")==1,if(dateBetween(prop("Date"),now(),"hours")==0,"1 day","1 day, "+if(dateBetween(prop("Date"),now(),"hours")%24>1,format(dateBetween(prop("Date"),now(),"hours")%24)+" hours","1 hour")),if(dateBetween(prop("Date"),now(),"days")%7>1,format(dateBetween(prop("Date"),now(),"days")%7)+" days","1 day"))),if(dateBetween(prop("Date"),now(),"weeks")==1,if(dateBetween(prop("Date"),now(),"days")==7,"1 week","1 week, "+if(dateBetween(prop("Date"),now(),"days")%7>1,format(dateBetween(prop("Date"),now(),"days")%7)+" days","1 day")),if(dateBetween(prop("Date"),now(),"weeks")%4>1,format(dateBetween(prop("Date"),now(),"weeks")%4)+" weeks","1 week"))),if(dateBetween(prop("Date"),now(),"months")==1,if(dateBetween(prop("Date"),now(),"weeks")==0,"1 month","1 month, "+if(dateBetween(prop("Date"),now(),"weeks")%4>1,format(dateBetween(prop("Date"),now(),"weeks")%4)+" weeks","1 week")),if(dateBetween(prop("Date"),now(),"months")%12>1,format(dateBetween(prop("Date"),now(),"months")%12)+" months","1 month"))),if(dateBetween(prop("Date"),now(),"years")==1,if(dateBetween(prop("Date"),now(),"months")==0,"1 year","1 year, "+if(dateBetween(prop("Date"),now(),"months")%12>1,format(dateBetween(prop("Date"),now(),"months")%12)+" months","1 month")),if(dateBetween(prop("Date"),now(),"years")>1,format(dateBetween(prop("Date"),now(),"years"))+" years","1 year")))))
