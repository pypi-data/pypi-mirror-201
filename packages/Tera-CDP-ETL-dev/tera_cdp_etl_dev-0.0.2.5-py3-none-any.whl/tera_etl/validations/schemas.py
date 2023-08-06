from marshmallow import Schema, fields, validate


class UserProfileSchema(Schema):
    UserId = fields.String(required=True)
    HomePhone = fields.String(allow_none=True)
    WorkPhone = fields.String(allow_none=True)
    AddrHouseNo = fields.String()
    AddrStreetName = fields.String()
    AddrWard = fields.String()
    AddrDistrict = fields.String()
    AddrProvince = fields.String()
    AddrCountry = fields.String()
    Firstname = fields.String()
    Lastname = fields.String()
    Gender = fields.String(
        validate=[
            validate.OneOf(["Male", "Female", "Other"])
        ]
    )
    RegisterDate = fields.DateTime()
    DataSource = fields.String()
    MaritalStatus = fields.String(
        validate=[
            validate.OneOf(["Single", "Married"])
        ]
    )


class UserWatchVideoSchema(Schema):
    VODId = fields.String(required=True)
    DeviceId = fields.String(required=True)
    DurationWatched =  fields.Integer()
    VODNameWatched = fields.String()
    Tag = fields.String()
    Category = fields.String()
