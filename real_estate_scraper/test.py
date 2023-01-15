features = []
for d in data:
    sec = d['security_types']
    e = d['extras_types']
    ex = d['equipment_types']
    lst = sec+e+ex
    for i in lst:
        features.append(i)
