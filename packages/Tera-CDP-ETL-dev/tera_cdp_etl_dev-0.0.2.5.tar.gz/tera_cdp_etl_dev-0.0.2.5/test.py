import json


# from tera_etl import quality_control as qc
# schema = {
#     "UserId" : "int",
#     "HomePhone" : "string",
#     "WorkPhone" : ["string", "null"],
#     "Address" : {
#         "HouseNo": "string",
#         "Streetname": "string",
#         "Ward": "string",
#         "District": "string",
#         "Province": "string",
#         "Country": "string"
#     },
#     "Firstname" : "string",
#     "Lastname" : "string",
#     "Gender" : "string",
#     "RegisterDate" : "datetime",
#     "Status" : "string",
#     "DataSource" : "string",
#     "Source" : "string",
#     "EventId" : "string"
# }
# data = {
#     "UserId": 202201439424,
#     "HomePhone": "0912919543",
#     "WorkPhone": None,""
#     "Address": {
#         "HouseNo": "",
#         "Streetname": "",
#         "Ward": "ẤP HÒA CƯỜNG, Xã Minh Hoà",
#         "District": "Huyện Dầu Tiếng",
#         "Province": "Tỉnh Bình Dương",
#         "Country": "Việt Nam"
#     },
#     "Firstname": "TRẦN VĂN ",
#     "Lastname": "TÙNG",
#     "Gender": "Male",
#     "RegisterDate": "2022-01-01T00:00:00.00Z",
#     "Status": "True",
#     "DataSource": "VTVHyundai",
#     "Source": "VTVHyundai",
#     "EventId": "VTVHyundai_IngestProfile_202201439424"
# }


# from tera_etl import quality_control as qc
# structures = {
#     "Fields": [
#       {"Name": "UserId", "FieldType": "string", "Validation": "String,MustHave", "Comment": "id của user trong hệ thống, phải là kiểu string" },
#       {"Name": "HomePhone", "FieldType": ["string", "null"], "Comment": "Nếu không có thì để trống" },
#       {"Name": "WorkPhone", "FieldType": ["string", "null"], "Comment": "Nếu không có thì để trống" },
#       {"Name": "AddrHouseNo", "FieldType": "string", "Comment": "Số nhà" },
#       {"Name": "AddrStreetName", "FieldType": "string", "Comment": "Tên đường" },
#       {"Name": "AddrWard", "FieldType": "string", "Comment": "Phường / Xã" },
#       {"Name": "AddrDistrict", "FieldType": "string", "Comment": "Quận / Huyện / Thành Phố trực thuộc tỉnh" },
#       {"Name": "AddrProvince", "FieldType": "string", "Comment": "Tỉnh / Thành phố trực thuộc TW" },
#       {"Name": "AddrCountry", "FieldType": "string", "Validation": "Iso Country Code", "Comment": "Tên nước - ISO Country Code - E.g. VN" },
#       {"Name": "Firstname", "FieldType": "string", "Comment": "Tên" },
#       {"Name": "Lastname", "FieldType": "string", "Comment": "Họ và chữ lót" },
#       {"Name": "Gender", "FieldType": "string", "Comment": "Giới tính, tiếng anh, để khỏi bị nhầm lẫn", "Validation": "Male/Female/Other" },
#       {"Name": "RegisterDate", "FieldType": "datetime", "Comment": "Ngày đăng ký vào hệ thống" },
#       {"Name": "DataSource", "FieldType": "string", "Comment": "DataProviderName" },
#       {"Name": "MaritalStatus", "FieldType": "string", "Comment": "Tình trạng hôn nhân", "Validation": "Single/Married" }
#     ]
#   }
# data = {
#     "UserId": "202201439260",
#     "HomePhone": "0369841490",
#     "WorkPhone": None,
#     "AddrHouseNo": "",
#     "AddrStreetName": "",
#     "AddrWard": "15 NGÕ 341, Phường Xuân Phương",
#     "AddrDistrict": "Quận Nam Từ Liêm",
#     "AddrProvince": "Thành phố Hà Nội",
#     "AddrCountry": "Việt Nam",
#     "Firstname": "NGUYỄN THỊ BÍCH ",
#     "Lastname": "HIỀN",
#     "Gender": "Female",
#     "RegisterDate": "2022-01-01T00:00:00.00Z",
#     "DataSource": "VTVHyundai",
#     "MaritalStatus": "Single"
# }
# schema = {
#     'UserId': 'string',
#     'HomePhone': ['string', 'null'],
#     'WorkPhone': ['string', 'null'],
#     'AddrHouseNo': 'string',
#     "AddrStreetName": "string",
#     'AddrWard': 'string',
#     'AddrDistrict': 'string',
#     'AddrProvince': 'string',
#     'AddrCountry': 'string',
#     'Firstname': 'string',
#     'Lastname': 'string',
#     'Gender': 'string',
#     'RegisterDate': 'datetime',
#     'DataSource': 'string',
#     'MaritalStatus': 'string'
# }

