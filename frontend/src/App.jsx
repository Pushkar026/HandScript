import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [font, setFont] = useState("handwriting");
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const [showFontModal, setShowFontModal] = useState(false);
  const [handwritingFile, setHandwritingFile] = useState(null);
  const [handwritingLoading, setHandwritingLoading] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL;

  // -------------------------------
  // Convert text to handwriting
  // -------------------------------
  const uploadTextAndConvert = async () => {
    if (!text.trim()) {
      alert("Please enter some text");
      return;
    }

    try {
      setLoading(true);
      setImageUrl(null);

      const uploadRes = await fetch(`${API_URL}/api/upload/text`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      const uploadData = await uploadRes.json();

      const convertRes = await fetch(`${API_URL}/api/convert`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          file_id: uploadData.file_id,
          file_type: "text",
          font_key: font,
        }),
      });

      const convertData = await convertRes.json();

setImageUrl(convertData.image_url);
    } catch (error) {
      console.error(error);
      alert("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  // -------------------------------
  // Upload custom handwriting template
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
        `${API_URL}/api/upload/handwriting`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!res.ok) {
        throw new Error("Upload failed");
      }

      alert("Template uploaded successfully!");

      setShowFontModal(false);
      setHandwritingFile(null);
    } catch (error) {
      console.error(error);
      alert("Failed to upload template");
    } finally {
      setHandwritingLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-6 py-10">
      {/* Hero Section */}
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">

          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            HandScript
          </h1>

          <p className="text-slate-400 max-w-2xl mx-auto text-lg leading-relaxed">
            Convert digital text into realistic handwritten notes
            with elegant handwriting styles.
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl">
          {/* Header */}
          <div className="flex justify-between items-center mb-5">
            <h2 className="text-2xl font-semibold">
              Text Input
            </h2>

            <span className="text-slate-400 text-sm">
              {text.length} characters
            </span>
          </div>

          {/* Textarea */}
          <textarea
            placeholder="Type or paste your text here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={10}
            className="
              w-full
              bg-slate-800
              border border-slate-700
              rounded-2xl
              p-5
              text-white
              placeholder-slate-400
              resize-none
              focus:outline-none
              focus:ring-2
              focus:ring-indigo-500
              text-base
              leading-relaxed
              mb-6
            "
          />

          {/* Controls */}
          <div className="flex flex-col lg:flex-row gap-5 justify-between mb-6">
            {/* Select */}
            <div className="flex-1">
              <label className="block mb-3 text-slate-300">
                Handwriting Style
              </label>

              <select
                value={font}
                onChange={(e) => setFont(e.target.value)}
                className="
                  w-full
                  bg-slate-800
                  border border-slate-700
                  rounded-xl
                  p-4
                  text-white
                  focus:outline-none
                  focus:ring-2
                  focus:ring-indigo-500
                "
              >
                <option value="handwriting">
                  Classic Handwriting
                </option>

                <option value="calibri">
                  Calibri
                </option>

                <option value="arial">
                  Arial
                </option>

                <option value="palscript">
                  Pal Script
                </option>

                <option value="chiller">
                  Chiller
                </option>

                <option value="rage">
                  Rage
                </option>
              </select>
            </div>

            {/* Buttons */}
            <div className="flex flex-wrap items-end gap-3">
              <button
                onClick={() =>
                  setShowFontModal(true)
                }
                className="
                  px-5 py-4
                  rounded-xl
                  bg-slate-800
                  border border-slate-700
                  hover:bg-slate-700
                  transition
                "
              >
                Custom Font
              </button>

              <a
                href={`${API_URL}/static/handwriting_template_v1.pdf`}
                target="_blank"
                rel="noreferrer"
                className="
                  px-5 py-4
                  rounded-xl
                  bg-blue-600
                  hover:bg-blue-500
                  transition
                "
              >
                Download Template
              </a>
            </div>
          </div>

          {/* Generate Button */}
          <button
            onClick={uploadTextAndConvert}
            disabled={loading}
            className="
              w-full
              py-4
              rounded-2xl
              bg-gradient-to-r
              from-indigo-600
              to-purple-600
              hover:opacity-90
              transition
              font-semibold
              text-lg
            "
          >
            {loading
              ? "Generating Handwriting..."
              : "Generate Handwriting"}
          </button>
        </div>

        {/* Result */}
        {imageUrl && (
          <div className="mt-10 bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl">
            <h2 className="text-2xl font-semibold mb-6">
              Generated Output
            </h2>

            <img
              src={imageUrl}
              alt="Handwritten Output"
              className="
                w-full
                rounded-2xl
                border border-slate-700
                mb-6
              "
            />

            <a
              href={imageUrl}
              download
              className="
                inline-block
                px-6 py-4
                rounded-xl
                bg-emerald-600
                hover:bg-emerald-500
                transition
              "
            >
              Download Image
            </a>
          </div>
        )}
      </div>

      {/* Modal */}
      {showFontModal && (
        <div
          className="
            fixed inset-0
            bg-black/70
            flex justify-center items-center
            p-4
            z-50
          "
        >
          <div
            className="
              w-full max-w-lg
              bg-slate-900
              border border-slate-800
              rounded-3xl
              p-8
            "
          >
            <h2 className="text-3xl font-bold mb-4">
              Create Custom Font
            </h2>

            <p className="text-slate-400 leading-relaxed mb-6">
              Upload the completed handwriting template.
              <br />
              Use a black pen and write one
              character per box.
            </p>

            <input
              type="file"
              accept=".png,.jpg,.jpeg,.pdf"
              onChange={(e) =>
                setHandwritingFile(
                  e.target.files[0]
                )
              }
              className="
                w-full
                mb-6
                text-slate-300
              "
            />

            <div className="flex justify-end gap-3">
              <button
                onClick={() =>
                  setShowFontModal(false)
                }
                className="
                  px-5 py-3
                  rounded-xl
                  border border-slate-700
                  bg-slate-800
                  hover:bg-slate-700
                  transition
                "
              >
                Cancel
              </button>

              <button
                onClick={
                  uploadHandwritingTemplate
                }
                disabled={handwritingLoading}
                className="
                  px-5 py-3
                  rounded-xl
                  bg-emerald-600
                  hover:bg-emerald-500
                  transition
                "
              >
                {handwritingLoading
                  ? "Uploading..."
                  : "Upload Template"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;



