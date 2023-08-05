from query_tool_service import QueryTool
from entities_service import EntitiesService
from dimension_service import DimensionService
from filters_service import FilterService

def get_query_tool() -> QueryTool:
    return QueryTool(
        entities_cls=EntitiesService(), 
        filters_cls=FilterService(),
        dimesion_cls=DimensionService(),
    )