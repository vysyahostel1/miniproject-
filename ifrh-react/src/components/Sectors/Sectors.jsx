import { useApp } from '../../context/AppContext';
const sectors = ['IT','Banking','Pharma','Auto','FMCG','Energy','Real Estate','Infrastructure','Metals','Consumer Durables','Chemicals','Telecom'];
export default function Sectors() {
  const { openSector } = useApp();
  return <section className="section navy"><h2>Sectors</h2><div className="pill-grid">{sectors.map((s)=><button key={s} className="pill-btn" onClick={()=>openSector(s)}>{s}</button>)}</div></section>;
}