# schema_dict={}
# for field in structures["Fields"]:
#     schema_dict[field["Name"]] = field["FieldType"]
# print(schema_dict)
# qc_type = qc.classify_data(data_chunk=data, schema=schema)
# print(qc_type)
# print("AddrStreetName" not in schema.keys())
# for field in data:
#     if field not in list(schema.keys()):
#         print(list(schema.keys()))
#         print(field)

# import json
# f = open("data.json")
# datas = json.load(f)
# f.close()
# for data in datas:
#     # print(data)
#     qc_result = qc.classify_data(data_chunk=data, schema=schema)
#     if qc_result["qc_type"] == qc.QualityControlResult.ACCEPTED:
#         # print(qc_result["qc_type"])
#         pass
#     else:
#         print(qc_result["errors"])

# schema = {
#     'UserId': 'string',
#     'HomePhone': ['string', 'null'],
#     'WorkPhone': ['string', 'null'],
#     'AddrHouseNo': 'string',
#     "AddrStreetName": "string",
#     'AddrWard': 'string',
#     'AddrDistrict': 'string',
#     'AddrProvince': 'string',
#     'AddrCountry': 'string',
#     'Firstname': 'string',
#     'Lastname': 'string',
#     'Gender': 'string',
#     'RegisterDate': 'datetime',
#     'DataSource': 'string',
#     'MaritalStatus': 'string'
# }

# from marshmallow import Schema, fields, validate
# from marshmallow.validate import Regexp, Length, OneOf

# from tera_etl import quality_control as qc

# data = {
#     "UserId": "202201439260",
#     "HomePhone": "0369841490",
#     "WorkPhone": None,
#     "AddrHouseNo": "",
#     "AddrStreetName": "",
#     "AddrWard": "15 NGÕ 341, Phường Xuân Phương",
#     "AddrDistrict": "Quận Nam Từ Liêm",
#     "AddrProvince": "Thành phố Hà Nội",
#     "AddrCountry": "Việt Nam",
#     "Firstname": "NGUYỄN THỊ BÍCH ",
#     "Lastname": "HIỀN",
#     "Gender": "Female",
#     "RegisterDate": "2022-01-01T00:00:00.00Z",
#     "DataSource": "VTVHyundai",
#     "MaritalStatus": "Single"
# }

# class UserProfileSchema(Schema):
#     UserId = fields.String(required=True)
#     HomePhone = fields.String(allow_none=True)
#     WorkPhone = fields.String(allow_none=True)
#     AddrHouseNo = fields.String()
#     AddrStreetName = fields.String()
#     AddrWard = fields.String()
#     AddrDistrict = fields.String()
#     AddrProvince = fields.String()
#     AddrCountry = fields.String()
#     Firstname = fields.String()
#     Lastname = fields.String()
#     Gender = fields.String(
#         validate=[
#             validate.OneOf(["Male", "Female", "Other"])
#         ]
#     )
#     RegisterDate = fields.String()
#     DataSource = fields.String()
#     MaritalStatus = fields.String(
#         validate=[
#             validate.OneOf(["Single", "Married"])
#         ]
#     )


# import json
# f = open("data.json")
# datas = json.load(f)
# f.close()
# # userProfileSchema = UserProfileSchema(many=True)
# for data in datas:
#     a = qc.classify_data(data_chunk=data,schema_name="UserProfileSchema")
#     if a["qc_type"] != qc.QualityControlResult.ACCEPTED:
#         print(a)

