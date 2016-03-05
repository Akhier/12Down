from uuid import uuid4
import config


class EntityManager:

    @classmethod
    def new_Id(self):
        nId = str(uuid4())
        config.Id.append(nId)
        return nId

    @classmethod
    def remove_Id(self, rId):
        config.Id.remove(rId)
