from recorder import Recorder


def main():
    recorder = Recorder()
    recorder.record()
    recorder.play()

    # To save the recording then playback later:
    # recorder.save_recording("test_record")
    # recorder.play("saved_recordings/1920_1080_test_record")
    

if __name__ == '__main__':
    main()