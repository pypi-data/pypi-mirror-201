from typing import List

OPERATORS = {
    "EQUALS": "=",
    "NOT EQUALS": "!=",
    "GREATER THAN": ">",
    "GREATER THAN EQUALS": ">=",
    "LESS THAN": "<",
    "LESS THAN EQUALS": "<=",
}

SPECIAL_OPERATORS = [
    "LIKE",
    "NOT LIKE",
    "IS NULL",
    "IS NOT NULL",
    "BEGINS WITH",
    "ENDS WITH",
    "CONTAINS",
    "NOT CONTAINS",
]


class FilterService:
    def __init__(self):
        self.filter_conditions = []
    
    def __is_string_column(self, column: dict = {}) -> bool:
        return True if column.get('data_type', 'string') == 'string' else False

    def get_filter_query(self, filters: List = None, table_aliases: dict = {}):
        if filters is not None:
            for filter in filters:
                self.__get_filter(filter, table_aliases)
        return self.filter_conditions

    def __get_filter(self, filter, table_aliases):
        self.filter_conditions.append("(")
        table, column = filter.get("fqcn", "").rsplit(".", 1)
        if filter.get("operator", "") in OPERATORS:
            self.filter_conditions.append(
                "{0}.{1} {2} {3}".format(
                    table_aliases.get(table, table),
                    column,
                    OPERATORS.get(filter.get("operator")),
                    f"'{filter.get('value')}'"
                    if self.__is_string_column(filter)
                    else filter.get("value"),
                )
            )
        else:
            if (
                filter.get("operator", "") == "LIKE"
                or filter.get("operator", "") == "NOT LIKE"
            ):
                self.filter_conditions.append(
                    "{0}.{1} {2} '%{3}%'".format(
                        table_aliases.get(table, table),
                        column,
                        filter.get("operator"),
                        filter.get("value"),
                    )
                )
            elif (
                filter.get("operator", "") == "IS NULL"
                or filter.get("operator", "") == "IS NOT NULL"
            ):
                self.filter_conditions.append(
                    "{0}.{1} {2}".format(
                        table_aliases.get(table, table), column, filter.get("operator")
                    )
                )
            elif (
                filter.get("operator", "") == "BEGINS WITH"
                or filter.get("operator", "") == "ENDS WITH"
            ):
                self.filter_conditions.append(
                    "{0}.{1} LIKE '{2}'".format(
                        table_aliases.get(table, table),
                        column,
                        f"%{filter.get('value')}"
                        if "BEGINS WITH" == filter.get("operator", "")
                        else f"{filter.get('value')}%",
                    )
                )
            elif (
                filter.get("operator", "") == "CONTAINS"
                or filter.get("operator", "") == "NOT CONTAINS"
            ):
                self.filter_conditions.append(
                    f"{0} contains({1}.{2}, '{3}')".format(
                        "NOT " if filter.get("operator", "") == "NOT CONTAINS" else "",
                        table_aliases.get(table, table),
                        column,
                        filter.get("value"),
                    )
                )

        if len(filter.get("filtersList", [])) > 0:
            self.filter_conditions.append(filter.get("connector", "AND"))
            for filter_ in filter.get("filtersList", []):
                self.__get_filter(filter_, table_aliases)
        self.filter_conditions.append(")")
