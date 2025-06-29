import uvicorn

from app.api import create_app
from fastapi.middleware.cors import CORSMiddleware

api = create_app()
api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run('main:api', host='127.0.0.1', port=8000, reload=True)
