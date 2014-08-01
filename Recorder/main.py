from jnius import autoclass
from kivy.app import App
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.logger import Logger

Environment = autoclass('android.os.Environment')
MediaRecorder = autoclass('android.media.MediaRecorder')
AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')

storage_path = Environment.getExternalStorageDirectory().getAbsolutePath()

recorder = MediaRecorder()
recorder.setAudioSource(AudioSource.MIC)
recorder.setOutputFormat(OutputFormat.THREE_GPP)
recorder.setAudioEncoder(AudioEncoder.AMR_NB)
recorder.setOutputFile(storage_path + '/kivy_recording.3gp')
recorder.prepare()


class RecorderApp(App):
    is_recording = False

    def begin_end_recording(self):
        if (self.is_recording):
            recorder.stop()
            self.is_recording = False
            self.root.ids.begin_end_recording.text = \
                ('[font=Modern Pictograms][size=120]'
                 'e[/size][/font]\nBegin recording')
            return

        recorder.start()
        self.is_recording = True
        self.root.ids.begin_end_recording.text = \
            ('[font=Modern Pictograms][size=120]'
             'X[/size][/font]\nEnd recording')

if __name__ == '__main__':
    Logger.info('App: storage path == "%s"' % storage_path)

    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '900')

    LabelBase.register(name='Modern Pictograms',
                       fn_regular='modernpics.ttf')

    RecorderApp().run()
