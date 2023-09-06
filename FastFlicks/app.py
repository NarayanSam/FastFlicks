from flask import Flask, render_template, request,jsonify
from pytube import YouTube
import os
import speech_recognition as sr
import assemblyai as aai

aai.settings.api_key = "cda6c282a0d84cf6b1cde545b6ce960a"
transcriber = aai.Transcriber()

app = Flask(__name__,static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
    url = request.form['url']
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()

    destination = "C:/Youtube"
    out_file = video.download(output_path=destination)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.wav'
    os.rename(out_file, new_file)

    transcript = transcriber.transcribe(
        new_file,
        config=aai.TranscriptionConfig(
            summarization=True,
            summary_model=aai.SummarizationModel.informative,
            summary_type=aai.SummarizationType.bullets
        )
    )
    #summary = transcript.summary
    #return render_template('result.html', title=yt.title, summary=summary)
    if transcript and transcript.status == 'completed':
        summary = transcript.summary
        #return jsonify({'status': 'completed', 'summary': summary})
        return render_template('result.html', title=yt.title, summary=summary)
    else:
    #    return jsonify({'status': 'in_progress'})
         return render_template('result.html', title=yt.title, summary="Error")
#
if __name__ == '__main__':
    app.run(debug=True)
