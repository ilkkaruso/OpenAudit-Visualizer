from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import topics, lgus, transactions, analytics, llm

app = FastAPI(
    title="OpenAudit API",
    description="API for Philippine audit reports data exploration and LLM integration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(topics.router)
app.include_router(lgus.router)
app.include_router(transactions.router)
app.include_router(analytics.router)
app.include_router(llm.router)


@app.get("/")
def root():
    return {
        "message": "OpenAudit API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
