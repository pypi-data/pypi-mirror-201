from .pinecone import *

__doc__ = pinecone.__doc__
if hasattr(pinecone, "__all__"):
    __all__ = pinecone.__all__