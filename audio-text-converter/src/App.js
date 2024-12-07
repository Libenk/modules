import React, { useState } from "react";

const App = () => {
  const [audioFile, setAudioFile] = useState(null);
  const [textInput, setTextInput] = useState("");
  const [output, setOutput] = useState("");

  // Handler for uploading audio files
  const handleAudioChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioFile(file);
    }
  };

  // Function to simulate converting audio to text
  const convertAudioToText = async () => {
    if (!audioFile) {
      alert("Please upload an audio file.");
      return;
    }

    // Simulate a backend API call
    const formData = new FormData();
    formData.append("audio", audioFile);

    // Example API call (replace URL with your backend endpoint)
    try {
      const response = await fetch("http://127.0.0.1:5000/api/audio-to-text", { 
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setOutput(data.text || "Failed to convert audio to text.");
    } catch (error) {
      console.error("Error converting audio to text:", error);
      setOutput("Error occurred.");
    }
  };

  // Function to simulate converting text to audio
  const convertTextToAudio = async () => {
    if (!textInput) {
      alert("Please enter some text.");
      return;
    }

    // Simulate a backend API call
    try {
      console.log("done");

      const response = await fetch("http://127.0.0.1:5000/api/text-to-audio", { 
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: textInput }),
      });
      console.log("done");
      const blob = await response.blob();
      const audioURL = URL.createObjectURL(blob);
      console.log("done");

      setOutput(
        <audio controls>
          <source src={audioURL} type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      );

    } catch (error) {
      console.error("Error converting text to audio:", error);
      setOutput("Error occurred.");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", padding: "20px" }}>
      <h1>Audio/Text Converter</h1>

      <div>
        <h3>Convert Audio to Text</h3>
        <input
          type="file"
          accept="audio/*"
          onChange={handleAudioChange}
        />
        <button onClick={convertAudioToText}>Convert to Text</button>
      </div>

      <div style={{ marginTop: "20px" }}>
        <h3>Convert Text to Audio</h3>
        <textarea
          rows="4"
          style={{ width: "100%" }}
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          placeholder="Enter text here"
        />
        <button onClick={convertTextToAudio}>Convert to Audio</button>
      </div>

      <div style={{ marginTop: "20px" }}>
        <h3>Output</h3>
        <div>{output}</div>
      </div>
    </div>
  );
};

export default App;