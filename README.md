# YouTube Context Scraper

This application extracts information from YouTube videos. Supported languages are English and German.

## Features

The YouTube Contex Scraper includes the following features:

1. transcription of spoken text
2. summary of transcription
3. extraction of five topics that are being discussed


## Convert Python File to Executable

For this step we use `pyinstaller` and the convertion is done as follows

```{shell}
pyinstaller --noconfirm --onefile --windowed --name "YouTube Context Scraper" --icon=application_icon.icns main.py --add-data '.env:.'
```

Remark: For everything to work as expected, `load_dotenv`` must be loaded as [follows](https://github.com/theskumar/python-dotenv/issues/259).