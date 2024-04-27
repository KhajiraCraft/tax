from flask import Flask
from routes import *
from models import *
from tax_record_service import *
from tax_summary_service import *
from tax_calculation import *
from tax_record_ui import *

app = Flask(__name__)

# Register blueprints
app.register_blueprint(tax_record_ui)
app.register_blueprint(routes)
app.register_blueprint(models)
app.register_blueprint(tax_record_service)
app.register_blueprint(tax_summary_service)
app.register_blueprint(tax_calculation)


if __name__ == "__main__":
    app.run(debug=True)
