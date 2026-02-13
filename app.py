from flask import Flask, render_template, request, redirect, url_for, session
from scripts.data_packet_processing import collect_data
import serial

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

@app.get("/")
def home():
    return render_template("home.html")

@app.get("/track")
def track():
    return render_template("track.html")

@app.get("/guide")
def guide():
    return render_template("guide.html")

@app.get("/guide/overview")
def overview():
    return render_template("overview.html")

@app.get("/track/control")
def control():
    field = session.get("field") # {"length": X, "width": X}
    return render_template("control.html", field=field)

# "post" ran when form submission, store length/width from user
@app.post("/track/control")
def field_submit():
    # creating variables from user input
    length = request.form.get("fieldLength")
    width = request.form.get("fieldWidth")

    # creating session dictionary for field dimensions
    session["field"] = {"length": length, "width": width}

    return redirect(url_for("control"))

# post: on control panel, run visualization function when button clicked
@app.post("/start-DP")
def start_data_processing():
    field = session.get("field") # {"length": X, "width": X}
    
    # running data_packet_processing.py function from backend
    if field:
        try:
            collect_data(float(field["length"]), float(field["width"]))
            session["status"] = "Data collection complete"
        except serial.SerialException:
            session["error"] = "Device not connected. Check COM port."
        except Exception as e:
            session["error"] = f"Error: {str(e)}"
    
    # return to control panel with results
    return redirect(url_for("control"))

if __name__ == "__main__":
    app.run(debug=True)