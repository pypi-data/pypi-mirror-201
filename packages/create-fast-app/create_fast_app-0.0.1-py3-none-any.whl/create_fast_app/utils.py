import os
import shutil

def generate_ml_app(project_dir: str):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'ml_app')
    shutil.copytree(template_dir, project_dir, dirs_exist_ok=True)
    
def attach_ml_app(project_dir: str):
    os.chdir(project_dir)
    os.chdir("src")
    os.mkdir("internal")
    os.mkdir("ml")
    new_dir = os.path.join(project_dir, "src", "internal", "ml")
    generate_ml_app(new_dir)
    
    
def generate_microservice_app(project_dir: str, attach_ml: bool):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'microservice')
    shutil.copytree(template_dir, project_dir, dirs_exist_ok=True)
    
    if attach_ml:
        attach_ml_app(project_dir)
    
def generate_monolith_app(project_dir: str, attach_ml: bool):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'monolith')
    shutil.copytree(template_dir, project_dir, dirs_exist_ok=True)
    if attach_ml:
        attach_ml_app(project_dir)
    
    
def install_packages():
    os.system('python -m venv venv')
    os.system('venv\\Scripts\\activate.bat')
    os.system('pip install -r requirements\\base.txt')
    os.system('venv\\Scripts\\deactivate.bat')