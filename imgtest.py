import sudoku as sud
import pytesseract


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    )
    nums = sud.proc()
    print(nums)
