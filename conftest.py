import sys
import os

# Vanemkataloogi lisamine sys.path-i, et saaks importida faile teistest kataloogidest. Oli vaja, et saaks pytesti käivitada.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))