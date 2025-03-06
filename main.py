from recorder import Recorder


def main():
    recorder = Recorder()
    recorder.play("saved_recordings/1920_1080_game")

    for i in range(22):
        print(i)
        recorder.play("saved_recordings/1920_1080_layout1")
        recorder.play("saved_recordings/1920_1080_layout2")
        recorder.play("saved_recordings/1920_1080_none")
        recorder.play("saved_recordings/1920_1080_none")
        recorder.play("saved_recordings/1920_1080_layout3")
        recorder.play("saved_recordings/1920_1080_layout4")
        recorder.play("saved_recordings/1920_1080_none")
        recorder.play("saved_recordings/1920_1080_layout1")
        recorder.play("saved_recordings/1920_1080_none")
        recorder.play("saved_recordings/1920_1080_none")
        recorder.play("saved_recordings/1920_1080_layout5")
        recorder.play("saved_recordings/1920_1080_layout6")
        recorder.play("saved_recordings/1920_1080_layout3")
        recorder.play("saved_recordings/1920_1080_layout5")
        recorder.play("saved_recordings/1920_1080_none")
        recorder.play("saved_recordings/1920_1080_none")

    # recorder.record(escape_key='`')
    # recorder.play()

    # To save the recording then playback later:
    # recorder.save_recording("layout6")

if __name__ == '__main__':
    main()