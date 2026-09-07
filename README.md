# AI Code Reviewer

AI Code Reviewer is a Streamlit application that uses OpenRouter-compatible
language models to analyze source code and return improvement suggestions,
potential errors, and a downloadable PDF report.

## Features

- Paste code directly into the application or upload a source file.
- Supports Python, JavaScript, Java, C, C++, HTML, CSS, and text files.
- Choose from OpenAI, Anthropic, Google, Meta, DeepSeek, and Mistral models
  exposed through OpenRouter.
- Automatically detects the language for syntax-highlighted code output.
- Export the generated review as a PDF document.
- Responsive two-column Streamlit interface.

## Requirements

- Python 3.9 or newer
- An [OpenRouter](https://openrouter.ai/) API key
- `wkhtmltopdf` installed and available on your system `PATH`

`wkhtmltopdf` is required by `pdfkit` to generate PDF reports.

## Installation

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/Addepalli-Sahil/AiCodeReviewer.git
   cd AiCodeReviewer
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install `wkhtmltopdf` using the installer or package manager for your
   operating system, then confirm it is available:

   ```bash
   wkhtmltopdf --version
   ```

## Configure the API key

Create `.streamlit/secrets.toml` with the following structure:

```toml
[openrouter]
api_key = "your-openrouter-api-key"
```

The secrets file is intentionally ignored by Git. Never commit API keys or
other credentials to the repository.

## Run locally

Start the Streamlit application with:

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually
`http://localhost:8501`, in the terminal.

## How to use

1. Paste code into the input box or upload a supported source file.
2. Select the model you want to use.
3. Click **Review Code**.
4. Read the generated review and inspect the highlighted source.
5. Select **Download Review as PDF** to save the report.

If both pasted code and an uploaded file are provided, pasted code takes
precedence.

## Project structure

```text
.
├── app.py                 # Streamlit application
├── requirements.txt       # Python dependencies
├── sss.py                # Example multiple-inheritance Python script
├── .streamlit/
│   └── secrets.toml       # Local secrets; do not commit
└── .gitignore
```

## Deployment

The app can be deployed to Streamlit Community Cloud or another environment
that supports Streamlit:

1. Set the repository as the application source.
2. Set the entry point to `app.py`.
3. Add the `OPENROUTER_API_KEY` equivalent under the deployment's
   Streamlit secrets using the same `[openrouter]` structure.
4. Ensure `wkhtmltopdf` is installed in the deployment environment if PDF
   downloads are enabled.

## Notes

- Reviews are sent to the selected OpenRouter model. Avoid submitting
  proprietary code unless your organization's policies allow it.
- Model availability and pricing are controlled by OpenRouter and may change.
- PDF generation depends on the external `wkhtmltopdf` executable.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
the complete license text.

## Commit attribution

This repository does not use Copilot co-author attribution. The local Git
configuration rejects commit messages containing a Copilot co-author trailer.
After cloning, enable the repository hook with:

```bash
git config core.hooksPath .githooks
```
