import cv2
import textwrap

class VideoTextOverlay:
    def __init__(self, video_path, output_path, font_scale=1, text_color=(255, 255, 255), font_thickness=2, shadow_color=(0, 0, 0), shadow_offset=(2, 2)):
        """
        Initialize the VideoTextOverlay class.

        :param video_path: Path to the input video
        :param output_path: Path to save the output video
        :param font_scale: Scale of the text font
        :param text_color: Color of the text (BGR format)
        :param font_thickness: Thickness of the text font
        :param shadow_color: Color of the shadow (BGR format)
        :param shadow_offset: Offset of the shadow (x, y)
        """
        self.video_path = video_path
        self.output_path = output_path
        self.font_scale = font_scale
        self.text_color = text_color
        self.font_thickness = font_thickness
        self.shadow_color = shadow_color
        self.shadow_offset = shadow_offset

        # Open the video file
        self.cap = cv2.VideoCapture(video_path)

        # Get video properties
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create a VideoWriter object
        self.out = cv2.VideoWriter(
            output_path, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.frame_width, self.frame_height)
        )

    def _wrap_text(self, text):
        """
        Wrap text to fit within the video frame width.

        :param text: The text to wrap
        :return: A list of wrapped text lines
        """
        # max_line_width = int(self.frame_width / (self.font_scale * 10))
        return textwrap.wrap(text, width=40)

    def _calculate_text_position(self, wrapped_text):
        """
        Calculate the starting y-coordinate for the text block.

        :param wrapped_text: A list of wrapped text lines
        :return: Starting y-coordinate for the text block
        """
        text_height = cv2.getTextSize("Test", cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, self.font_thickness)[0][1]
        line_spacing = 9
        text_block_height = len(wrapped_text) * (text_height + line_spacing) - line_spacing
        return max(self.frame_height - text_block_height - 20, 20)  # Bottom margin of 20px

    def add_text(self, text, duration=10):
        """
        Add text with shadow to the bottom center of the video.

        :param text: The text to overlay
        :param duration: Duration for which the text appears (in seconds)
        """
        wrapped_text = self._wrap_text(text)
        y_start = self._calculate_text_position(wrapped_text)
        text_frames = int(duration * self.fps)

        frame_count = 0

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_count += 1

            if frame_count <= text_frames:
                y = y_start
                for line in wrapped_text:
                    text_size = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, self.font_thickness)[0]
                    x = (self.frame_width - text_size[0]) // 2

                    # Draw shadow
                    cv2.putText(
                        frame, line, 
                        (x + self.shadow_offset[0], y + self.shadow_offset[1]), 
                        cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, self.shadow_color, self.font_thickness, cv2.LINE_AA
                    )

                    # Draw main text
                    cv2.putText(
                        frame, line, 
                        (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, self.text_color, self.font_thickness, cv2.LINE_AA
                    )

                    y += text_size[1] + 9

            self.out.write(frame)

        self.cap.release()
        self.out.release()