from typing import Any, Coroutine, Callable, List

from fastapi import HTTPException, Request, Query

from .types import Operators, OperatorParameter


def operator_param(param_name: str) -> Callable[[Any], Coroutine]:
    async def parse(request: Request) -> OperatorParameter:
        print(request.query_params[param_name])
        vals = request.query_params[param_name].split(':')
        if len(vals) == 1:
            return OperatorParameter(vals[0])
        elif len(vals) == 2:
            try:
                return OperatorParameter(vals[1], Operators(vals[0]))
            except ValueError:
                raise HTTPException(status_code=400, detail=f'Unknown operator: {vals[0]}')
        else:
            raise HTTPException(status_code=400, detail=f'Bad arguments to parameter: {param_name}')
    return parse
