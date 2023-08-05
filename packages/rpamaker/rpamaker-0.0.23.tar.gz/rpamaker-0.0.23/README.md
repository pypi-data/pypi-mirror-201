# Build library

'''
python setup.py sdist bdist_wheel
'''

# Upload library

'''
twine upload dist/* -u rpamaker -p x4vJFP7VU*cdQy

rpamaker
x4vJFP7VU*cdQy
'''

# Run code
'''
python -m rpamaker.workspace_api
'''