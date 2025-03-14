from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "DhakAI Backend running smoothly!"}

@app.post("/run-test")
def run_automation_test():
    result = subprocess.run(["pytest", "../automation"], capture_output=True, text=True)
    return {"test_output": result.stdout, "test_errors": result.stderr}
