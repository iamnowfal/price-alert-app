from src.app import app



app.run(debug=app.config['DEBUG'], port=4490) # app.config is an attribute of app class. Therefore the config has to be imported to the app class to make this work

#Before run file can import something from app file, python has to compile the app file first and then let it be imported