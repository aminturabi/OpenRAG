from core.contracts import VectorStoreBackend
from core.registry import register_plugin, create_plugin, list_plugins
from core.exceptions import PluginNotFoundError


@register_plugin("vectorstores", "test_mock_store")
class MockVectorStore(VectorStoreBackend):
    def __init__(self, val: int = 42) -> None:
        self.val = val

    def add_documents(self, collection_name, documents, embeddings, ids):
        pass

    def query(self, collection_name, query_embeddings, n_results=4):
        return ["mock result"]

    def delete_collection(self, collection_name):
        return True

    def list_collections(self):
        return ["mock_col"]


def test_plugin_registration_and_creation():
    plugins = list_plugins("vectorstores")
    assert "test_mock_store" in plugins

    instance = create_plugin("vectorstores", "test_mock_store", val=100)
    assert isinstance(instance, VectorStoreBackend)
    assert instance.val == 100
    assert instance.query("mock_col", [[0.1]]) == ["mock result"]


def test_plugin_not_found_raises_exception():
    try:
        create_plugin("vectorstores", "non_existent_plugin_xyz")
        assert False, "Should have raised PluginNotFoundError"
    except PluginNotFoundError:
        assert True
