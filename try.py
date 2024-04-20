import numpy as np
import requests
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

# Define the video transformer class
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        super().__init__()
        self.frame = None

    def transform(self, frame):
        self.frame = frame.to_ndarray(format="bgr24")  # Convert frame to ndarray
        return self.frame

# URL of the endpoint
url = "https://master-white-box-cartoonization-psi1104.endpoint.ainize.ai/predict"

# Define the Streamlit app
def main():
    # Set the page title
    st.title("Cartoonizer App")

    # Initialize the video transformer
    video_transformer = VideoTransformer()

    # Start the camera stream
    webrtc_streamer(key="camera", video_transformer_factory=video_transformer)

    # Check if a frame is captured
    if video_transformer.frame is not None:
        # File to upload
        files = {'source': ('frame.png', video_transformer.frame, 'image/png')}

        # Data fields
        data = {'file_type': 'image'}

        # Sending POST request
        response = requests.post(url, files=files, data=data)

        # Check the response
        if response.status_code == 200:
            # Assuming the response content is an image, you can save it
            with open('cartoonized_image.jpg', 'wb') as f:
                f.write(response.content)
            st.success("Image successfully cartoonized and saved as 'cartoonized_image.jpg'")
        else:
            st.error("Error:", response.status_code)

# Run the Streamlit app
if __name__ == "__main__":
    main()
