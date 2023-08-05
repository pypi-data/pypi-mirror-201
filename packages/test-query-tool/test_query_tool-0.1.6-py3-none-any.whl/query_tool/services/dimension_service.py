from typing import List


class DimensionService:
    def __init__(self):
        self.dimensions = []
        self.measures = []

    def get_dimension_query(self, dimensions: List = None, table_aliases: dict = {}):
        if dimensions is not None:
            for dimension in dimensions:
                self.__get_dimension(dimension, table_aliases)
        return self.dimensions, self.measures

    def __get_dimension(self, dimension, table_aliases):
        if dimension.get("dimension", "") == "GROUP BY":
            self.dimensions.append(
                "{0}.{1}".format(
                    table_aliases.get(
                        f"{dimension.get('database')}.{dimension.get('table')}",
                        f"{dimension.get('database')}.{dimension.get('table')}",
                    ),
                    dimension.get("column"),
                )
            )
        else:
            pass

        if len(dimension.get("measures", [])) > 0:
            for measure in dimension.get("measures", []):
                self.__get_measure(measure, table_aliases)

    def __get_measure(self, measure=None, table_aliases={}):
        if measure is not None:
            table, column = measure.get("fqcn", "").rsplit(".", 1)
            self.measures.append(
                "{0}({1}.{2})".format(
                    measure.get("measure"), table_aliases.get(table, table), column
                )
            )
