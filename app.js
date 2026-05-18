const { useState, useMemo, useEffect } = React;

const Icon = { dashboard: "📊", pos: "🖥️", stock: "📦", recipe: "📝", plus: "➕", minus: "➖", trash: "🗑️", x: "❌", check: "✅", back: "◀️", inbox: "📥" };

const UNIT_FAMILIES = {
  "กรัม": [{ name: "กรัม", mult: 1 }, { name: "กิโลกรัม", mult: 1000 }],
  "มล.": [{ name: "มล.", mult: 1 }, { name: "ลิตร", mult: 1000 }],
  "ชิ้น": [{ name: "ชิ้น", mult: 1 }, { name: "แพ็ค(50)", mult: 50 }]
};

const fmtCost = (n) => `฿${Number(n).toLocaleString('th-TH', {minimumFractionDigits: 2, maximumFractionDigits: 4})}`;

function POSApp() {
  const [active, setActive] = useState("dashboard");
  const [ings, setIngs] = useState([
    { id:1, name:"ใบชาไทย", type:"วัตถุดิบ", unit:"กรัม", stock:2000, costPerUnit:0.18, minStock:500 }
  ]);
  const [recs, setRecs] = useState([]);
  const [ords, setOrds] = useState([]);

  return (
    <div className="flex h-screen bg-slate-950">
      <aside className="w-16 md:w-56 bg-slate-900 border-r border-slate-800 flex flex-col">
        <div className="p-4 font-bold text-white">POS</div>
        <nav className="flex-1 p-2 space-y-2">
          {["dashboard","pos","stock","recipe"].map(id => (
            <button key={id} onClick={()=>setActive(id)} className={`w-full p-3 rounded-lg ${active===id?'bg-amber-500 text-black':'text-slate-400'}`}>
              {id.toUpperCase()}
            </button>
          ))}
        </nav>
      </aside>
      <main className="flex-1 p-5 overflow-auto text-white">
        <h1>หน้า {active}</h1>
        <p>หากเห็นหน้านี้ แสดงว่าระบบทำงานปกติครับบอส!</p>
      </main>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<POSApp />);
