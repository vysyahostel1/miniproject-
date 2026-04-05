import { useApp } from '../../context/AppContext';
import useModal from '../../hooks/useModal';

export default function WatchlistModal() {
  const { watchlistOpen, setWatchlistOpen } = useApp();
  useModal(watchlistOpen, () => setWatchlistOpen(false));
  if (!watchlistOpen) return null;
  return <div className="modal" onClick={() => setWatchlistOpen(false)}><div className="modal-card" onClick={(e)=>e.stopPropagation()}><h3>Watchlist</h3><p>Track sectors you follow.</p></div></div>;
}
