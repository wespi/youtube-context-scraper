import sys
import os
import PySimpleGUI as sg
from youtube_transcript_api import YouTubeTranscriptApi
import openai
from dotenv import load_dotenv


data_dir = os.getcwd()
if getattr(sys, "frozen", False):
    data_dir = sys._MEIPASS

load_dotenv(dotenv_path=os.path.join(data_dir, ".env"))
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_transcript(youtube_url):
    try:
        video_id = youtube_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["de", "en"]
        )
        text = " ".join([t["text"].replace("\n", " ") for t in transcript])
        return text
    except Exception as e:
        print("Error:", e)
        return None


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.7):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message["content"]
    except:
        return "Your transcription is too long."


def main():
    layout = [
        [sg.Text("Enter YouTube Video URL:")],
        [sg.Input(key="URL")],
        [
            sg.Button("Extract Transcript", button_color="tomato"),
            sg.Button("Clean Up"),
            sg.Button("Exit"),
        ],
        [sg.Multiline(size=(80, 20), key="OUTPUT_TRANSCRIPT", autoscroll=True)],
        [sg.Button("Summarize", button_color="tomato")],
        [sg.Multiline(size=(80, 10), key="OUTPUT_SUMMARY", autoscroll=True)],
        [sg.Button("Get Topics", button_color="tomato")],
        [sg.Multiline(size=(80, 5), key="OUTPUT_TOPICS", autoscroll=True)],
    ]

    window = sg.Window("YouTube Context Scraper", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Clean Up":
            window["URL"].update("")
            for i in ["TRANSCRIPT", "SUMMARY", "TOPICS"]:
                window[f"OUTPUT_{i}"].update("")
        elif event == "Extract Transcript":
            youtube_url = values["URL"]
            transcript_text = extract_transcript(youtube_url)
            if transcript_text:
                window["OUTPUT_TRANSCRIPT"].update(transcript_text)
            else:
                window["OUTPUT_TRANSCRIPT"].update("Failed to extract transcript.")
        elif event == "Summarize" and transcript_text:
            prompt = f"""
            Your task is to generate a short summary of a text.

            Summarize the text below, delimited by triple
            backticks, in at most 50 words. Your summary has to be
            in the same language as the given text.

            Text: ```{transcript_text}```
            """
            response = get_completion(prompt)
            window["OUTPUT_SUMMARY"].update(response)
        elif event == "Get Topics" and transcript_text:
            prompt = f"""
            Determine five topics that are being discussed in the
            following text, which is delimited by triple backticks.

            Make each item one or two words long. 

            Format your response as a list of items separated by commas.
            Hence, the result looks like ``topic1, topic2, topic3, topic4, topic5``.

            Text: '''{transcript_text}'''
            """
            response = get_completion(prompt, temperature=0)
            window["OUTPUT_TOPICS"].update(response)
    window.close()


if __name__ == "__main__":
    THEME = "DarkTeal10"
    FONT_FAMILY = "Arial"
    FONT_SIZE = 14
    sg.theme(THEME)
    sg.set_options(font=(FONT_FAMILY, FONT_SIZE))
    main()
