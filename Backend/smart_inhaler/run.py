from app import create_app
from app.routes import routes

app = create_app()
app.register_blueprint(routes)  # Register the routes blueprint

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Run the app in debug mode
