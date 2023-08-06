from nsj_rest_lib.dao.dao_base import DAOBase
from nsj_gcf_utils.db_adapter2 import DBAdapter2
from nsj_rest_lib.entity.entity_base import EntityBase
from nsj_rest_lib.exception import NotFoundException


class DatabaseDAO(DAOBase):
    def __init__(self, db: DBAdapter2, entity_class: EntityBase):
        super().__init__(db, entity_class)
    
    def get_by_tenant(self, tenant):
        sql = """
            select host, porta, nome
            from multibanco.database
            where tenant = :tenant;
        """

        # Running query
        resp = self._db.execute_query(
            sql,
            tenant=tenant
        )

        if len(resp) <= 0:
            raise NotFoundException(
                f'Não foi encontrado um usuário vinculado à Conta Nasajon')
        
        return resp[0]