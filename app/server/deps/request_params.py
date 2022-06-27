
import json
from typing import Optional

from pymongo import ASCENDING, DESCENDING

from fastapi import HTTPException, Query
# from sqlalchemy import asc, desc
# from sqlalchemy.ext.declarative import DeclarativeMeta

from server.schemas.request_params import RequestParams


def parse_react_admin_params() -> RequestParams:
    """Parses sort and range parameters coming from a react-admin request"""
    #model: DeclarativeMeta
    def inner(
        sort_: Optional[str] = Query(
            None,
            alias="sort",
            description='Format: `["field_name", "direction"]`',
            example='["id", "ASC"]',
        ),
        range_: Optional[str] = Query(
            None,
            alias="range",
            description="Format: `[start, end]`",
            example="[0, 10]",
        ),
    ):
        skip, limit = 0, 10
        if range_:
            start, end = json.loads(range_)
            skip, limit = start, (end - start + 1)

        order_by = ("_id", DESCENDING) #desc(model.id)
        if sort_:
            sort_column, sort_order = json.loads(sort_)

            if sort_order.lower() == "asc":
                direction = ASCENDING
            elif sort_order.lower() == "desc":
                direction = DESCENDING
            else:
                raise HTTPException(
                    400, f"Invalid sort direction {sort_order}")
            # direction('name')  # model.__table__.c[sort_column]
            order_by = (f"_{sort_column}", direction)

        return RequestParams(skip=skip, limit=limit, order_by=order_by)

    return inner