#     errors = userProfileSchema.validate(data)
#     if errors:
#         print(data)
# print(errors.keys())

    # UserId = fields.Str(required=True)
    # HomePhone = fields.Str(required=False)
    # WorkPhone = fields.Str(required=False)
    # AddrHouseNo = fields.Str(required=True)
    # AddrStreetName = fields.Str(required=True)
    # AddrWard = fields.Str(required=True)
    # AddrDistrict = fields.Str(required=True)
    # AddrProvince = fields.Str(required=True)
    # AddrCountry = fields.Str(required=True)
    # Firstname = fields.Str(required=True)
    # Lastname = fields.Str(required=True)
    # Gender = fields.Str(
    #     required=True,
    #     validate=[
    #         OneOf(choices=["Male","Female", "Other"])
    #     ]
    # )
    # RegisterDate = fields.Str(required=True)
    # DataSource = fields.Str(required=True)
    # MaritalStatus = fields.Str(
    #     required=True,
    #     validate=[
    #         OneOf(choices=["Single", "Married"])
    #     ]
    # )
# print(globals())

# f = open("profile_ontv.json")
# vtvcabcrm = json.load(f)
# f.close()
# res = []
# print(len(vtvcabcrm))
# for idx, profile in  enumerate(vtvcabcrm):
#     print(f'PROGRESS {idx}')
#     try:
#         profile['UserId'] = profile.pop('CrmId')
#         profile['HomePhone'] = profile.pop('Phone') if 'Phone' in profile else ''
#         profile['WorkPhone'] = None
#         profile['AddrHouseNo'] = profile.pop('HouseNo') if 'HouseNo' in profile else ''
#         profile['AddrStreetName'] = profile.pop('Street') if 'Street' in profile else ''
#         profile['AddrWard'] = profile.pop('Area') if 'Area' in profile else ''
#         profile['AddrDistrict'] = profile.pop('District') if 'District' in profile else ''
#         profile['AddrProvince'] = profile.pop('City') if 'City' in profile else ''
#         profile['AddrCountry'] = profile.pop('Country') if 'Country' in profile else 'Việt Nam'
#         profile['Firstname'] = profile.pop('FirstName') if 'FirstName' in profile else ''
#         profile['Lastname'] = profile.pop('LastName') if 'LastName' in profile else ''
#         profile['RegisterDate'] = '2022-01-01T00:00:00.00Z'
#         if 'Gender' in profile:
#             if profile['Gender'] == 'Nam':
#                 profile['Gender'] = 'Male'
#             if profile['Gender'] == 'Nữ':
#                 profile['Gender'] = 'Female'
#         else:
#             profile['Gender'] = 'Not Define'
#         profile['DataSource'] = profile.pop('DataSource') if 'DataSource' in profile else ''
#         profile['MaritalStatus'] = 'Single'
#         if 'PhoneId' in profile: del profile['PhoneId']
#         if 'FullAddress' in profile: del profile['FullAddress']
#         if 'DOB' in profile: del profile['DOB']
#         if 'MOB' in profile: del profile['MOB']
#         if 'YOB' in profile: del profile['YOB']
#         if 'Birthday' in profile: del profile['Birthday']
#         res.append(profile)
#     except Exception as e:
#         print(e)
#         print(profile)
#         break
import sys
f = open("/Users/mac/Desktop/data_formated.json")
data = json.load(f)
f.close()
# with open('/Users/mac/Desktop/data_formated_500000.json', 'w') as f:
#     json.dump(data[:500000], f, indent=4, default=str, ensure_ascii=False)

import uuid
# Define the maximum size for each DynamoDB record in bytes (400KB)
MAX_RECORD_SIZE = 400000
my_list = data[:50000]
# Split the list of dictionaries into multiple smaller ones
partition_key = str(uuid.uuid4())  # Generate a random partition key
records = []
current_record = {'partition_key': partition_key}
group_records = []
for idx, my_dict in enumerate(my_list):
    current_group_size = sys.getsizeof(group_records)
    if current_group_size < MAX_RECORD_SIZE:
        group_records.append(my_dict)
    else:
        records.append(group_records)
        group_records = [my_dict]
    
    if idx == (len(my_list) - 1) and group_records:
        records.append(group_records)
total = 0
for i, record in enumerate(records):
    total += len(record)
    print(f"Record {i+1} Length:{len(record)}")
print(f'Total: {total}')
