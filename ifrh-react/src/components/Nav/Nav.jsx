import { useApp } from '../../context/AppContext';

export default function Nav() {
  const { brand, currentUser, openSignIn, openSignUp, openAdminLogin, isAdmin, adminLogout, setProfileOpen, setWatchlistOpen } = useApp();
  return (
    <header className="nav-wrap">
      <div className="brand"><span className="logo">₹</span><strong>{brand.shortName}</strong></div>
      <nav>
        {['Home', 'Stocks', 'Economy', 'IPOs', 'Sectors', 'Reports'].map((x) => <a key={x} href="#">{x}</a>)}
      </nav>
      <div className="actions">
        <button onClick={openAdminLogin}>{isAdmin ? 'Admin ✓' : 'Admin'}</button>
        {!currentUser ? (
          <>
            <button onClick={openSignIn}>Sign In</button>
            <button onClick={openSignUp}>Sign Up</button>
          </>
        ) : (
          <>
            <button onClick={() => setProfileOpen(true)}>My Profile</button>
            <button onClick={() => setWatchlistOpen(true)}>Watchlist</button>
            <button onClick={adminLogout}>Sign Out</button>
          </>
        )}
      </div>
    </header>
  );
}
