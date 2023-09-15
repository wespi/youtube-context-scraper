# YouTube Context Scraper

**Remark: The YouTube Context Scraper works only for short videos and should be understood as a showcase project.**

This application extracts information from YouTube videos. Supported languages are English and German.

## Features

The YouTube Contex Scraper includes the following features:

1. Transcription of spoken text
2. Summarizaiton of transcription
3. Extraction of five key topics that are being discussed


## Convert Python File to Executable

For this step we use `pyinstaller` and the convertion is done as follows

```{shell}
pyinstaller --noconfirm --onefile --windowed --name "YouTube Context Scraper" --icon=application_icon.icns main.py --add-data '.env:.'
```

Remark: For everything to work as expected, `load_dotenv` must be loaded as [follows](https://github.com/theskumar/python-dotenv/issues/259).

## OpenAI

In order to use the API of ChatGTP, a key is needed. The key can be easily created on the OpenAI website
and should be stored in a `.env` file on the same folder hierarchy as `main.py`. The content should look like this:

```{shell}
OPENAI_API_KEY=your_key_is_here
```