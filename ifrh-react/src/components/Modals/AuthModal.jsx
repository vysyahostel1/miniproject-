import { useState } from 'react';
import useModal from '../../hooks/useModal';
import { useApp } from '../../context/AppContext';

export default function AuthModal() {
  const { authMode, closeAuth, doSignIn, doSignUp } = useApp();
  const [form, setForm] = useState({ email: '', password: '', first_name: '', last_name: '' });
  const open = authMode !== 'closed';
  useModal(open, closeAuth);
  if (!open) return null;
  return <div className="modal" onClick={closeAuth}><div className="modal-card" onClick={(e)=>e.stopPropagation()}><h3>{authMode === 'signin' ? 'Sign In' : 'Sign Up'}</h3><input placeholder="Email" value={form.email} onChange={(e)=>setForm({...form,email:e.target.value})}/><input type="password" placeholder="Password" value={form.password} onChange={(e)=>setForm({...form,password:e.target.value})}/>{authMode==='signup'&&<><input placeholder="First Name" value={form.first_name} onChange={(e)=>setForm({...form,first_name:e.target.value})}/><input placeholder="Last Name" value={form.last_name} onChange={(e)=>setForm({...form,last_name:e.target.value})}/></>}<button onClick={()=>authMode === 'signin' ? doSignIn(form) : doSignUp(form)}>{authMode === 'signin' ? 'Sign In' : 'Sign Up'}</button></div></div>;
}
