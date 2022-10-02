"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""

from wallet_friend_entities.Entities import updated_base
from sqlalchemy import create_engine

# Warning!: Run only once when you need to create the DB.
db_string = "postgresql://e89db34874f8a3e18aff2c149d35eed83b50bcce294983021855fd751a7" \
            ":57dc776594d12466b45b1765c001fb390cecd0ba03f91506b00d7a2e42e@localhost:5432" \
            "/d453b9b4c616f9899e4fa08a8f726cbcbbc1b898318b62d2c5af23098c57"


db = create_engine(db_string)
updated_base.metadata.drop_all(bind=db)
updated_base.metadata.create_all(db, updated_base.metadata.tables.values())
