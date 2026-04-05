import { useState } from 'react';
import { useApp } from '../../context/AppContext';

export default function Reports() {
  const { settings } = useApp();
  const [loading, setLoading] = useState(null);
  const reports = [
    { id: 1, title: 'IT Sector Outlook Q2', size: '1.8 MB' },
    { id: 2, title: 'Banking Credit Cycle', size: '2.1 MB' },
    { id: 3, title: 'IPO Pipeline India', size: '1.3 MB' },
    { id: 4, title: 'FMCG Rural Demand', size: '1.6 MB' }
  ];
  const dl = (id) => { setLoading(id); setTimeout(() => setLoading(null), 3000); };
  return <section className="section light"><h2>Reports</h2><div className="grid">{reports.map((r)=><article key={r.id} className="report"><h3>{r.title}</h3><p>{r.size}</p><button disabled={!settings.downloads || loading===r.id} onClick={()=>dl(r.id)}>{loading===r.id ? '✓ Done' : 'Download'}</button></article>)}</div></section>;
}
