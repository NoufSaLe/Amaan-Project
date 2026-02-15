import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [error, setError] = useState(null);

  // دالة التعامل مع رفع الصورة (من الكاميرا أو الاستوديو)
  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // تجهيز البيانات لإرسالها للباك إند
    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError(null);
    setScanResult(null);

    try {
      // إرسال الصورة للمسار الذي برمجناه في Flask
      const response = await axios.post('http://127.0.0.1:5000/api/scan-qr', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setScanResult(response.data); // تخزين نتيجة الفحص (آمن/خطر)
    } catch (err) {
      setError(err.response?.data?.error || "حدث خطأ أثناء الفحص");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="main-container">
        <h1>مشروع أمان - AMAAN</h1>
        
        {/* بطاقة المسح الرئيسية المستوحاة من Figma */}
        <div className="scan-card">
          <div className="icon-placeholder">📷</div>
          <h2>مسح رمز الاستجابة</h2>
          <p>Scan QR Code</p>

          <label className="upload-btn">
            {loading ? "جاري التحليل..." : "اضغط للبدء"}
            <input 
              type="file" 
              accept="image/*" 
              capture="environment" // يفتح الكاميرا مباشرة في الجوال
              onChange={handleImageUpload} 
              hidden 
            />
          </label>
        </div>

        {/* عرض النتائج - شاشة التحذير أو الأمان */}
        {scanResult && (
          <div className={`result-overlay ${scanResult.vt_result?.malicious ? 'warning' : 'safe'}`}>
             <div className="result-content">
                {scanResult.vt_result?.malicious ? (
                  <>
                    <div className="alert-icon">⚠️</div>
                    <h2>تحذير - WARNING</h2>
                    <p>خطر أمني - لا تتابع!</p>
                  </>
                ) : (
                  <>
                    <div className="success-icon">✅</div>
                    <h2>آمن - SAFE</h2>
                    <p>تم التحقق بنجاح</p>
                  </>
                )}
                <button onClick={() => setScanResult(null)}>إغلاق</button>
             </div>
          </div>
        )}

        {error && <p className="error-msg">{error}</p>}
      </div>
    </div>
  );
}

export default App;