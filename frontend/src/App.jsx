import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [font, setFont] = useState("handwriting");
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  // Custom handwriting upload states
  const [showFontModal, setShowFontModal] = useState(false);
  const [handwritingFile, setHandwritingFile] = useState(null);
  const [handwritingLoading, setHandwritingLoading] = useState(false);

  // -------------------------------
  // Text → Handwriting conversion
  // -------------------------------
  const uploadTextAndConvert = async () => {
    if (!text.trim()) {
      alert("Please enter some text");
      return;
    }

    try {
      setLoading(true);
      setImageUrl(null);

      const uploadRes = await fetch(
        "http://127.0.0.1:8000/api/upload/text",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
        }
      );

      const uploadData = await uploadRes.json();
      const fileId = uploadData.file_id;

      const convertRes = await fetch(
        "http://127.0.0.1:8000/api/convert",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            file_id: fileId,
            file_type: "text",
            font_key: font,
          }),
        }
      );

      const convertData = await convertRes.json();

      setImageUrl(
        `http://127.0.0.1:8000/outputs/${convertData.output_id}.png`
      );
    } catch (err) {
      console.error(err);
      alert("Something went wrong. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  // -------------------------------
  // Upload handwriting template
  // -------------------------------
  const uploadHandwritingTemplate = async () => {
    if (!handwritingFile) {
      alert("Please select a file");
      return;
    }

    try {
      setHandwritingLoading(true);

      const formData = new FormData();
      formData.append("file", handwritingFile);

      const res = await fetch(
        "http://127.0.0.1:8000/api/upload/handwriting",
        {
          method: "POST",
          body: formData, // no headers
        }
      );

      if (!res.ok) {
        throw new Error("Upload failed");
      }

      const data = await res.json();
      console.log("Handwriting template file ID:", data.file_id);

      alert("Handwriting template uploaded successfully!");

      setShowFontModal(false);
      setHandwritingFile(null);
    } catch (err) {
      console.error(err);
      alert("Failed to upload handwriting template");
    } finally {
      setHandwritingLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Custom Handwriting Converter</h1>

      <textarea
        placeholder="Enter text to convert..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={6}
      />

      <div className="font-row">
        <select value={font} onChange={(e) => setFont(e.target.value)}>
          <option value="handwriting">Handwriting</option>
          <option value="calibri">Calibri</option>
          <option value="arial">Arial</option>
          <option value="palscript">Pal Script</option>
          <option value="chiller">Chiller</option>
          <option value="rage">Rage</option>
        </select>

        <button onClick={() => setShowFontModal(true)}>
          Create Custom Font
        </button>

        <a
          href="http://127.0.0.1:8000/static/handwriting_template_v1.pdf"
          target="_blank"
          rel="noreferrer"
          className="download-template"
        >
          Download Template
        </a>
      </div>

      <button onClick={uploadTextAndConvert} disabled={loading}>
        {loading ? "Converting..." : "Convert to Handwriting"}
      </button>

      {imageUrl && (
        <div className="output">
          <h2>Result</h2>
          <img src={imageUrl} alt="Handwritten Output" />
          <a href={imageUrl} download>
            Download Image
          </a>
        </div>
      )}

      {/* Custom Font Modal */}
      {showFontModal && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>Create Custom Font</h2>

            <p className="modal-text">
              Upload the handwriting template filled with:
              <br />
              A–Z and a–z
              <br />
              Use black pen. One character per box.
            </p>

            <input
              type="file"
              accept=".png,.jpg,.jpeg,.pdf"
              onChange={(e) => setHandwritingFile(e.target.files[0])}
            />

            <div className="modal-actions">
              <button onClick={() => setShowFontModal(false)}>
                Cancel
              </button>
              <button
                onClick={uploadHandwritingTemplate}
                disabled={handwritingLoading}
              >
                {handwritingLoading ? "Uploading..." : "Upload"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;



