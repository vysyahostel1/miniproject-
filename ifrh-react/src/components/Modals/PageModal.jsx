import { useApp } from '../../context/AppContext';
import useModal from '../../hooks/useModal';

export default function PageModal() {
  const { pageMod, closePage, sectorMod, closeSector } = useApp();
  const open = Boolean(pageMod || sectorMod);
  useModal(open, pageMod ? closePage : closeSector);
  if (!open) return null;
  const title = pageMod || sectorMod;
  return <div className="modal" onClick={pageMod ? closePage : closeSector}><div className="modal-card" onClick={(e)=>e.stopPropagation()}><h3>{title}</h3><p>Detailed content managed by admin settings.</p></div></div>;
}
