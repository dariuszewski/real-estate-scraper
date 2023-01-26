def feature_list(data):
    features = []
    for d in data:
        sec = d.get('security_types', [])
        e = d.get('extras_types', [])
        ex = d.get('equipment_types', [])
        lst = sec+e+ex
        for i in lst:
            features.append(i)
    return set(features)

#c