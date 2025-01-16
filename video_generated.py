from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

class VideoEditor:
    def __init__(self, imagemagick_path):
        """
        Initialize the VideoEditor class and configure ImageMagick binary path.

        :param imagemagick_path: Path to the ImageMagick binary
        """
        change_settings({"IMAGEMAGICK_BINARY": imagemagick_path})

    def add_text_to_video(self, video_path, output_path, text, fontsize=50, text_color='white', bg_color='transparent', position='center', duration=10, words_per_line=7, shadow_offset=(1, 1), shadow_color='green'):
        """
        Add a text overlay to a video and save the resulting video. The text is broken into lines after a specified number of words.

        :param video_path: Path to the input video file
        :param output_path: Path to save the output video file
        :param text: The text to overlay on the video
        :param fontsize: Font size of the text
        :param text_color: Color of the text
        :param bg_color: Background color of the text
        :param position: Position of the text on the video
        :param duration: Duration for which the text appears
        :param words_per_line: Number of words per line before breaking to a new line
        """
        try:
            # Split the text into chunks of words
            words = text.split()
            lines = [' '.join(words[i:i + words_per_line]) for i in range(0, len(words), words_per_line)]
            formatted_text = '\n'.join(lines)  # Join the lines with newlines

            # Load the video
            video = VideoFileClip(video_path)

            # Create a text clip with the formatted text
            shadow_clip = TextClip(formatted_text, fontsize=fontsize, color=shadow_color, bg_color=bg_color, size=video.size)
            shadow_clip = shadow_clip.set_position((position[0] + shadow_offset[0], position[1] + shadow_offset[1])).set_duration(duration)

            # Create the main text clip
            text_clip = TextClip(formatted_text, fontsize=fontsize, color=text_color, bg_color=bg_color, size=video.size)
            text_clip = text_clip.set_position(position).set_duration(duration)

            # Combine the shadow and text clips with the video
            video_with_text = CompositeVideoClip([video, shadow_clip, text_clip])

            # Write the output video file
            video_with_text.write_videofile(output_path, fps=video.fps)

            print(f"Video saved to {output_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
