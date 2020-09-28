import json
with open('brainly.json') as f:
    # load json objects to dictionaries
    jsons = map(json.loads, f)
    result = list()
    items_set = set()

    for js in jsons:
        for data in js:
        # only add unseen items (referring to 'title' as key)
            if not data['url'] in items_set:
                # mark as seen
                items_set.add(data['url'])
                # add to results
                result.append(data)

# write to new json file
with open('new_file.json' ,'w') as nf:
    json.dump(result, nf)

print(result)