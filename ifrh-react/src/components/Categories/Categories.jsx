export default function Categories() {
  const cards = ['Indian Stocks', 'Economy', 'IPOs', 'Sectors'];
  return <section className="section"><h2>Categories</h2><div className="grid">{cards.map((c)=><article key={c} className="card"><h3>{c}</h3><p>Structured analysis designed for learners.</p></article>)}</div></section>;
}
