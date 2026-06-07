# PDF Manager: Split & Merge

A modern, lightweight Python desktop application built with `customtkinter` and `pypdf` to easily manipulate PDF files. The app allows you to split existing PDFs into individual pages or specific page ranges, and merge multiple PDFs together with custom reordering.

## Features

- **Split PDF**:
  - Extract every single page into separate PDF files.
  - Extract specific page ranges using a Word-like syntax (e.g., `1, 3, 5-8`).
- **Merge PDF**:
  - Combine multiple PDF files into a single document.
  - Easily reorder the sequence of the files before merging using an intuitive Up/Down control system.
- **Modern UI**: Dark/Light mode support matching your system preferences thanks to CustomTkinter.

## Prerequisites

Make sure you have Python 3 installed on your system. You will need the following libraries:

- `customtkinter` (for the graphical user interface)
- `pypdf` (for PDF processing)

## Installation

1. Clone this repository or download the source code.
2. Open your terminal or command prompt.
3. Install the required dependencies by running:

   ```bash
   pip install customtkinter pypdf
   ```

## Usage

Run the main Python script from your terminal:

```bash
python pdf_manager.py

```

1. Click on **SEPARA PDF** (Split) to select a file, define your page extraction rules, and save the output.
2. Click on **UNISCI PDF** (Merge) to add multiple files, arrange their order, and combine them into a single PDF.

## License

This project is open-source and available under the MIT License.

---
