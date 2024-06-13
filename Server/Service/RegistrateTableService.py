import datetime

from ..Repository import RegistrateTableRepository
from ..database import db, RegistrateTable, Table
from ..Models import OrderViewAdmin


class RegistrateTableService:
    def __init__(self):
        self.__repository: RegistrateTableRepository = RegistrateTableRepository(db.session)

    def converter_min_to_time(self, minute: int) -> str:
        hour = minute // 60
        min = minute - 60 * hour
        return "{:02d}:{:02d}".format(hour, min)

    def add_registrate_table(self, entity: RegistrateTable):
        self.__repository.add(entity)

    def get_list_reg_by_status_registrate(self, state_order: str) -> list[RegistrateTable]:
        list_entity = self.__repository.get_list_registrate_table_by_state_order(state_order)
        return list_entity

    def get_reg_by_uuid(self, uuid: str) -> RegistrateTable:
        entity = self.__repository.get_by_uuid(uuid)
        return entity

    def get_tables_list(self, bakery_id: int) -> list[Table]:
        return self.__repository.get_list_tables(bakery_id)

    def get_dict_map_table(self, bakery_id: int, date: datetime.datetime) -> dict:
        regs = self.__repository.get_reg_list_by_bakery_and_date(bakery_id, date)
        map_reg = {}
        for r in regs:
            if r.table.name not in map_reg:
                map_reg[r.table.name] = []
            map_reg[r.table.name].append(f"{self.converter_min_to_time(r.start_time)}-{self.converter_min_to_time(r.end_time)}")
        return map_reg

    def update(self, entity: RegistrateTable):
        self.__repository.update(entity)
