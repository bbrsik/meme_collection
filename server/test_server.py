import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base
from models import Meme
import io
from serializers import serialize_meme, serialize_memes

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_meme():
    response = client.post(
        "/memes/?text=This is a test meme",
    )
    assert response.status_code == 200
    data = response.json()
    # import pdb; pdb.set_trace()
    assert data["text"] == "This is a test meme"
    assert "id" in data
    assert "upload_date" in data

def test_create_meme_with_image(mocker):
    # Mock the requests.post call
    mock_post = mocker.patch('requests.post')
    mock_post.return_value.status_code = 200

    response = client.post(
        "/memes/?text=This is a test meme",
        files={"image": ("test.jpg", io.BytesIO(b"test"), "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "This is a test meme"
    assert "id" in data
    assert "image_name" in data
    assert "upload_date" in data

def test_get_memes():
    # Create a test meme
    client.post("/memes/?text=This is a test meme")

    response = client.get("/memes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["text"] == "This is a test meme"

def test_get_meme_by_id():
    # Create a test meme
    create_response = client.post("/memes/?text=This is a test meme")
    meme_id = create_response.json()["id"]

    response = client.get(f"/memes/{meme_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "This is a test meme"

def test_get_meme_image_by_id(mocker):
    # Mock the requests.get call
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.content = b"test image content"

    # Mock the requests.post call for creating meme with image
    mock_post = mocker.patch('requests.post')
    mock_post.return_value.status_code = 200

    # Create a test meme with image
    create_response = client.post(
        "/memes/?text=This is a test meme",
        files={"image": ("test.jpg", io.BytesIO(b"test"), "image/jpeg")}
    )
    meme_id = create_response.json()["id"]

    response = client.get(f"/memes/{meme_id}/image")
    assert response.status_code == 200
    assert response.content == b"test image content"

def test_update_meme():
    # Create a test meme
    create_response = client.post("/memes/?text=This is a test meme")
    meme_id = create_response.json()["id"]

    # Update the meme
    response = client.put(
        f"/memes/{meme_id}?text=This is an updated test meme"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "This is an updated test meme"

def test_update_meme_with_image(mocker):
    # Mock the requests.put call
    mock_put = mocker.patch('requests.put')
    mock_put.return_value.status_code = 200

    # Create a test meme
    create_response = client.post("/memes/?text=This is a test meme")
    meme_id = create_response.json()["id"]

    # Update the meme with image
    response = client.put(
        f"/memes/{meme_id}?text=This is an updated test meme",
        files={"image": ("updated.jpg", io.BytesIO(b"updated"), "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "This is an updated test meme"
    assert "image_name" in data

def test_delete_meme(mocker):
    # Mock the requests.delete call
    mock_delete = mocker.patch('requests.delete')
    mock_delete.return_value.status_code = 200

    # Create a test meme
    create_response = client.post("/memes/?text=This is a test meme")
    meme_id = create_response.json()["id"]

    # Delete the meme
    response = client.delete(f"/memes/{meme_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Meme with ID {meme_id} was successfully deleted!"

    # Verify the meme is deleted
    get_response = client.get(f"/memes/{meme_id}")
    assert get_response.status_code == 404
