import { AppProvider, useApp } from './context/AppContext';
import Nav from './components/Nav/Nav';
import Ticker from './components/Ticker/Ticker';
import Hero from './components/Hero/Hero';
import Categories from './components/Categories/Categories';
import Reports from './components/Reports/Reports';
import Sectors from './components/Sectors/Sectors';
import ResearchRequest from './components/ResearchRequest/ResearchRequest';
import Footer from './components/Footer/Footer';
import Toast from './components/Nav/Toast';
import AuthModal from './components/Modals/AuthModal';
import ForgotModal from './components/Modals/ForgotModal';
import ProfileModal from './components/Modals/ProfileModal';
import WatchlistModal from './components/Modals/WatchlistModal';
import PageModal from './components/Modals/PageModal';
import AdminLogin from './components/Admin/AdminLogin';
import AdminPanel from './components/Admin/AdminPanel';

function PublicApp() {
  const { settings, isAdmin } = useApp();
  return (
    <>
      <div className="disclaimer">NOT SEBI Registered Research Analyst • Educational Purposes Only • NOT Financial Advice • NOT for Investment Decisions • Consult a SEBI Registered Advisor</div>
      {settings.ticker && <Ticker />}
      <Nav />
      {isAdmin ? (
        <AdminPanel />
      ) : (
        <main>
          <Hero />
          <Categories />
          <Reports />
          <Sectors />
          <ResearchRequest />
        </main>
      )}
      <Footer />
      <Toast />
      <AuthModal />
      <ForgotModal />
      <ProfileModal />
      <WatchlistModal />
      <PageModal />
      <AdminLogin />
    </>
  );
}

export default function App() {
  return (
    <AppProvider>
      <PublicApp />
    </AppProvider>
  );
}
