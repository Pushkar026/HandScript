import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);

  const uploadText = async () => {
    if (!text.trim()) {
      alert("Please enter some text");
      return;
    }

    const formData = new FormData();
    formData.append("text", text);

    const res = await fetch("http://127.0.0.1:8000/api/upload/text", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    console.log("Text upload response:", data);
    alert(`Uploaded! Request ID: ${data.request_id}`);
  };

  const uploadHandwritten = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/api/upload/handwritten", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    console.log("Handwritten upload response:", data);
    alert(`Uploaded! Request ID: ${data.request_id}`);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-xl">
        <h1 className="text-2xl font-bold text-center mb-3">
          Custom Handwriting Converter
        </h1>

        <p className="text-gray-600 text-sm text-center mb-6">
          Upload digital text or a handwritten document. Conversion will be
          added in the next step.
        </p>

        <div className="space-y-6">
          {/* Digital Text Upload */}
          <div>
            <label className="block text-sm font-medium mb-1">
              Digital Text
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={4}
              className="w-full border rounded-lg px-3 py-2"
              placeholder="Type or paste text here..."
            />
            <button
              onClick={uploadText}
              className="mt-2 w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition"
            >
              Upload Digital Text
            </button>
          </div>

          {/* Handwritten Upload */}
          <div>
            <label className="block text-sm font-medium mb-1">
              Handwritten File (PDF / Image)
            </label>
            <input
              type="file"
              accept=".pdf,.jpg,.png"
              onChange={(e) => setFile(e.target.files[0])}
              className="w-full border rounded-lg px-3 py-2"
            />
            <button
              onClick={uploadHandwritten}
              className="mt-2 w-full bg-green-600 text-white py-2 rounded-lg font-semibold hover:bg-green-700 transition"
            >
              Upload Handwritten File
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

