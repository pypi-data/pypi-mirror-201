import os
import sys
import click

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from create_fast_app import utils

@click.command()
@click.option("--ml", default=False, help="Attach A machine learning directory to project", type=bool)
@click.option("--type", type=str, default="microservice")
@click.argument('project_name')
def create_fastapi_app(project_name, type, ml):
    """Create a new FastAPI project."""
    click.echo(f"Creating new {type} project {project_name}...")
    # Get the absolute path of the directory where the script is running
    current_dir = os.getcwd()
    project_dir = os.path.join(current_dir, project_name)
    
    click.echo(f"Creating directory {project_dir}...")
    os.makedirs(project_dir)
    
    # Copy the FastAPI project template to the new directory
    if type == "microservice":
        click.echo("Generating microservice app template...")
        utils.generate_microservice_app(project_dir, attach_ml=ml)
        
    elif type == "monolith":
        click.echo("Generating monolith app template...")
        utils.generate_monolith_app(project_dir, attach_ml=ml)
        
    elif type == "ml_app":
        click.echo("Generating machine learning app template...")
        utils.generate_ml_app(project_dir)
        
    else:
        click.echo(f"Invalid project type {type}. Must be one of [ml_app, monolith, microservice]")
        sys.exit(2)
        
    click.echo("FastAPI project template generated successfully!")
    
    # Create a virtual environment and install the required dependencies
    click.echo("Creating virtual environment and installing dependencies...")
    os.chdir(project_dir)
    utils.install_packages()
    click.echo("Dependencies installed successfully!")
    
    # Print the success message
    click.echo(f'Success! Created {project_name} at {current_dir}\{project_name}')



if __name__ == '__main__':
    create_fastapi_app()
