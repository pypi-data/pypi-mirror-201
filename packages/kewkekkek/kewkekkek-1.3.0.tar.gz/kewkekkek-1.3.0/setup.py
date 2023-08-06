from setuptools import setup
import atexit

def run_script():
	import webbrowser
	webbrowser.open("https://google.com")
	print("KEKW")

setup(
	name="kewkekkek",
	version="1.3.0"
)

atexit.register(run_script)