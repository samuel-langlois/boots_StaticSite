from generatepub import generate_page, generate_pages_recursive, generate_public
import os, sys

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Generating pages for basepath: {basepath}")
    generate_pages_recursive(basepath=basepath, dest_dir_path='docs')


if __name__ == "__main__":
    main()