from typing import List


class EntitiesService:
    def __init__(self):
        self.__table_aliases = {}

    def get_entities(self, entities):
        # get unqiue tables from entities and relations
        unique_tables = self.__get_tables_from_entities(entities)
        # unique_tables = self.__get_tables_from_relations(entities, unique_tables)
        self.__create_table_aliases(unique_tables)
        entity_columns, tables = self.__get_entites(entities)
        relations, join_tables = self.__get_relations(entities)
        tables_with_aliases = self.__get_tables_with_aliases(tables, join_tables)
        return (
            entity_columns,
            tables_with_aliases,
            relations,
            self.__table_aliases,
        )

    def __create_table_aliases(self, tables):
        alias_index = 1
        for table in tables:
            if table not in self.__table_aliases:
                self.__table_aliases[table] = f"T{alias_index}"
            alias_index += 1

    def __get_tables_with_aliases(self, tables: List[str], join_tables: List[str]):
        select_tables = [table for table in tables if table not in join_tables]
        return (
            ", ".join(
                [
                    f"{table} as {self.__table_aliases.get(table, table)}"
                    for table in select_tables
                ]
            ),
        )

    def __get_tables_from_entities(self, entities):
        tables = []
        if entities is not None:
            for entity in entities:
                join_table = f"{entity.get('database')}.{entity.get('table')}"
                if join_table not in tables:
                    tables.append(join_table)
        return tables

    def __get_tables_from_relations(
        self, entities, existing_tables: List[str]
    ) -> List[str]:
        join_tables = existing_tables
        if entities is not None:
            for entity in entities:
                for relation in entity.get("relationship", []):
                    join_table = f"{relation.get('rightColumnDatabase', '')}.{relation.get('rightColumnTable', '')}"
                    if join_table in join_tables:
                        join_tables.remove(join_table)
                    join_tables.append(join_table)
        return join_tables

    def __get_entites(self, entities: List = None):
        entity_columns = []
        tables = []
        if entities is not None:
            for entity in entities:
                table = f"{entity.get('database')}.{entity.get('table')}"
                for column in entity.get("columns"):
                    entity_columns.append(
                        f"{self.__table_aliases.get(table, table)}.{column}"
                    )
                    if table not in tables:
                        tables.append(table)
        return (entity_columns, tables)

    def __get_relations(self, entities: List = None):
        relations = []
        join_tables = []
        if entities is not None:
            for entity in entities:
                for relation in entity.get("relationship", []):
                    table = f"{relation.get('rightColumnDatabase', '')}.{relation.get('rightColumnTable', '')}"
                    column = relation.get("rightColumnColumn", "")
                    join_column = relation.get("leftColumnFqcn", "")
                    join_table = (
                        f"{entity.get('database', '')}.{entity.get('table', '')}"
                    )
                    if join_table not in join_tables:
                        join_tables.append(join_table)

                    relations.append(
                        f"{relation.get('joinType')} {join_table} as {self.__table_aliases.get(join_table, join_table)} ON {self.__table_aliases.get(table, table)}.{column} = {self.__table_aliases.get(join_table, join_table)}.{join_column}"
                    )
        return relations, join_tables
