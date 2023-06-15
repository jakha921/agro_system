from fastapi import FastAPI, Request, status
from fastapi.exceptions import ValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.roles.routers import router as roles_routes
from src.countries.routers import router as countries_routes
from src.rigions.routers import router as regions_routes
from src.cities.routers import router as cities_routes
from src.districts.routers import router as districts_routes
from src.genders.routers import router as genders_routes
from src.statuses.routers import router as statuses_routes
from src.complain_statuses.routers import router as complain_statuses_routes
from src.departments.routers import router as department_routes
from src.categories.routers import router as categories_routes


app = FastAPI(
    title="Agriculture API",
    description="API for agriculture",
    version="0.0.1",
)


# exception handler ValidationError
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(roles_routes)
app.include_router(countries_routes)
app.include_router(regions_routes)
app.include_router(cities_routes)
app.include_router(districts_routes)
app.include_router(department_routes)
app.include_router(genders_routes)
app.include_router(statuses_routes)
app.include_router(complain_statuses_routes)
app.include_router(categories_routes)
