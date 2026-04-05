import { useApp } from '../../context/AppContext';
import useModal from '../../hooks/useModal';

export default function ForgotModal() {
  const { forgotOpen, setForgotOpen } = useApp();
  useModal(forgotOpen, () => setForgotOpen(false));
  if (!forgotOpen) return null;
  return <div className="modal" onClick={() => setForgotOpen(false)}><div className="modal-card" onClick={(e)=>e.stopPropagation()}><h3>Forgot Password</h3><p>OTP flow placeholder.</p></div></div>;
}
