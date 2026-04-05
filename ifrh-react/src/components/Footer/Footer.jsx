import { useApp } from '../../context/AppContext';

export default function Footer() {
  const { brand, socials, openPage } = useApp();
  return <footer><h3>{brand.fullName}</h3><p>Educational finance research for India.</p><div>{socials.map((s)=><a key={s.name} href={s.url}>{s.name}</a>)}</div><div className="footer-links">{['About','Contact','Privacy','Terms','Blog','Guides','FAQ','Support'].map((p)=><button key={p} onClick={()=>openPage(p)}>{p}</button>)}</div></footer>;
}
