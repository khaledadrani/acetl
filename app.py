from fastapi import FastAPI, APIRouter
from typing import Dict, List
import uvicorn
from fastapi.routing import APIRoute

app = FastAPI()
routers: Dict[str, APIRouter] = {}

@app.get("/create_route/{route_name}")
async def create_route(route_name: str):
    router = APIRouter()

    @router.get(f"/{route_name}")
    async def new_route():
        return {"message": f"You have accessed {route_name} route"}

    routers[route_name] = router
    app.include_router(router)
    app.openapi_schema = None;
    app.setup()
    return {"message": f"Route {route_name} created"}


@app.get("/get_all_routes")
def get_all_endpoints() -> List[str]:
    endpoints = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            endpoints.append(route.path)
    return endpoints

@app.get("/delete_route/{route_name}")
async def delete_route(route_name: str):
    del routers[route_name]
    # I can't delete the route from the app
    return {"message": f"Route {route_name} deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080, log_level="info")