from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                      Relationship, RelationshipTo)


class Account(StructuredNode):
    profile_id = IntegerProperty(unique_index=True)
    name = StringProperty(required=True)
    profile_picture = StringProperty(required=True)
    profile_link = StringProperty(required=True)

    tag_line = StringProperty()
    education = StringProperty()
    work = StringProperty()
    about = StringProperty()

    friends = RelationshipTo("Account", "friends_with")

    @staticmethod
    def from_scraped(data):
        return Account(profile_id=data['id'], name=data['Name'],
                       profile_picture=data['profile_picture'], profile_link="", tag_line=data.get('tagline'),
                       education=data.get('Education'), work=data.get('Work'), about=data.get('About'))

    @staticmethod
    def from_friends(data):
        return Account(profile_id=data['id'], name=data['name'],
                       profile_picture=data['profile_picture'],
                       profile_link=data['link'])

    @classmethod
    def category(cls):
        pass
