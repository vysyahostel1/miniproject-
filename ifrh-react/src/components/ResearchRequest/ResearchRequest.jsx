import { useState } from 'react';
import { api } from '../../utils/api';
import { showToast } from '../../utils/toast';

export default function ResearchRequest() {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({ type: 'Stock', priority: 'Normal', subject: '', message: '', name: '', email: '', phone: '', agree: false });
  const submit = async () => {
    const data = await api.requests('submit', form);
    data.ok ? showToast(`Request submitted: ${data.req_id}`) : showToast('Submission failed', 'error');
  };
  return <section className="section"><h2>Research Request</h2><p>Step {step} of 3</p>
    {step === 1 && <div><input value={form.type} onChange={(e)=>setForm({...form,type:e.target.value})}/><button onClick={()=>setStep(2)}>Next</button></div>}
    {step === 2 && <div><input placeholder="Subject" value={form.subject} onChange={(e)=>setForm({...form,subject:e.target.value})}/><textarea value={form.message} onChange={(e)=>setForm({...form,message:e.target.value})}/><button onClick={()=>setStep(3)}>Next</button></div>}
    {step === 3 && <div><input placeholder="Name" value={form.name} onChange={(e)=>setForm({...form,name:e.target.value})}/><input placeholder="Email" value={form.email} onChange={(e)=>setForm({...form,email:e.target.value})}/><label><input type="checkbox" checked={form.agree} onChange={(e)=>setForm({...form,agree:e.target.checked})}/> Educational use only</label><button onClick={submit}>Submit</button></div>}
  </section>;
}
