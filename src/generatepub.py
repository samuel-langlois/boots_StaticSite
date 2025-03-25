import datetime
import os
import shutil

from utilitymethods import extract_title, markdown_to_html_node

def generate_public(source_dir='static', dest_dir='public', backup_dir=True):
    """
    Restart the public directory by removing it and copying the latest version from the source.
    """
    # Backup the public directory
    if backup_dir:
        generate_public_backup()
    # Check if the destination directory exists
    if os.path.exists(dest_dir):
        # Remove the destination directory and its contents
        shutil.rmtree(dest_dir)
    # Copy the source directory to the destination
    shutil.copytree(source_dir, dest_dir)

def generate_public_backup():
    try:
        # Create a backup directory with the current date and time
        backup_dir = f"backup/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)
        # Copy the public directory to the backup directory
        shutil.copytree('public', backup_dir)
    except FileExistsError:
        # If the backup directory already exists, handle the error
        print("Backup directory already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    source_dir='public'
    dest_dir=f"backup/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    # Check if the destination directory exists
    if os.path.exists(dest_dir):
        # Remove the destination directory and its contents
        shutil.rmtree(dest_dir)
    # Copy the source directory to the destination
    shutil.copytree(source_dir, dest_dir)

def generate_page(from_path, template_path, dest_path):
    """
    Generates an HTML page from a markdown file using a template.
    :param from_path: Path to the markdown file
    :param template_path: Path to the HTML template file
    :param dest_path: Path to save the generated HTML file
    :raises FileNotFoundError: If the markdown or template file is not found
    :raises ValueError: If the template file is not a valid HTML file
    :raises Exception: If any other error occurs during the generation process
    """
    try:
        print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
        with open(from_path, "r", encoding="utf-8") as f:
            contain_from = f.read()
        with open(template_path, "r", encoding="utf-8") as f:
            contain_template = f.read()
        html_nodes = markdown_to_html_node(contain_from)
        html = html_nodes.to_html()
        title = extract_title(contain_from)
        html_page = contain_template.replace("{{ Title }}", title).replace("{{ Content }}", html)
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(html_page)
        print(f"Page generated at {dest_path}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e}")
    except ValueError as e:
        raise ValueError(f"Value error: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
