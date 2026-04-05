const items = ['NIFTY 50 22,541.30 ▲', 'SENSEX 74,118.70 ▲', 'TCS ₹4,010', 'RELIANCE ₹2,990', 'HDFC BANK ₹1,722', 'INFOSYS ₹1,456'];
export default function Ticker() {
  return <div className="ticker"><div className="marquee">{items.concat(items).join('   •   ')}</div></div>;
}
