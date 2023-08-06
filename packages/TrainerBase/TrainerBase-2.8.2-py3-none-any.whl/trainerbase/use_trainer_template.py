import os
import shutil


shutil.copytree(os.path.join(os.path.dirname(__file__), "template"), os.getcwd(), dirs_exist_ok=True)
