from modules.pipeline.dod_pipeline import DODRenderPipeline
from modules.pipeline.load_scene import load_scene
from modules.pipeline.execute_frame import execute_frame

# Alias agar backward compatible dengan test lama
RenderPipeline = DODRenderPipeline

__all__ = ["DODRenderPipeline", "RenderPipeline", "load_scene", "execute_frame"]