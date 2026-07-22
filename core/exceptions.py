"""Framework-level exceptions."""


class RAGFrameworkError(Exception):
    """Base exception for framework errors."""


class ConfigurationError(RAGFrameworkError):
    """Raised when configuration is invalid."""


class PluginNotFoundError(RAGFrameworkError):
    """Raised when a requested plugin is not registered."""


class DocumentLoadError(RAGFrameworkError):
    """Raised when a document cannot be loaded."""


class VectorStoreError(RAGFrameworkError):
    """Raised when vector store operations fail."""


class PluginDependencyError(RAGFrameworkError):
    """Raised when a plugin's optional third-party dependency is missing."""


