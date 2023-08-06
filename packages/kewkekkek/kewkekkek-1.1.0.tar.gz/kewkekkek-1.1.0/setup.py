from setuptools import setup

setup(
	name="kewkekkek",
	version="1.1.0",
	entry_points={
		'console_scripts':[
			'kewkekkek_post_install = kewkekkek.post_install:run_script',
		],
	},

)