import { useEffect, useRef, useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const [prediction, setPrediction] = useState("Waiting...");
  const [confidence, setConfidence] = useState(0);
  const [accuracy, setAccuracy] = useState(0);
  const [totalPredictions, setTotalPredictions] = useState(0);
  const [highConfidencePredictions, setHighConfidencePredictions] = useState(0)
  const [practiceLetter, setPracticeLetter] = useState("A");
  const [practiceScore, setPracticeScore] = useState(0);
  const [practiceAttempts, setPracticeAttempts] = useState(0);
  const [assessmentQuestion, setAssessmentQuestion] = useState(0);
  const [assessmentScore, setAssessmentScore] = useState(0);
  const [assessmentActive, setAssessmentActive] = useState(false);
  const [assessmentComplete, setAssessmentComplete] = useState(false);


  const [loading, setLoading] = useState(false);

  // Webcam states
  const [cameraActive, setCameraActive] = useState(false);
  const [cameraLoading, setCameraLoading] = useState(false);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const intervalRef = useRef(null);
  const checkPractice = () => {
    if (!prediction || prediction === "Waiting...") {
      return;
    }

    const predicted = prediction.toUpperCase();
    const target = practiceLetter.toUpperCase();

    setPracticeAttempts((prev) => prev + 1);

    if (predicted.includes(target)) {
      setPracticeScore((prev) => prev + 1);

      const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
      const nextLetter = letters[Math.floor(Math.random() * letters.length)];
      setPracticeLetter(nextLetter);
    }
  };
  // --------------------------------------------------
  // ASSESSMENT MODE
  // --------------------------------------------------

  const startAssessment = () => {
    setAssessmentQuestion(1);
    setAssessmentScore(0);
    setAssessmentActive(true);
    setAssessmentComplete(false);

    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const randomLetter =
      letters[Math.floor(Math.random() * letters.length)];

    setPracticeLetter(randomLetter);
  };

  const checkAssessment = () => {
    if (!prediction || prediction === "Waiting...") {
      return;
    }

    const predicted = prediction.toUpperCase();
    const target = practiceLetter.toUpperCase();

    const isCorrect = predicted.includes(target);

    if (isCorrect) {
      setAssessmentScore((prev) => prev + 1);
    }

    if (assessmentQuestion >= 10) {
      setAssessmentActive(false);
      setAssessmentComplete(true);
      return;
    }

    setAssessmentQuestion((prev) => prev + 1);

    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const nextLetter =
      letters[Math.floor(Math.random() * letters.length)];

    setPracticeLetter(nextLetter);
  };

  const resetAssessment = () => {
    setAssessmentQuestion(0);
    setAssessmentScore(0);
    setAssessmentActive(false);
    setAssessmentComplete(false);
  };
  // --------------------------------------------------
  // IMAGE UPLOAD
  // --------------------------------------------------

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    if (!selectedFile) return;

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));

    setPrediction("Ready to predict");
    setConfidence(0);
  };

  // --------------------------------------------------
  // IMAGE PREDICTION
  // --------------------------------------------------

  const testPrediction = async () => {
    if (!file) {
      setPrediction("Please select an image");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        "http://localhost:8000/gesture/predict",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Prediction request failed");
      }

      const data = await response.json();

      const predictedLabel = data.predicted_label || "Unknown";
      const predictedConfidence = data.confidence || 0;

      setPrediction(predictedLabel);
      setConfidence(predictedConfidence);

      setTotalPredictions((prev) => prev + 1);

      if (predictedConfidence >= 0.7) {
        setHighConfidencePredictions((prev) => prev + 1);
      }

      
    } catch (error) {
      console.error(error);
      setPrediction("Backend connection failed");
    }

    setLoading(false);
  };

  // --------------------------------------------------
  // STATISTICS
  // --------------------------------------------------

  

  // --------------------------------------------------
  // START CAMERA
  // --------------------------------------------------

  const startCamera = async () => {
    try {
      setCameraLoading(true);

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: 640,
          height: 480,
        },
        audio: false,
      });

      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      setCameraActive(true);
      setPrediction("Camera ready");
    } catch (error) {
      console.error("Camera error:", error);

      setPrediction("Unable to access camera");
      alert(
        "Camera access was denied or the camera is unavailable."
      );
    }

    setCameraLoading(false);
  };

  // --------------------------------------------------
  // STOP CAMERA
  // --------------------------------------------------

  const stopCamera = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => {
        track.stop();
      });

      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setCameraActive(false);
    setPrediction("Camera stopped");
  };

  // --------------------------------------------------
  // CAPTURE FRAME FROM WEBCAM
  // --------------------------------------------------

  const captureFrame = () => {
    if (
      !videoRef.current ||
      !canvasRef.current ||
      !cameraActive
    ) {
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");

    context.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height
    );

    canvas.toBlob(
      async (blob) => {
        if (!blob) return;

        const formData = new FormData();

        formData.append(
          "file",
          blob,
          "webcam-frame.jpg"
        );

        try {
          const response = await fetch(
            "http://localhost:8000/gesture/predict",
            {
              method: "POST",
              body: formData,
            }
          );

          if (!response.ok) {
            return;
          }

          const data = await response.json();

          const predictedLabel =
            data.predicted_label || "Unknown";

          const predictedConfidence =
            data.confidence || 0;

          setAccuracy(data.accuracy || 0);

          console.log("Expected:", data.expected);
          console.log("Correct:", data.correct);

          setPrediction(predictedLabel);
          setConfidence(predictedConfidence);

          setTotalPredictions((prev) => prev + 1);

          if (predictedConfidence >= 0.5) {
              setHighConfidencePredictions((prev) => prev + 1);
          }

          if (data.correct === true) {
              setCorrectPredictions((prev) => prev + 1);
          }

          
        } catch (error) {
          console.error(
            "Webcam prediction error:",
            error
          );
        }
      },
      "image/jpeg",
      0.8
    );
  };

  // --------------------------------------------------
  // START LIVE PREDICTION
  // --------------------------------------------------

  const startLivePrediction = () => {
    if (!cameraActive) return;

    if (intervalRef.current) {
      return;
    }

    // Capture approximately every 700 ms
    intervalRef.current = setInterval(() => {
      captureFrame();
    }, 700);

    setPrediction("Live prediction started");
  };

  // --------------------------------------------------
  // STOP LIVE PREDICTION
  // --------------------------------------------------

  const stopLivePrediction = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    setPrediction("Live prediction stopped");
  };

  // --------------------------------------------------
  // CLEANUP
  // --------------------------------------------------

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }

      if (streamRef.current) {
        streamRef.current
          .getTracks()
          .forEach((track) => track.stop());
      }
    };
  }, []);

  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (
    <div style={styles.page}>
      <div style={styles.container}>

        {/* HEADER */}
        <header style={styles.header}>
          <h1 style={styles.title}>
            AI Sign Language Learning Platform
          </h1>

          <p style={styles.subtitle}>
            Learn and practice sign language using AI
          </p>
        </header>


        {/* MAIN WORKSPACE */}
        <div style={styles.workspace}>

          {/* ================= PRACTICE ================= */}
          <div style={styles.card}>
            <h2>🎯 Practice Mode</h2>

            <p style={styles.description}>
              Make the sign shown below using your hand.
            </p>

            <div style={styles.targetLetter}>
              {practiceLetter}
            </div>

            <button
              onClick={checkPractice}
              disabled={!cameraActive}
              style={styles.button}
            >
              Check My Sign
            </button>

            <div style={styles.score}>
              Score: <strong>{practiceScore}</strong> /{" "}
              {practiceAttempts}
            </div>
          </div>


          {/* ================= CAMERA ================= */}
          <div style={styles.card}>
            <div style={styles.cardHeader}>
              <div>
                <h2>📷 Live Sign Recognition</h2>
                <p style={styles.description}>
                  Use your webcam to practice in real time.
                </p>
              </div>

              <span
                style={{
                  ...styles.statusBadge,
                  background: cameraActive
                    ? "rgba(34,197,94,0.15)"
                    : "rgba(239,68,68,0.15)",
                  color: cameraActive
                    ? "#4ade80"
                    : "#f87171",
                }}
              >
                {cameraActive ? "● LIVE" : "● OFF"}
              </span>
            </div>

            <div style={styles.videoContainer}>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                style={styles.video}
              />

              {!cameraActive && (
                <div style={styles.cameraPlaceholder}>
                  <span style={styles.cameraIcon}>
                    📷
                  </span>

                  <p>Camera is currently off</p>
                </div>
              )}
            </div>

            <canvas
              ref={canvasRef}
              style={{ display: "none" }}
            />

            <div style={styles.cameraButtons}>

              {!cameraActive ? (
                <button
                  onClick={startCamera}
                  disabled={cameraLoading}
                  style={styles.cameraButton}
                >
                  {cameraLoading
                    ? "Starting..."
                    : "Start Camera"}
                </button>
              ) : (
                <button
                  onClick={stopCamera}
                  style={styles.stopButton}
                >
                  Stop Camera
                </button>
              )}

              {cameraActive && (
                <>
                  <button
                    onClick={startLivePrediction}
                    style={styles.button}
                  >
                    ▶️ Start Recognition
                  </button>

                  <button
                    onClick={stopLivePrediction}
                    style={styles.secondaryButton}
                  >
                    ⏸️ Stop Recognition
                  </button>
                </>
              )}

            </div>
          </div>


          {/* ================= ASSESSMENT ================= */}
          <div style={styles.card}>
            <h2>📝 Assessment Mode</h2>

            {!assessmentActive && !assessmentComplete && (
              <>
                <p style={styles.description}>
                  Test your sign language recognition skills
                  with 10 random questions.
                </p>

                <button
                  onClick={startAssessment}
                  style={styles.button}
                >
                  Start Assessment
                </button>
              </>
            )}

            {assessmentActive && (
              <>
                <div style={styles.assessmentProgress}>
                  Question {assessmentQuestion} / 10
                </div>

                <div style={styles.targetLetterSmall}>
                  {practiceLetter}
                </div>

                <p style={styles.description}>
                  Make the sign shown above using your hand.
                </p>

                <button
                  onClick={checkAssessment}
                  disabled={!cameraActive}
                  style={styles.button}
                >
                  Check Answer
                </button>

                <div style={styles.score}>
                  Current Score:{" "}
                  <strong>{assessmentScore}</strong> /{" "}
                  {assessmentQuestion - 1}
                </div>
              </>
            )}

            {assessmentComplete && (
              <div style={styles.assessmentComplete}>

                <div style={styles.completeIcon}>
                  🎉
                </div>

                <h2>Assessment Complete!</h2>

                <div style={styles.finalScore}>
                  {assessmentScore} / 10
                </div>

                <p>
                  Accuracy:{" "}
                  <strong>
                    {(assessmentScore / 10) * 100}%
                  </strong>
                </p>

                <button
                  onClick={resetAssessment}
                  style={styles.secondaryButton}
                >
                  Try Again
                </button>

              </div>
            )}
          </div>


          {/* ================= IMAGE PREDICTION ================= */}
          <div style={styles.card}>
            <h2>🤟 Gesture Prediction</h2>

            <p style={styles.description}>
              Upload a sign image and let the AI identify it.
            </p>

            <label style={styles.upload}>
              Choose Sign Image

              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                style={{ display: "none" }}
              />
            </label>

            {file && (
              <p style={styles.filename}>
                Selected: {file.name}
              </p>
            )}

            {preview && (
              <img
                src={preview}
                alt="Selected sign"
                style={styles.preview}
              />
            )}

            <div>
              <button
                onClick={testPrediction}
                disabled={loading}
                style={styles.button}
              >
                {loading
                  ? "Predicting..."
                  : "Test Prediction"}
              </button>
            </div>
          </div>

        </div>


        {/* ================= AI FEEDBACK ================= */}
        <div style={styles.feedback}>

          <div>
            <span style={styles.feedbackIcon}>🧠</span>
            <h3>AI Feedback</h3>
          </div>

          <p>
            {prediction === "Waiting..."
              ? "Upload a sign image or start the camera to begin."
              : prediction === "Ready to predict"
              ? "Click Test Prediction to analyze your sign."
              : `The AI predicted: ${prediction}`}
          </p>

        </div>


        {/* ================= LIVE RESULTS ================= */}
        <div style={styles.dashboard}>

          <div style={styles.statCard}>
            <span style={styles.statIcon}>🤟</span>
            <h3>Current Gesture</h3>

            <p style={styles.value}>
              {prediction}
            </p>
          </div>

          <div style={styles.statCard}>
            <span style={styles.statIcon}>🎯</span>
            <h3>Confidence</h3>

            <p style={styles.value}>
              {(confidence * 100).toFixed(0)}%
            </p>
          </div>

          <div style={styles.statCard}>
            <span style={styles.statIcon}>📈</span>
            <h3>Accuracy</h3>

            <p style={styles.value}>
              {accuracy.toFixed(0)}%
            </p>
          </div>

        </div>


        {/* ================= SESSION STATISTICS ================= */}
        <div style={styles.sessionCard}>

          <h2>📊 Session Statistics</h2>

          <div style={styles.sessionGrid}>

            <div>
              <span style={styles.sessionNumber}>
                {cameraActive ? "ACTIVE" : "OFF"}
              </span>

              <p>Camera Status</p>
            </div>

            <div>
              <span style={styles.sessionNumber}>
                {totalPredictions}
              </span>

              <p>Total Predictions</p>
            </div>

            <div>
              <span style={styles.sessionNumber}>
                {highConfidencePredictions}
              </span>

              <p>High-Confidence Predictions</p>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
// ======================================================
// STYLES
// ======================================================

const styles = {

  page: {
    minHeight: "100vh",
    background:
      "linear-gradient(135deg, #07111f 0%, #0b1f3a 45%, #123b68 100%)",
    color: "#f8fafc",
    padding: "22px 18px",
    fontFamily: "Inter, Arial, sans-serif",
    boxSizing: "border-box",
  },

  container: {
    width: "100%",
    maxWidth: "1180px",
    margin: "0 auto",
  },

  header: {
    textAlign: "center",
    marginBottom: "20px",
  },

  title: {
    fontSize: "32px",
    fontWeight: "700",
    margin: "0 0 5px",
    letterSpacing: "-0.6px",
  },

  subtitle: {
    fontSize: "14px",
    color: "#9fb3c8",
    margin: 0,
  },


  /* ================= MAIN GRID ================= */

  workspace: {
    display: "grid",
    gridTemplateColumns: "1fr 1.35fr",
    gap: "14px",
    alignItems: "stretch",
  },


  /* ================= CARDS ================= */

  card: {
    background:
      "linear-gradient(145deg, rgba(18,42,70,0.92), rgba(10,28,50,0.92))",
    borderRadius: "16px",
    padding: "18px",
    border:
      "1px solid rgba(148,163,184,0.15)",
    boxShadow:
      "0 10px 30px rgba(0,0,0,0.18)",
    boxSizing: "border-box",
  },

  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: "10px",
  },


  /* ================= TEXT ================= */

  description: {
    color: "#9fb3c8",
    fontSize: "13px",
    lineHeight: "1.5",
    margin: "7px 0 12px",
  },


  /* ================= PRACTICE ================= */

  targetLetter: {
    fontSize: "72px",
    fontWeight: "700",
    color: "#60a5fa",
    margin: "20px 0",
    textShadow:
      "0 0 25px rgba(96,165,250,0.25)",
  },

  targetLetterSmall: {
    fontSize: "55px",
    fontWeight: "700",
    color: "#60a5fa",
    margin: "12px 0",
  },

  score: {
    marginTop: "12px",
    color: "#cbd5e1",
    fontSize: "14px",
  },

  assessmentProgress: {
    display: "inline-block",
    background: "rgba(96,165,250,0.12)",
    color: "#93c5fd",
    borderRadius: "20px",
    padding: "5px 12px",
    fontSize: "12px",
    marginTop: "8px",
  },

  assessmentComplete: {
    textAlign: "center",
    padding: "5px",
  },

  completeIcon: {
    fontSize: "40px",
  },

  finalScore: {
    fontSize: "44px",
    fontWeight: "700",
    color: "#4ade80",
    margin: "8px 0",
  },


  /* ================= BUTTONS ================= */

  button: {
    padding: "10px 18px",
    border: "none",
    borderRadius: "9px",
    background: "#2563eb",
    color: "white",
    fontSize: "13px",
    fontWeight: "600",
    cursor: "pointer",
    transition: "0.2s",
  },

  secondaryButton: {
    padding: "10px 18px",
    border: "none",
    borderRadius: "9px",
    background: "#334155",
    color: "white",
    fontSize: "13px",
    fontWeight: "600",
    cursor: "pointer",
  },


  /* ================= IMAGE UPLOAD ================= */

  upload: {
    display: "inline-block",
    background: "#2563eb",
    padding: "9px 16px",
    borderRadius: "9px",
    cursor: "pointer",
    fontSize: "13px",
    fontWeight: "600",
  },

  filename: {
    color: "#94a3b8",
    fontSize: "12px",
    margin: "8px 0",
  },

  preview: {
    width: "140px",
    height: "140px",
    objectFit: "cover",
    borderRadius: "12px",
    marginTop: "8px",
    border:
      "2px solid rgba(96,165,250,0.6)",
  },


  /* ================= CAMERA ================= */

  cameraDescription: {
    color: "#9fb3c8",
    fontSize: "13px",
    margin: "5px 0 10px",
  },

  videoContainer: {
    width: "100%",
    maxWidth: "560px",
    aspectRatio: "4 / 3",
    margin: "0 auto",
    borderRadius: "13px",
    overflow: "hidden",
    background: "#020617",
    border:
      "1px solid rgba(96,165,250,0.35)",
    position: "relative",
  },

  video: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    display: "block",
  },

  cameraPlaceholder: {
    position: "absolute",
    inset: 0,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    color: "#64748b",
  },

  cameraIcon: {
    fontSize: "38px",
    marginBottom: "6px",
  },

  cameraButtons: {
    marginTop: "10px",
    display: "flex",
    justifyContent: "center",
    gap: "7px",
    flexWrap: "wrap",
  },

  cameraButton: {
    padding: "10px 18px",
    border: "none",
    borderRadius: "9px",
    background: "#2563eb",
    color: "white",
    fontSize: "13px",
    fontWeight: "600",
    cursor: "pointer",
  },

  stopButton: {
    padding: "10px 18px",
    border: "none",
    borderRadius: "9px",
    background: "#ef4444",
    color: "white",
    fontSize: "13px",
    fontWeight: "600",
    cursor: "pointer",
  },

  statusBadge: {
    padding: "5px 9px",
    borderRadius: "20px",
    fontSize: "10px",
    fontWeight: "700",
    whiteSpace: "nowrap",
  },


  /* ================= FEEDBACK ================= */

  feedback: {
    marginTop: "14px",
    background:
      "rgba(34,197,94,0.07)",
    border:
      "1px solid rgba(34,197,94,0.22)",
    borderRadius: "14px",
    padding: "14px 18px",
    textAlign: "center",
  },

  feedbackIcon: {
    fontSize: "18px",
  },


  /* ================= STATS ================= */

  dashboard: {
    display: "grid",
    gridTemplateColumns:
      "repeat(3, minmax(0, 1fr))",
    gap: "12px",
    marginTop: "14px",
  },

  statCard: {
    background:
      "rgba(15,35,60,0.78)",
    borderRadius: "13px",
    padding: "14px",
    border:
      "1px solid rgba(148,163,184,0.13)",
    textAlign: "center",
  },

  statIcon: {
    fontSize: "20px",
  },

  value: {
    fontSize: "22px",
    fontWeight: "700",
    color: "#60a5fa",
    margin: "7px 0 0",
  },


  /* ================= SESSION ================= */

  sessionCard: {
    marginTop: "14px",
    background:
      "rgba(15,35,60,0.78)",
    borderRadius: "15px",
    padding: "16px",
    border:
      "1px solid rgba(148,163,184,0.13)",
    textAlign: "center",
  },

  sessionGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(3, minmax(0, 1fr))",
    gap: "10px",
    marginTop: "10px",
  },

  sessionNumber: {
    fontSize: "21px",
    fontWeight: "700",
    color: "#60a5fa",
  },
};

export default App;