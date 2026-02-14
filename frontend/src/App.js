import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // متغير لتخزين الرسالة القادمة من الباك إند
  const [message, setMessage] = useState("جاري الاتصال بالباك إند...");

  useEffect(() => {
    // نطلب البيانات من رابط Flask (تأكدي أن السيرفر شغال على بورت 5000)
    axios.get('http://127.0.0.1:5000/')
      .then(response => {
        setMessage(response.data); // لو نجح الاتصال، نخزن الرسالة
      })
      .catch(error => {
        console.error("خطأ في الاتصال:", error);
        setMessage("فشل الاتصال بالباك إند ❌ تأكدي من تشغيل app.py");
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>مشروع أمان - Amaan Project</h1>
        <div style={{ padding: '20px', border: '2px solid white', borderRadius: '10px' }}>
          <p>حالة الاتصال:</p>
          <h2>{message}</h2> 
        </div>
      </header>
    </div>
  );
}

export default App;