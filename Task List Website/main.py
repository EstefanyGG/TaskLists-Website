# import website code as a package
# from the __init__.py file
from website import create_app
app = create_app()

# if the file is run
if __name__ == '__main__':
    # run flask application,
    # debug = true means any change in code will re run in webserver
    app.run(debug=True)