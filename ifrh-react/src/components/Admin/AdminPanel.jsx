import { useApp } from '../../context/AppContext';

export default function AdminPanel() {
  const { settings, setSettings } = useApp();
  return <section className="section"><h2>Admin Panel</h2><label><input type="checkbox" checked={settings.ticker} onChange={(e)=>setSettings({...settings,ticker:e.target.checked})}/> Ticker Bar</label><label><input type="checkbox" checked={settings.downloads} onChange={(e)=>setSettings({...settings,downloads:e.target.checked})}/> Download Reports</label><label><input type="checkbox" checked={settings.regs} onChange={(e)=>setSettings({...settings,regs:e.target.checked})}/> New Registrations</label><label><input type="checkbox" checked={settings.maint} onChange={(e)=>setSettings({...settings,maint:e.target.checked})}/> Maintenance</label></section>;
}
