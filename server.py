from src.app import app
from src.config import PORT
import src.controllers.labcontroller
import src.controllers.studentcontroller

app.run("0.0.0.0", PORT, debug=True)
