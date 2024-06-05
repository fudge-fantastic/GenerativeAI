## [FastAPI - Learn FastAPI](https://fastapi.tiangolo.com/tutorial/) & [Flask - Learn Flask](https://flask.palletsprojects.com/en/3.0.x/tutorial/)
```
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
  uvicorn.run("main:app", host="localhost", port=8000)
```
1. fastapi dev main.py (in terminal) OR 
2. python main.py (if using (if __name__ == '__main__'))
3. Below is for Flask
```
# If not in Prod, debug=True, else, debug=False
if __name__ == '__main__':
	app.run(host = "0.0.0.0", port = "8000", debug = True)
```


## [Tesseract-Fix](https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i)

**Installing Tesseract Binary:**
**Linux:**

1. Open a terminal window.
2. Update the package list:
   ```bash
   sudo apt-get update
   ```
3. Install the required packages:
   ```bash
   sudo apt-get install libleptonica-dev tesseract-ocr tesseract-ocr-dev libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn
   ```
   - This command installs Tesseract OCR itself, along with its development libraries and language packs (English and script for Latin characters).

**Mac:**

1. Open a terminal window.
2. Install Tesseract using Homebrew (package manager for Mac):
   ```bash
   brew install tesseract
   ```

**Windows:**

1. Download the Tesseract installer from [https://github.com/tesseract-ocr/tesseract/blob/main/INSTALL](https://github.com/tesseract-ocr/tesseract/blob/main/INSTALL). Choose the appropriate installer (32-bit or 64-bit) based on your system.
2. Run the downloaded installer and follow the on-screen instructions. During installation, make sure to select the option to add Tesseract to your system PATH environment variable. This allows you to access Tesseract from any command prompt.

**Installing Python Package:**
Once you've installed the Tesseract binary for your system, you can install the Python packages:

1. Open a terminal window (Linux/Mac) or command prompt (Windows).
2. Install `tesseract` package using pip (package manager for Python):
   ```bash
   pip install tesseract
   ```
3. (Optional) If you want to use `pytesseract` library for a simpler interface, install it as well:
   ```bash
   pip install pytesseract
   ```

**Additional Notes:**

- The `pytesseract.pytesseract.tesseract_cmd` line is used for specific cases where Tesseract's location might not be automatically detected by `pytesseract`. You typically wouldn't need this line after installing Tesseract correctly.
- After installation, you can verify if Tesseract is working by running the following command in your terminal/command prompt:
   ```bash
   tesseract --version
   ```