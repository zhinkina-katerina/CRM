def edit_query_to_dict(quaery_set):
    parsed_set = list(quaery_set.values())
    result = {}

    for item in parsed_set:
        result[item['id']] = item
    return result