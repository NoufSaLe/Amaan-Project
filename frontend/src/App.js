import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';

// --- المكونات (Pages) ---

// 1. صفحة الهوم والمسح
const HomePage = ({ setScanResult, setLoading }) => {
  const navigate = useNavigate();

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      // إرسال الصورة للباك إند
      const response = await axios.post('http://127.0.0.1:5000/api/scan-qr', formData);
      setScanResult(response.data);
      navigate('/result'); // الانتقال لصفحة النتيجة بعد انتهاء الفحص
    } catch (err) {
      alert("عذراً، حدث خطأ أثناء قراءة الصورة أو الاتصال بالسيرفر.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page home-page">
      <div className="scan-card">
        <div className="icon-placeholder">📷</div>
        <h2>مسح رمز الاستجابة</h2>
        <p>قم برفع صورة الـ QR Code لفحصها أمنياً</p>
        <label className="upload-btn">
          إبدأ الفحص الآن
          <input type="file" accept="image/*" onChange={handleImageUpload} hidden />
        </label>
        <p className="privacy-note">🛡️ خصوصيتك أولويتنا: لا يتم حفظ صورك في سيرفراتنا.</p>
      </div>
    </div>
  );
};

// 2. صفحة النتيجة
const ResultPage = ({ scanResult }) => {
  const navigate = useNavigate();

  // حماية في حال دخل المستخدم الصفحة مباشرة بدون سكان
  if (!scanResult) {
    return (
      <div className="page">
        <div className="result-card">
          <p>لا توجد نتائج لعرضها.</p>
          <button onClick={() => navigate('/')}>العودة للرئيسية</button>
        </div>
      </div>
    );
  }

  const isMalicious = scanResult.vt_result?.malicious;

  return (
    <div className={`page result-page ${isMalicious ? 'danger-theme' : 'safe-theme'}`}>
      <div className="result-card">
        <div className="result-icon">{isMalicious ? '⚠️' : '✅'}</div>
        <h2>{isMalicious ? 'تحذير: رابط غير آمن!' : 'رابط آمن تماماً'}</h2>
        
        <div className="details-container">
          <p className="url-text"><strong>الرابط:</strong> {scanResult.data}</p>
          {isMalicious && (
            <p className="threat-count">
              تم اكتشاف تهديد بواسطة <strong>{scanResult.vt_result.malicious_count}</strong> محرك فحص أمني.
            </p>
          )}
        </div>

        <div className="actions-btns">
          <button className="back-btn" onClick={() => navigate('/')}>فحص رابط آخر</button>
          {isMalicious && (
            <button className="report-btn" onClick={() => navigate('/report')}>الإبلاغ عن الرابط</button>
          )}
        </div>
      </div>
    </div>
  );
};

// 3. صفحة الابلاغ
const ReportPage = () => {
  const navigate = useNavigate();
  const [isSent, setIsSent] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSent(true);
    // هنا مستقبلاً نربط مع قاعدة بيانات لإرسال البلاغ
  };

  return (
    <div className="page report-page">
      <div className="report-card">
        <h2>نموذج الإبلاغ</h2>
        {!isSent ? (
          <>
            <p>ساعدنا في تحسين مجتمع "أمان" من خلال الإبلاغ عن الروابط الاحتيالية.</p>
            <form onSubmit={handleSubmit}>
              <textarea placeholder="أدخل تفاصيل إضافية عن الرابط المشبوه..." required></textarea>
              <button type="submit" className="submit-report">إرسال البلاغ</button>
              <button type="button" className="cancel-btn" onClick={() => navigate(-1)}>إلغاء</button>
            </form>
          </>
        ) : (
          <div className="success-report">
            <div className="success-icon">✔️</div>
            <h3>تم استلام بلاغك!</h3>
            <p>شكراً لمساهمتك في جعل الإنترنت مكاناً أكثر أماناً.</p>
            <button onClick={() => navigate('/')}>العودة للصفحة الرئيسية</button>
          </div>
        )}
      </div>
    </div>
  );
};

// --- المكون الرئيسي للهيكلة ---
function App() {
  const [scanResult, setScanResult] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <Router>
      <div className="App">
        {/* شاشة التحميل (Loader Overlay) */}
        {loading && (
          <div className="loader-overlay">
            <div className="spinner"></div>
            <p>جاري التحليل الأمني الشامل...</p>
          </div>
        )}

        <Routes>
          <Route path="/" element={<HomePage setScanResult={setScanResult} setLoading={setLoading} />} />
          <Route path="/result" element={<ResultPage scanResult={scanResult} />} />
          <Route path="/report" element={<ReportPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;