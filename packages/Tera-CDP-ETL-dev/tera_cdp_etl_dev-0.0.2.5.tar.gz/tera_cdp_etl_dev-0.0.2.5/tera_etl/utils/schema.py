import json


def get_event_schema(data_source, event_name):
    if data_source == 'vtvcab':
        if event_name == 'init':
            return json.loads('''{
                        "additionalProperties": true,
                        "properties": {
                            "Birthday": {
                                "format": "date-time",
                                "type": "string"
                            },
                            "City": {
                                "type": "string"
                            },
                            "DateInserted": {
                                "format": "date-time",
                                "type": "string"
                            },
                            "District": {
                                "type": "string"
                            },
                            "EventId": {
                                "type": "string"
                            },
                            "Gender": {
                                "type": "string"
                            },
                            "NoOfStreet": {
                                "type": "string"
                            },
                            "OnboardingSource": {
                                "type": "string"
                            },
                            "PhoneNumber": {
                                "type": "string"
                            },
                            "Province": {
                                "type": "string"
                            },
                            "RegisterDate": {
                                "format": "date-time",
                                "type": "string"
                            },
                            "Status": {
                                "type": "string"
                            },
                            "StreetName": {
                                "type": "string"
                            },
                            "UserId": {
                                "type": "string"
                            },
                            "aa": {
                                "type": "integer"
                            },
                            "bb": {
                                "type": "number"
                            },
                            "cc": {
                                "type": "object",
                                "additionalProperties": true,
                                "properties": {
                                    "tt": {
                                        "type": "string"
                                    }
                                }
                            },
                            "dd": {
                                "type": "boolean"
                            }
                        },
                        "type": "object"
                    }
                    ''')
    return None
