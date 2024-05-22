import shutil
from customtkinter import filedialog

def add_subtitle_to_video():
    
    copied_video = mainApp.copied_video
    video_input_stream = ffmpeg.input(copied_video)
    subtitle_input_stream = ffmpeg.input(ass_file)
    subtitle_track_title = ass_file.replace(".ass", "")
    
    soft_subtitle = False
    subtitle_language = 'en'
    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
            "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
        ffmpeg.run(stream, overwrite_output=True)
        print("successfully added soft subtitles")
        
    else:
        # Add hard subtitles
        stream = ffmpeg.output(video_input_stream, output_video,
                               vf=f"subtitles={ass_file}")
        ffmpeg.run(stream, overwrite_output=True)
        print("successfully added hard subtitles")

    # Prompt user for output location after adding subtitles
    output_filename = filedialog.asksavefilename(
        defaulterrortitle="Please choose a location",
        initialfile=f"output-{copied_video}.mp4",
        title="Save Output Video",
        filetypes=[("MP4 files", "*.mp4")]
    )

    # Check if user selected a filename
    if output_filename:
        # Move the output video to the chosen location using shutil.move
        shutil.move(output_video, output_filename)
        print(f"Output video saved to: {output_filename}")
    else:
        print("Output video generation cancelled.")
