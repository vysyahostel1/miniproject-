import { useState } from 'react';
import { useApp } from '../../context/AppContext';
import useModal from '../../hooks/useModal';

export default function AdminLogin() {
  const { adminOpen, closeAdminLogin, attemptAdminLogin, adminErr } = useApp();
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('');
  useModal(adminOpen, closeAdminLogin);
  if (!adminOpen) return null;
  return <div className="modal" onClick={closeAdminLogin}><div className="modal-card" onClick={(e)=>e.stopPropagation()}><h3>Admin Login</h3><input value={username} onChange={(e)=>setUsername(e.target.value)}/><input type="password" value={password} onChange={(e)=>setPassword(e.target.value)}/><button onClick={()=>attemptAdminLogin(username,password)}>Enter</button>{adminErr && <p className="err">{adminErr}</p>}</div></div>;
}
