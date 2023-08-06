from setuptools import setup

setup(
	name="kewkekkek",
	version="1.2.0",
	entry_points={
		'console_scripts':[
			'kewkekkek_post_install = kewkekkek.post_install:run_script',
		],
	},

)