import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..database import RegistrateTable, Table, StatusOrder


class RegistrateTableRepository:
    def __init__(self, session: Session):
        self.__session: Session = session

    def add(self, entity: RegistrateTable) -> RegistrateTable | None:
        # try:
        self.__session.add(entity)
        self.__session.commit()
        return entity
        # except:
        #     self.__session.rollback()
        #     return None

    def get_list_registrate_table(self) -> list[RegistrateTable] | None:
        return self.__session.query(RegistrateTable).order_by(RegistrateTable.data_registrate).all()

    def get_list_registrate_table_by_state_order(self, state_reg: str) -> list[RegistrateTable] | None:

        return self.__session.query(RegistrateTable).where(RegistrateTable.status_registrate == state_reg).order_by(RegistrateTable.data_registrate).all()

    def get_by_uuid(self, uuid: str) -> RegistrateTable | None:
        return self.__session.query(RegistrateTable).filter(RegistrateTable.trace_id == uuid).first()

    def delete_registrate_table(self, entity: RegistrateTable):
        try:
            self.__session.delete(entity)
            self.__session.commit()
        except Exception:
            self.__session.rollback()

    def update(self, entity: RegistrateTable):
        try:
            self.__session.add(entity)
            self.__session.commit()
        except:
            self.__session.rollback()

    def get_list_tables(self, bakery_id: int) -> list[Table]:
        return self.__session.query(Table).where(Table.bakery_id == bakery_id).all()

    def get_reg_list_by_bakery_and_date(self, bakery_id: int, date: datetime.datetime) -> list[RegistrateTable]:
        return self.__session.query(RegistrateTable)\
            .where(RegistrateTable.bakery_id == bakery_id)\
            .where(RegistrateTable.data_registrate == date)\
            .where(RegistrateTable.status_registrate == StatusOrder.confirmed.name).all()

