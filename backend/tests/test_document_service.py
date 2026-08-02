from app.services.documents import DocumentService


def test_document_service_can_be_constructed() -> None:
    assert DocumentService() is not None
