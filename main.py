import subprocess
import threading
import time

def run_fastapi():
    subprocess.run(["uvicorn", "apis:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def run_streamlit():
    subprocess.run(["streamlit", "run", "app_frontend.py"])

if __name__ == "__main__":
    # Start FastAPI in a thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()

    # Delay slightly to allow FastAPI to start
    time.sleep(2)

    # Run Streamlit
    run_streamlit()
