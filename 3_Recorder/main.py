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
MediaPlayer = autoclass('android.media.MediaPlayer')
File = autoclass('java.io.File')

storage_path = (Environment.getExternalStorageDirectory()
                .getAbsolutePath() + '/kivy_recording.3gp')

recorder = MediaRecorder()
player = MediaPlayer()


def init_recorder():
    recorder.setAudioSource(AudioSource.MIC)
    recorder.setOutputFormat(OutputFormat.THREE_GPP)
    recorder.setAudioEncoder(AudioEncoder.AMR_NB)
    recorder.setOutputFile(storage_path)
    recorder.prepare()


def reset_player():
    if (player.isPlaying()):
        player.stop()
    player.reset()


def restart_player():
    reset_player()
    try:
        player.setDataSource(storage_path)
        player.prepare()
        player.start()
    except:
        player.reset()


class RecorderApp(App):
    is_recording = False

    def begin_end_recording(self):
        if (self.is_recording):
            recorder.stop()
            recorder.reset()
            self.is_recording = False
            self.root.ids.begin_end_recording.text = \
                ('[font=Modern Pictograms][size=120]'
                 'e[/size][/font]\nBegin recording')
            return

        init_recorder()
        recorder.start()
        self.is_recording = True
        self.root.ids.begin_end_recording.text = \
            ('[font=Modern Pictograms][size=120]'
             '%[/size][/font]\nEnd recording')

    def begin_playback(self):
        restart_player()

    def delete_file(self):
        reset_player()
        File(storage_path).delete()


if __name__ == '__main__':
    Logger.info('App: storage path == "%s"' % storage_path)

    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '900')

    LabelBase.register(name='Modern Pictograms',
                       fn_regular='modernpics.ttf')

    RecorderApp().run()
