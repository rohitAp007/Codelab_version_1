from flask import Flask, request, render_template
import subprocess
import os
import time

app = Flask(__name__)
JAVA_FILE = "Main.java"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_code():
    code = request.form["code"]
    # Save code to Main.java
    with open(JAVA_FILE, "w") as file:
        file.write(code)

    # Compile the Java code
    compile_process = subprocess.run(["javac", JAVA_FILE], capture_output=True, text=True)
    if compile_process.returncode != 0:
        return f"Compilation Error:\n<pre>{compile_process.stderr}</pre>"

    # Run the compiled Java program
    start_time = time.time()
    run_process = subprocess.run(["java", JAVA_FILE.replace(".java", "")], capture_output=True, text=True)
    execution_time = time.time() - start_time

    if run_process.returncode == 0:
        return f"Output:\n<pre>{run_process.stdout}</pre>\nExecution Time: {execution_time:.2f} seconds"
    else:
        return f"Runtime Error:\n<pre>{run_process.stderr}</pre>"

if __name__ == "__main__":
    app.run(debug=True)
