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
# Ensure submodules are importable as api.api.export, etc.
from . import export  # noqa: F401

# Ensure local backend_service root is ahead of site-packages to avoid same-name package shadowing
import sys, os  # noqa: E401
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
