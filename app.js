const { useState, useEffect } = React;

// ─── UI COMPONENTS ───
const Card = ({ title, children }) => (
    <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl mb-4">
        {title && <h2 className="text-lg font-bold text-white mb-4">{title}</h2>}
        {children}
    </div>
);

// ─── MAIN SYSTEM ───
function POSApp() {
    const [act, setAct] = useState("dashboard");
    const [ings, setIngs] = useState([{id:1, name:"ใบชาไทย", stock:2000, cost:0.18, min:500, unit:"กรัม"}]);
    const [recs, setRecs] = useState([{id:1, name:"ชาไทยเย็น", price:45, lines:[{ingId:1, qty:15}]}]);
    const [ords, setOrds] = useState([]);

    // คำนวณต้นทุนจากสูตร
    const getRecCost = (lines) => lines.reduce((s,l) => s + ((ings.find(i=>i.id===l.ingId)?.cost||0) * l.qty), 0);

    return (
        <div className="flex h-screen bg-slate-950 text-slate-300">
            <aside className="w-56 bg-slate-900 border-r border-slate-800 p-4">
                <div className="text-white font-bold text-xl mb-8">Drink POS Pro</div>
                {["dashboard","pos","stock","recipe"].map(i => (
                    <button key={i} onClick={()=>setAct(i)} className={`w-full p-3 rounded-xl text-left ${act===i?'bg-amber-500 text-black font-bold':''}`}>{i.toUpperCase()}</button>
                ))}
            </aside>

            <main className="flex-1 p-8 overflow-auto">
                {/* DASHBOARD */}
                {act === "dashboard" && (
                    <div className="grid grid-cols-3 gap-6">
                        <Card title="ยอดขายรวม"><p className="text-3xl text-emerald-400 font-bold">฿{ords.reduce((s,o)=>s+o.price,0)}</p></Card>
                        <Card title="กำไรประเมิน"><p className="text-3xl text-amber-400 font-bold">฿{ords.reduce((s,o)=>s+(o.price - getRecCost(recs.find(r=>r.id===o.id)?.lines||[])),0)}</p></Card>
                        <Card title="ออเดอร์"><p className="text-3xl font-bold">{ords.length}</p></Card>
                    </div>
                )}

                {/* POS */}
                {act === "pos" && (
                    <div className="grid grid-cols-2 gap-6">
                        {recs.map(r => (
                            <button key={r.id} onClick={()=>{
                                setOrds([...ords, r]);
                                setIngs(ings.map(i => {
                                    const l = r.lines.find(x=>x.ingId===i.id);
                                    return l ? {...i, stock: i.stock - l.qty} : i;
                                }));
                            }} className="bg-slate-900 p-6 rounded-2xl hover:border-amber-500 border border-slate-800 text-left">
                                <h3 className="text-xl font-bold text-white">{r.name}</h3>
                                <p className="text-amber-500">฿{r.price}</p>
                            </button>
                        ))}
                    </div>
                )}

                {/* STOCK */}
                {act === "stock" && (
                    <Card title="คลังวัตถุดิบ">
                        <table className="w-full">
                            <thead><tr className="text-left border-b border-slate-800"><th className="pb-3">ชื่อ</th><th className="pb-3">คงเหลือ</th><th className="pb-3">สถานะ</th></tr></thead>
                            <tbody>{ings.map(i => (
                                <tr key={i.id} className="border-b border-slate-800/50">
                                    <td className="py-4">{i.name}</td>
                                    <td className="py-4">{i.stock} {i.unit}</td>
                                    <td className={`py-4 ${i.stock < i.min ? 'text-rose-400' : 'text-emerald-400'}`}>{i.stock < i.min ? "ต้องเติมของ" : "ปกติ"}</td>
                                </tr>
                            ))}</tbody>
                        </table>
                    </Card>
                )}
                
                {/* RECIPE */}
                {act === "recipe" && (
                    <div className="space-y-4">
                        {recs.map(r => (
                            <Card key={r.id} title={r.name}>
                                <p>ต้นทุนวัตถุดิบ: ฿{getRecCost(r.lines).toFixed(2)}</p>
                                <p>กำไรต่อแก้ว: ฿{(r.price - getRecCost(r.lines)).toFixed(2)}</p>
                            </Card>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<POSApp />);
