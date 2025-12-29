# Expose routers for FastAPI app include_router
from .projects import router as projects_router  # noqa: F401
from .files import router as files_router  # noqa: F401
from .llm import router as llm_router  # noqa: F401
from .anythingllm import router as anythingllm_router  # noqa: F401
from .generation import router as generation_router  # noqa: F401
from .analysis import router as analysis_router  # noqa: F401
from .materials import router as materials_router  # noqa: F401
from .pipeline import router as pipeline_router  # noqa: F401
from .chapters import router as chapters_router  # noqa: F401
from .export import router as export_router  # noqa: F401
from .document import router as document_router  # noqa: F401
