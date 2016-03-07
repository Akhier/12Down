from uuid import uuid4
import ECS_Storage as S


class EntityManager:

    @classmethod
    def new_Id(self):
        nId = str(uuid4())
        S.Id.append(nId)
        return nId

    @classmethod
    def remove_Id(self, rId):
        S.Id.remove(rId)
