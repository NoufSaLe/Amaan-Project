import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';

/* =========================
   Home Page
========================= */
const HomePage = ({ setScanResult, setLoading }) => {
  const navigate = useNavigate();

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);

    try {
      const response = await axios.post(
        'http://127.0.0.1:5000/api/scan-qr',
        formData
      );

      // ❌ لا يوجد QR
      if (!response.data.success) {
        setScanResult({ noQR: true });
        navigate('/result');
        return;
      }

      // ✅ يوجد QR
      setScanResult(response.data);
      navigate('/result');

    } catch (err) {
      setScanResult({ serverError: true });
      navigate('/result');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page home-page">
      <div className="scan-card">
        <div className="icon-placeholder">📷</div>
        <h2>مسح رمز الاستجابة</h2>
        <p>قم برفع صورة QR Code لفحصها أمنياً</p>

        <label className="upload-btn">
          إبدأ الفحص الآن
          <input type="file" accept="image/*" onChange={handleImageUpload} hidden />
        </label>

        <p className="privacy-note">
          🛡️ خصوصيتك أولويتنا: لا يتم حفظ صورك في سيرفراتنا.
        </p>
      </div>
    </div>
  );
};

/* =========================
   Result Page
========================= */
const ResultPage = ({ scanResult }) => {
  const navigate = useNavigate();

  if (!scanResult) {
    return (
      <div className="page">
        <div className="result-card">
          <p>لا توجد نتائج لعرضها.</p>
          <button onClick={() => navigate('/')}>العودة</button>
        </div>
      </div>
    );
  }

  // ❌ لا يوجد QR
  if (scanResult.noQR) {
    return (
      <div className="page result-page safe-theme">
        <div className="result-card">
          <div className="result-icon">🔍</div>
          <h2>لم يتم العثور على رمز QR</h2>
          <p>تم تحليل الصورة ولكن لم يتم اكتشاف أي رمز QR.</p>

          <button className="back-btn" onClick={() => navigate('/')}>
            تجربة صورة أخرى
          </button>
        </div>
      </div>
    );
  }

  // ❌ خطأ سيرفر
  if (scanResult.serverError) {
    return (
      <div className="page result-page danger-theme">
        <div className="result-card">
          <div className="result-icon">⚠️</div>
          <h2>حدث خطأ أثناء الاتصال بالسيرفر</h2>

          <button className="back-btn" onClick={() => navigate('/')}>
            المحاولة مرة أخرى
          </button>
        </div>
      </div>
    );
  }

  /* =========================
     ⭐ التعديل الجديد هنا
     التحقق هل المحتوى رابط أم نص
  ========================= */

  const qrText = scanResult.data || "";

  const isURL =
    qrText.startsWith("http://") ||
    qrText.startsWith("https://") ||
    qrText.startsWith("www.");

  // 📝 QR يحتوي نص فقط
  if (!isURL) {
    return (
      <div className="page result-page safe-theme">
        <div className="result-card">
          <div className="result-icon">📝</div>

          <h2>تم اكتشاف نص داخل QR</h2>

          <div className="details-container">
            <p className="url-text">
              هذا الرمز لا يحتوي على رابط وإنما نص:
            </p>

            <p className="url-text" style={{ marginTop: "10px" }}>
              <strong>{qrText}</strong>
            </p>
          </div>

          <button className="back-btn" onClick={() => navigate('/')}>
            فحص رمز آخر
          </button>
        </div>
      </div>
    );
  }

  /* =========================
     رابط طبيعي (الفحص الأمني)
  ========================= */

  const isMalicious = scanResult.vt_result?.malicious;

  return (
    <div className={`page result-page ${isMalicious ? 'danger-theme' : 'safe-theme'}`}>
      <div className="result-card">
        <div className="result-icon">
          {isMalicious ? '⚠️' : '✅'}
        </div>

        <h2>
          {isMalicious ? 'تحذير: رابط غير آمن!' : 'رابط آمن تماماً'}
        </h2>

        <div className="details-container">
          <p className="url-text">
            <strong>الرابط:</strong> {qrText}
          </p>
        </div>

        <button className="back-btn" onClick={() => navigate('/')}>
          فحص رابط آخر
        </button>
      </div>
    </div>
  );
};

/* =========================
   App Root
========================= */
function App() {
  const [scanResult, setScanResult] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <Router>
      <div className="App">

        {loading && (
          <div className="loader-overlay">
            <div className="spinner"></div>
            <p>جاري التحليل الأمني الشامل...</p>
          </div>
        )}

        <Routes>
          <Route path="/" element={<HomePage setScanResult={setScanResult} setLoading={setLoading} />} />
          <Route path="/result" element={<ResultPage scanResult={scanResult} />} />
        </Routes>

      </div>
    </Router>
  );
}

export default App;
