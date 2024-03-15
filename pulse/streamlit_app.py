import streamlit as st
from lib.device import Camera
from lib.processors_noopenmdao import findFaceGetPulse
import numpy as np

class PulseApp:
    def __init__(self):
        self.camera = Camera(camera=0)  # Initialize camera
        self.processor = findFaceGetPulse(bpm_limits=[70, 160],
                                          data_spike_limit=2500.,
                                          face_detector_smoothness=10.)
        self.bpm_plot = True
        self.running = True

    def main(self):
        st.title("Webcam Pulse Detector")

        self.bpm_plot = st.checkbox("Show BPM Plot", value=self.bpm_plot)

        if not self.running:
            if st.button("Start"):
                self.running = False
        else:
            if st.button("Stop"):
                self.running = False

        while self.running:
            frame = self.camera.get_frame()
            h, w, _ = frame.shape

            self.processor.frame_in = frame
            self.processor.run(0)  # 0 as selected camera index
            output_frame = self.processor.frame_out

            st.image(output_frame, channels="BGR", width=None)  # Full width

            if self.bpm_plot:
                self.make_bpm_plot()

    def make_bpm_plot(self):
        plot_title = "Data display - raw signal (top) and PSD (bottom)"

if __name__ == "__main__":
    app = PulseApp()
    app.main()
