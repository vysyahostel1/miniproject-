import { useEffect, useState } from 'react';

export default function Toast() {
  const [toast, setToast] = useState(null);
  useEffect(() => {
    const h = (e) => {
      setToast(e.detail);
      setTimeout(() => setToast(null), 2200);
    };
    window.addEventListener('ifrh-toast', h);
    return () => window.removeEventListener('ifrh-toast', h);
  }, []);
  return toast ? <div className={`toast ${toast.type}`}>{toast.text}</div> : null;
}
