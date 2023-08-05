from query_tool.services.query_tool_service import QueryTool
from query_tool.services.entities_service import EntitiesService
from query_tool.services.dimension_service import DimensionService
from query_tool.services.filters_service import FilterService

def get_query_tool() -> QueryTool:
    return QueryTool(
        entities_cls=EntitiesService(), 
        filters_cls=FilterService(),
        dimesion_cls=DimensionService(),
    )