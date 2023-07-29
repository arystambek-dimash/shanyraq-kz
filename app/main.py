from fastapi import FastAPI
from .auth.router_auth import router as router_auth
from .announcement.router_announcement import router as router_ad
from .comment.router_comment import router as router_comment
from .superuser.route_superuser import router as router_superuser
from .database import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(router=router_auth)
app.include_router(router=router_ad)
app.include_router(router=router_comment)
app.include_router(router= router_superuser)