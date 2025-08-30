import argparse, sys, time
import cv2
from video.capture import open_capture, read_frame, list_indexes
from video.sinks import WindowSink, VirtualCamSink
from processing.ascii import to_ascii_image

def parse_args():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("--input", type=int, default=0, help="camera index")
    p.add_argument("--list", action="store_true", help="list camera indexes and exit")
    p.add_argument("--mode", choices=["window","virtual"], default="window", help="output mode")
    p.add_argument("--in-width", type=int, default=1280, help="camera capture width")
    p.add_argument("--in-height", type=int, default=720, help="camera capture height")
    p.add_argument("--out-width", type=int, default=1280, help="output width")
    p.add_argument("--out-height", type=int, default=720, help="output height")
    p.add_argument("--fps", type=int, default=20, help="frames per second")
    p.add_argument('--ascii', dest='ascii', action='store_true', help="enable ASCII rendering (on by default)")
    p.add_argument('--no-ascii', dest='ascii', action='store_false', help="disable ASCII rendering")
    p.set_defaults(ascii=True)
    p.add_argument("--cols", type=int, default=100, help="number of ASCII columns")
    p.add_argument("--rows", type=int, default=60, help="number of ASCII rows")
    p.add_argument("--ascii-mode", choices=["colored", "grayscale", "black-and-white", "matrix"], default="colored", help="set the ASCII rendering mode")
    p.add_argument("--rain-cols", type=int, default=70, help="number of running letters columns in matrix mode")
    p.add_argument("--rain-words", type=str, nargs='+', default=[], help="words to use for the matrix rain effect instead of random characters")
    return p.parse_args()

def main():
    args = parse_args()
    if args.list:
        print("available camera indexes:", list_indexes())
        return

    cap = open_capture(args.input, args.in_width, args.in_height, args.fps)

    sink = None
    try:
        if args.mode == "virtual":
            try:
                sink = VirtualCamSink(args.out_width, args.out_height, args.fps)
            except Exception as e:
                print("virtual camera unavailable:", e, "\nFalling back to window.")
                sink = WindowSink(args.out_width, args.out_height)
        else:
            sink = WindowSink(args.out_width, args.out_height)

        t0 = time.time(); frames = 0
        matrix_state = None # Initialize state for the matrix animation

        while True:
            frame = read_frame(cap)

            if args.ascii:
                frame_out, matrix_state = to_ascii_image(
                    frame, 
                    args.out_width, 
                    args.out_height, 
                    args.cols, 
                    args.rows, 
                    args.ascii_mode,
                    matrix_state, # Pass and receive the state
                    rain_cols=args.rain_cols,
                    rain_words=args.rain_words
                )
            else:
                frame_out = cv2.resize(frame, (args.out_width, args.out_height))

            sink.write(frame_out)
            frames += 1
            if frames % (args.fps * 5) == 0:
                dt = time.time() - t0
                print(f"avg fps ~ {frames/dt:.1f}")
    except KeyboardInterrupt:
        pass
    finally:
        try:
            if sink: sink.close()
        finally:
            cap.release()

if __name__ == "__main__":
    sys.exit(main())
