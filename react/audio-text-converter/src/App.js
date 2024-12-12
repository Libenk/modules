import React, { useState } from "react";

const App = () => {
  const [textInput, setTextInput] = useState("");
  const [audioSrc, setAudioSrc] = useState(null);
  const [loading, setLoading] = useState(false);
  const [transcription, setTranscription] = useState("");  // To store the transcription result
  const [audioFile, setAudioFile] = useState(null);

  const handleTextChange = (e) => {
    setTextInput(e.target.value);
  };

  const handleGenerateAudio = async () => {
    if (!textInput) {
      alert("Please enter some text.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("https://coverters-c26f1d7e1762.herokuapp.com/text-to-audio/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: textInput, voice: 1 }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const audioUrl = URL.createObjectURL(blob);
        setAudioSrc(audioUrl);
      } else {
        console.error("Failed to generate audio:", response.statusText);
        alert("Error generating audio.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error generating audio.");
    }

    setLoading(false);
  };

  const handleDownloadAudio = () => {
    if (!audioSrc) {
      alert("No audio generated yet.");
      return;
    }

    const link = document.createElement("a");
    link.href = audioSrc;
    link.download = "output.mp3";
    link.click();
  };

  const handleAudioChange = (e) => {
    const file = e.target.files[0];
    setAudioFile(file);
  };

  const handleTranscribeAudio = async () => {
    if (!audioFile) {
      alert("Please upload an audio file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", audioFile);

    setLoading(true);
    try {
      const response = await fetch("https://coverters-c26f1d7e1762.herokuapp.com/audio-to-text/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setTranscription(data.transcription);  // Set the transcribed text
      } else {
        const errorData = await response.json();
        alert(errorData.error || "Error transcribing audio.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error transcribing audio.");
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", padding: "20px" }}>
      <h1>Text-to-Audio and Audio-to-Text Converter</h1>

      <div>
        <h3>Enter Text</h3>
        <textarea
          rows="4"
          style={{ width: "100%" }}
          value={textInput}
          onChange={handleTextChange}
          placeholder="Enter text here"
        />
      </div>

      <div style={{ marginTop: "20px" }}>
        <button onClick={handleGenerateAudio} disabled={loading}>
          {loading ? "Generating..." : "Generate Audio"}
        </button>
      </div>

      {audioSrc && (
        <div style={{ marginTop: "20px" }}>
          <h3>Play Audio</h3>
          <audio controls>
            <source src={audioSrc} type="audio/mp3" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}

      {audioSrc && (
        <div style={{ marginTop: "20px" }}>
          <button onClick={handleDownloadAudio}>Download Audio</button>
        </div>
      )}

      {/* New Section for Audio-to-Text */}
      <div style={{ marginTop: "30px" }}>
        <h3>Upload MP3 to Transcribe</h3>
        <input type="file" accept="audio/mp3" onChange={handleAudioChange} />
        <button onClick={handleTranscribeAudio} disabled={loading}>
          {loading ? "Transcribing..." : "Transcribe Audio"}
        </button>
        {transcription && (
          <div style={{ marginTop: "20px" }}>
            <h4>Transcription:</h4>
            <p>{transcription}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
