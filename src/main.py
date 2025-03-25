from generatepub import generate_page, generate_public
import os

def main():
    generate_public(backup_dir=False)
    if os.path.exists("content/index.md"):
        generate_page("content/index.md", "template.html", "public/index.html")
    else:
        print("File not found: content/index.md")

if __name__ == "__main__":
    main()