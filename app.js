const { useState, useEffect } = React;

const Icon = { dashboard: "📊", pos: "🖥️", stock: "📦", recipe: "📝", plus: "➕", minus: "➖", trash: "🗑️", x: "❌", check: "✅" };

function POSApp() {
  const [act, setAct] = useState("dashboard");
  const [ings, setIngs] = useState([{ id:1, name:"ใบชาไทย", unit:"กรัม", stock:2000, cost:0.18 }]);
  const [recs, setRecs] = useState([{ id:1, name:"ชาไทยเย็น", price: 45, lines:[{ingId:1,qty:15}] }]);
  const [ords, setOrds] = useState([]);

  // ฟังก์ชันคำนวณคอส
  const getRecipeCost = (lines) => lines.reduce((s,l) => s + (ings.find(i=>i.id===l.ingId)?.cost * l.qty || 0), 0);

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200">
      <aside className="w-56 bg-slate-900 p-4 border-r border-slate-800">
        <h1 className="font-bold text-white mb-6">POS System</h1>
        {["dashboard","pos","stock","recipe"].map(i => (
          <button key={i} onClick={()=>setAct(i)} className={`w-full p-3 mb-2 rounded-xl text-left ${act===i?'bg-amber-500 text-black font-bold':'hover:bg-slate-800'}`}>
            {i.toUpperCase()}
          </button>
        ))}
      </aside>
      
      <main className="flex-1 p-6 overflow-auto">
        {act === "dashboard" && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold">Dashboard</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800">
                <p className="text-slate-400">ยอดขายรวม</p>
                <p className="text-3xl font-bold text-emerald-400">฿{ords.reduce((s,o)=>s+o.price,0)}</p>
              </div>
              <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800">
                <p className="text-slate-400">ออเดอร์ทั้งหมด</p>
                <p className="text-3xl font-bold">{ords.length} บิล</p>
              </div>
            </div>
          </div>
        )}

        {act === "pos" && (
          <div className="grid grid-cols-3 gap-6">
            <div className="col-span-2 space-y-4">
              {recs.map(r => (
                <button key={r.id} onClick={() => setOrds([...ords, r])} className="w-full bg-slate-900 p-4 rounded-xl border border-slate-800 hover:border-amber-500 text-left">
                  {r.name} <span className="float-right font-bold text-amber-500">฿{r.price}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {act === "stock" && (
          <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6">
            <h2 className="text-xl font-bold mb-4">คลังวัตถุดิบ</h2>
            <table className="w-full">
              <thead><tr className="text-left text-slate-400 border-b border-slate-800"><th className="pb-3">รายการ</th><th className="pb-3">คงเหลือ</th><th className="pb-3">ต้นทุน/หน่วย</th></tr></thead>
              <tbody>{ings.map(i => <tr key={i.id} className="border-b border-slate-800"><td className="py-3">{i.name}</td><td className="py-3">{i.stock} {i.unit}</td><td className="py-3">฿{i.cost}</td></tr>)}</tbody>
            </table>
          </div>
        )}

        {act === "recipe" && (
          <div className="space-y-4">
            {recs.map(r => (
              <div key={r.id} className="bg-slate-900 p-6 rounded-2xl border border-slate-800">
                <h3 className="text-lg font-bold">{r.name}</h3>
                <p className="text-amber-400">ต้นทุนต่อแก้ว: ฿{getRecipeCost(r.lines).toFixed(2)}</p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<POSApp />);
