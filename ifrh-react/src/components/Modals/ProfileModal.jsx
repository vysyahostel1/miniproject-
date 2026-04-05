import { useApp } from '../../context/AppContext';
import useModal from '../../hooks/useModal';

export default function ProfileModal() {
  const { profileOpen, setProfileOpen, currentUser } = useApp();
  useModal(profileOpen, () => setProfileOpen(false));
  if (!profileOpen) return null;
  return <div className="modal" onClick={() => setProfileOpen(false)}><div className="modal-card" onClick={(e)=>e.stopPropagation()}><h3>My Profile</h3><p>{currentUser?.email || 'Guest'}</p></div></div>;
}
