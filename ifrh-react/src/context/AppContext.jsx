import { createContext, useContext, useMemo, useState } from 'react';
import { showToast } from '../utils/toast';
import { api } from '../utils/api';

const AppCtx = createContext(null);

const defaultBrand = {
  fullName: 'Indian Financial Research Hub',
  shortName: 'IFRH',
  primary: '#E8871A',
  bg: '#0B1A2E',
  accent: '#C9952A'
};

export function AppProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [authMode, setAuthMode] = useState('closed');
  const [forgotOpen, setForgotOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [watchlistOpen, setWatchlistOpen] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [adminOpen, setAdminOpen] = useState(false);
  const [adminErr, setAdminErr] = useState('');
  const [brand, setBrand] = useState(defaultBrand);
  const [logoUrl, setLogoUrl] = useState('₹');
  const [settings, setSettings] = useState({ ticker: true, downloads: true, regs: true, maint: false });
  const [socials, setSocials] = useState([{ name: 'X', url: '#' }, { name: 'LinkedIn', url: '#' }]);
  const [requests, setRequests] = useState([]);
  const [pageMod, setPageMod] = useState(null);
  const [sectorMod, setSectorMod] = useState(null);

  const loginUser = (user) => setCurrentUser(user);
  const logoutUser = () => setCurrentUser(null);
  const openSignIn = () => setAuthMode('signin');
  const openSignUp = () => setAuthMode('signup');
  const closeAuth = () => setAuthMode('closed');

  const doSignIn = async (payload) => {
    const data = await api.auth('signin', payload);
    if (data.ok) {
      setCurrentUser(data.user);
      closeAuth();
      showToast('Signed in successfully', 'success');
    } else showToast(data.error || 'Sign-in failed', 'error');
  };

  const doSignUp = async (payload) => {
    const data = await api.auth('signup', payload);
    data.ok ? showToast('Account created', 'success') : showToast(data.error || 'Sign-up failed', 'error');
  };

  const doGoogleAuth = () => showToast('Google OAuth hook ready', 'success');

  const openAdminLogin = () => setAdminOpen(true);
  const closeAdminLogin = () => setAdminOpen(false);

  const attemptAdminLogin = async (username, password) => {
    const data = await api.admin('login', { username, password });
    if (data.ok) {
      setIsAdmin(true);
      setAdminErr('');
      setAdminOpen(false);
      showToast('Admin mode enabled', 'success');
    } else {
      setAdminErr('Invalid credentials');
    }
  };

  const adminLogout = () => setIsAdmin(false);
  const changeAdminPass = async (payload) => api.admin('change_pass', payload);

  const debounceSave = () => {
    clearTimeout(window.__ifrhSync);
    window.__ifrhSync = setTimeout(() => api.sync('save', { brand, settings, socials, requests }), 1500);
  };

  const value = useMemo(() => ({
    currentUser, openSignIn, openSignUp, closeAuth, loginUser, logoutUser, doSignIn, doSignUp, doGoogleAuth,
    authMode, forgotOpen, setForgotOpen, profileOpen, setProfileOpen, watchlistOpen, setWatchlistOpen,
    isAdmin, adminOpen, adminErr, openAdminLogin, closeAdminLogin, attemptAdminLogin, adminLogout, changeAdminPass,
    brand, setBrand, logoUrl, setLogoUrl, settings, setSettings, socials, setSocials, requests, setRequests,
    syncStatus: 'idle', debounceSave, pageMod, openPage: setPageMod, closePage: () => setPageMod(null),
    sectorMod, openSector: setSectorMod, closeSector: () => setSectorMod(null)
  }), [currentUser, authMode, forgotOpen, profileOpen, watchlistOpen, isAdmin, adminOpen, adminErr, brand, logoUrl, settings, socials, requests, pageMod, sectorMod]);

  return <AppCtx.Provider value={value}>{children}</AppCtx.Provider>;
}

export const useApp = () => useContext(AppCtx);
