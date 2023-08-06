from tera_etl.utils.normalise_utils import assign_to_event, clean_phone_field


def normalise_data(datas, schema_name) -> dict:
    normalised_data = __normalise(datas, schema_name)
    return normalised_data if normalised_data else datas


def __normalise(datas, schema_name):
    result = []
    if schema_name == "UserProfileSchema":
        for data in datas:
            for key, value in data.items():
                if key in ["HomePhone", "WorkPhone"]:
                    assign_to_event(data, key, clean_phone_field(value))
                else:
                    assign_to_event(data, key, value)
            result.append(data)
    if schema_name == "UserWatchVideoSchema":
        for data in datas:
            for key, value in data.items():
                assign_to_event(data, key, value)
            result.append(data)
    return result
