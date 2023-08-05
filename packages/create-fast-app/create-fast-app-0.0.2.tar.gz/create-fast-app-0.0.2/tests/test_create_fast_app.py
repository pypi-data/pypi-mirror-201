import os
import subprocess
import shutil
import pytest

# The path to the create-fastapi-app script
os.chdir("../")
SCRIPT_PATH = os.path.join(os.getcwd(), "create_fast_app", "cli.py")
print(SCRIPT_PATH)

def test_create_microservice_app(tmpdir):
    """Test creating a FastAPI microservice app"""
    project_name = "test_microservice_app"
    project_path = os.path.join(tmpdir, project_name)
    subprocess.run(["python", SCRIPT_PATH, project_name, "--type=microservice"], cwd=tmpdir, check=True)
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, "src", "app.py"))
    assert os.path.exists(os.path.join(project_path, "src", "database.py"))
    assert os.path.exists(os.path.join(project_path, "src", "models.py"))
    assert os.path.exists(os.path.join(project_path, "src", "routes.py"))
    assert os.path.exists(os.path.join(project_path, "src", "schemas.py"))
    assert os.path.exists(os.path.join(project_path, "src", "utils.py"))
    assert os.path.exists(os.path.join(project_path, "requirements", "base.txt"))

def test_create_monolith_app(tmpdir):
    """Test creating a FastAPI monolith app"""
    project_name = "test_monolith_app"
    project_path = os.path.join(tmpdir, project_name)
    subprocess.run(["python", SCRIPT_PATH, project_name, "--type=monolith"], cwd=tmpdir, check=True)
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, "src", "main.py"))
    assert os.path.exists(os.path.join(project_path, "src", "database.py"))
    assert os.path.exists(os.path.join(project_path, "src", "models.py"))
    assert os.path.exists(os.path.join(project_path, "requirements", "base.txt"))

def test_create_ml_app(tmpdir):
    """Test creating a FastAPI machine learning app"""
    project_name = "test_ml_app"
    project_path = os.path.join(tmpdir, project_name)
    subprocess.run(["python", SCRIPT_PATH, project_name, "--type=ml_app"], cwd=tmpdir, check=True)
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, "notebooks"))
    assert os.path.exists(os.path.join(project_path, "data"))
    assert os.path.exists(os.path.join(project_path, "models"))
    assert os.path.exists(os.path.join(project_path, "src", "data", "make_dataset.py"))
    assert os.path.exists(os.path.join(project_path, "src", "features", "build_features.py"))
    assert os.path.exists(os.path.join(project_path, "src", "models", "predict.py"))
    assert os.path.exists(os.path.join(project_path, "src", "models", "train.py"))

def test_invalid_project_type(tmpdir):
    """Test creating an invalid project type"""
    project_name = "test_invalid_project_type"
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(["python", SCRIPT_PATH, project_name, "--type=invalid"], cwd=tmpdir, check=True)

def test_attach_ml(tmpdir):
    """Test attaching a machine learning directory"""
    project_name = "test_attach_ml"
    project_path = os.path.join(tmpdir, project_name)
    subprocess.run(["python", SCRIPT_PATH, project_name, "--type=microservice", "--ml=True"], cwd=tmpdir, check=True)
    assert os.path.exists(project_path)
    assert os.path.exists(os.path.join(project_path, "src", "app.py"))
    assert os.path.exists(os.path.join(project_path, "src", "database.py"))
    assert os.path.exists(os.path.join(project_path, "src", "models.py"))
    assert os.path.exists(os.path.join(project_path, "src", "routes.py"))
    assert os.path.exists(os.path.join(project_path, "src", "schemas.py"))
    assert os.path.exists(os.path.join(project_path, "src", "utils.py"))
    assert os.path.exists(os.path.join(project_path, "requirements", "base.txt"))
    assert os.path.exists(os.path.join(project_path, "src", "internal", "ml", "notebooks"))
    assert os.path.exists(os.path.join(project_path, "src", "internal", "ml",  "data"))
    assert os.path.exists(os.path.join(project_path, "src", "internal", "ml",  "models"))
    assert os.path.exists(os.path.join(project_path, "src",  "internal", "ml", "src", "data", "make_dataset.py"))
    assert os.path.exists(os.path.join(project_path, "src",  "internal", "ml", "src", "features", "build_features.py"))
    assert os.path.exists(os.path.join(project_path, "src",  "internal", "ml", "src", "models", "predict.py"))
    assert os.path.exists(os.path.join(project_path, "src",  "internal", "ml", "src", "models", "train.py"))
