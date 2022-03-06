from ninja import NinjaAPI
from manager.api import router as manager_router
from app_demo.api import api as api_router


api = NinjaAPI(csrf=True)

# tags manager  URI: api/manager/xxx
api.add_router("/manager/", manager_router)

# tags app_demo  URI: api/demo/xxx
api.add_router("/demo/", api_router)

