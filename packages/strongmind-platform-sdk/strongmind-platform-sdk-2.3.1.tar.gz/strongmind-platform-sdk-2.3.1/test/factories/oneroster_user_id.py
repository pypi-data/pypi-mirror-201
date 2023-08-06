from oneroster_client.models.user_id_type import UserIdType
from factory import Factory, Faker


class OneRosterUserIdFactory(Factory):
    class Meta:
        model = UserIdType

    type = Faker('word')
    identifier = Faker('uuid4')
