"""
The app extracts and saves audio from a Youtube video

BeeWare Commands
briefcase new - create a new skeletal BeeWare app
briefcase dev - run the BeeWare app in development
briefcase create - start to package the app for distribution
briefcase build - compile the app
briefcase run - run the compiled app
briefcase package - package the compiled app
briefcase create android
briefcase build android
briefcase run android
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from pytube import YouTube
from http.client import IncompleteRead
from pytube.helpers import safe_filename
import asyncio


class YoutubePodcast(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.
        """
        ## set style
        container_style = Pack(
            padding=10,
            alignment='center'
            )

        ## create instruction text and input window
        instruction_label = toga.Label(
            text='Paste the link:',
            style=container_style
            )
        self.url_input = toga.TextInput(
            style=container_style
            )

        ## create button to save audio track
        download_button = toga.Button(
            'Save',
            on_press=self.download_audio,
            style=container_style
            )

        ## create info text output
        self.info_text = toga.Label(
            text='Waiting for the URL...',
            style=container_style
            )

        ## construct and show main interface
        main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                alignment='center',
                )
            )
        main_box.add(instruction_label)
        main_box.add(self.url_input)
        main_box.add(download_button)
        main_box.add(self.info_text)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    
    def download_audio(self, widget):
        url = self.url_input.value
        if url:
            try:
                yt = YouTube(url)
                audio_stream = yt.streams.filter(only_audio=True)[0]

                title = safe_filename(yt.title) + '.mp3'
                path = '/storage/emulated/0/Download/'

                audio_stream.download(filename=title, output_path=path)
                self.info_text.text = 'Done!'
                self.url_input.value = ''  # clean URL input
            except Exception:
                self.info_text.text = 'Download failed'
        else:
            self.info_text.text = 'Enter URL first'


def main():
    return YoutubePodcast()
