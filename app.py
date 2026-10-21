import React, { useState, useMemo, useEffect } from 'react';
import { 
  LayoutDashboard, 
  MonitorSmartphone, 
  Package, 
  Users, 
  UserCog, 
  LogOut, 
  Search, 
  ShoppingCart, 
  Plus, 
  Trash2, 
  Coffee, 
  Car, 
  Receipt,
  X,
  CheckCircle2,
  Menu
} from 'lucide-react';

// --- MOCK DATA ---
const initialProducts = [
  { id: 1, name: 'Cuci Salju Mobil Kecil', price: 40000, category: 'Car Wash', icon: 'Car' },
  { id: 2, name: 'Cuci Salju Mobil Besar', price: 50000, category: 'Car Wash', icon: 'Car' },
  { id: 3, name: 'Cuci Mesin + Jamur Kaca', price: 150000, category: 'Car Wash', icon: 'Car' },
  { id: 4, name: 'Espresso', price: 18000, category: 'F&B', icon: 'Coffee' },
  { id: 5, name: 'Ice Caffe Latte', price: 25000, category: 'F&B', icon: 'Coffee' },
  { id: 6, name: 'Caramel Macchiato', price: 30000, category: 'F&B', icon: 'Coffee' },
  { id: 7, name: 'French Fries', price: 15000, category: 'F&B', icon: 'Package' },
];

const initialEmployees = [
  { id: 1, name: 'Budi Santoso', role: 'Washer', phone: '08123456789' },
  { id: 2, name: 'Siti Aminah', role: 'Barista', phone: '08129876543' },
];

const initialUsers = [
  { id: 1, username: 'admin', name: 'Super Admin', role: 'Admin' },
  { id: 2, username: 'kasir1', name: 'Andi Kasir', role: 'Cashier' },
];

const initialTransactions = [
  { id: 'TRX-1001', date: new Date().toISOString(), total: 65000, items: [{ name: 'Cuci Salju Mobil Besar', qty: 1, price: 50000 }, { name: 'French Fries', qty: 1, price: 15000 }] }
];

// --- UTILS ---
const formatRupiah = (number) => {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(number);
};

// --- COMPONENTS ---

const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex justify-center items-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
          <h3 className="font-semibold text-lg text-slate-800">{title}</h3>
          <button onClick={onClose} className="p-1 hover:bg-slate-100 rounded-full text-slate-500 transition-colors">
            <X size={20} />
          </button>
        </div>
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  );
};

export default function App() {
  const [activeTab, setActiveTab] = useState('pos');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // State Management
  const [products, setProducts] = useState(initialProducts);
  const [employees, setEmployees] = useState(initialEmployees);
  const [users, setUsers] = useState(initialUsers);
  const [transactions, setTransactions] = useState(initialTransactions);

  // Layout Wrapper
  const Layout = ({ children }) => (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-800 overflow-hidden">
      {/* Sidebar Overlay for Mobile */}
      {!isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/50 z-20 lg:hidden"
          onClick={() => setIsSidebarOpen(true)}
        />
      )}

      {/* Sidebar */}
      <aside className={`${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} fixed lg:static inset-y-0 left-0 w-64 bg-white border-r border-slate-200 z-30 transition-transform duration-300 flex flex-col`}>
        <div className="h-16 flex items-center px-6 border-b border-slate-100">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
            <Car size={20} className="text-white" />
          </div>
          <span className="font-bold text-xl tracking-tight text-slate-900">Wash & Brew</span>
          <button className="ml-auto lg:hidden" onClick={() => setIsSidebarOpen(false)}>
            <X size={20} className="text-slate-500" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto py-6 px-4 space-y-1">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 px-3">Main Menu</div>
          <NavItem icon={<MonitorSmartphone />} label="POS / Kasir" isActive={activeTab === 'pos'} onClick={() => {setActiveTab('pos'); setIsSidebarOpen(false);}} />
          <NavItem icon={<LayoutDashboard />} label="Dashboard" isActive={activeTab === 'dashboard'} onClick={() => {setActiveTab('dashboard'); setIsSidebarOpen(false);}} />
          
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mt-8 mb-2 px-3">Admin Panel</div>
          <NavItem icon={<Package />} label="Layanan & Produk" isActive={activeTab === 'products'} onClick={() => {setActiveTab('products'); setIsSidebarOpen(false);}} />
          <NavItem icon={<Users />} label="Pegawai" isActive={activeTab === 'employees'} onClick={() => {setActiveTab('employees'); setIsSidebarOpen(false);}} />
          <NavItem icon={<UserCog />} label="Pengguna" isActive={activeTab === 'users'} onClick={() => {setActiveTab('users'); setIsSidebarOpen(false);}} />
        </div>

        <div className="p-4 border-t border-slate-100">
          <button className="flex items-center w-full px-4 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50 rounded-xl transition-colors">
            <LogOut size={18} className="mr-3" />
            Keluar Sistem
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden relative">
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 lg:px-8 z-10">
          <div className="flex items-center">
            <button className="p-2 mr-2 lg:hidden text-slate-600 hover:bg-slate-100 rounded-lg" onClick={() => setIsSidebarOpen(true)}>
              <Menu size={24} />
            </button>
            <h1 className="text-xl font-semibold text-slate-800 capitalize">
              {activeTab === 'pos' ? 'Point of Sale' : activeTab.replace('-', ' ')}
            </h1>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-sm text-right hidden sm:block">
              <p className="font-medium text-slate-700">Andi Kasir</p>
              <p className="text-xs text-slate-500">Cashier</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-blue-100 border-2 border-white shadow-sm flex items-center justify-center text-blue-700 font-bold">
              AK
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-y-auto bg-slate-50 p-4 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  );

  const NavItem = ({ icon, label, isActive, onClick }) => (
    <button
      onClick={onClick}
      className={`w-full flex items-center px-4 py-3 rounded-xl mb-1 transition-all duration-200 ${
        isActive 
          ? 'bg-blue-50 text-blue-700 font-medium' 
          : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
      }`}
    >
      <span className={`mr-3 ${isActive ? 'text-blue-600' : 'text-slate-400'}`}>
        {React.cloneElement(icon, { size: 20 })}
      </span>
      {label}
    </button>
  );

  // --- VIEWS ---

  const POSView = () => {
    const [cart, setCart] = useState([]);
    const [filter, setFilter] = useState('All');
    const [searchQuery, setSearchQuery] = useState('');
    const [showCheckoutSuccess, setShowCheckoutSuccess] = useState(false);

    const filteredProducts = useMemo(() => {
      return products.filter(p => {
        const matchCategory = filter === 'All' || p.category === filter;
        const matchSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase());
        return matchCategory && matchSearch;
      });
    }, [products, filter, searchQuery]);

    const addToCart = (product) => {
      setCart(prev => {
        const existing = prev.find(item => item.product.id === product.id);
        if (existing) {
          return prev.map(item => item.product.id === product.id ? { ...item, qty: item.qty + 1 } : item);
        }
        return [...prev, { product, qty: 1 }];
      });
    };

    const updateQty = (productId, delta) => {
      setCart(prev => prev.map(item => {
        if (item.product.id === productId) {
          const newQty = item.qty + delta;
          return newQty > 0 ? { ...item, qty: newQty } : item;
        }
        return item;
      }).filter(item => item.qty > 0));
    };

    const cartTotal = cart.reduce((sum, item) => sum + (item.product.price * item.qty), 0);

    const handleCheckout = () => {
      if (cart.length === 0) return;
      const newTrx = {
        id: `TRX-${1000 + transactions.length + 1}`,
        date: new Date().toISOString(),
        total: cartTotal,
        items: cart.map(c => ({ name: c.product.name, qty: c.qty, price: c.product.price }))
      };
      setTransactions([newTrx, ...transactions]);
      setShowCheckoutSuccess(true);
      setCart([]);
      setTimeout(() => setShowCheckoutSuccess(false), 3000);
    };

    return (
      <div className="flex flex-col lg:flex-row gap-6 h-full">
        {/* Left: Products */}
        <div className="flex-1 flex flex-col h-full">
          {/* Filters & Search */}
          <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
            <div className="flex space-x-2 bg-white p-1 rounded-xl shadow-sm border border-slate-200 w-full sm:w-auto">
              {['All', 'Car Wash', 'F&B'].map(cat => (
                <button
                  key={cat}
                  onClick={() => setFilter(cat)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex-1 sm:flex-none ${
                    filter === cat ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
            <div className="relative w-full sm:w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
              <input
                type="text"
                placeholder="Cari menu..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
              />
            </div>
          </div>

          {/* Product Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4 overflow-y-auto pb-20 lg:pb-0 pr-2">
            {filteredProducts.map(product => (
              <div 
                key={product.id} 
                onClick={() => addToCart(product)}
                className="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 hover:border-blue-300 hover:shadow-md transition-all cursor-pointer group flex flex-col h-full"
              >
                <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  {product.icon === 'Car' ? <Car size={24} className="text-blue-600" /> : 
                   product.icon === 'Coffee' ? <Coffee size={24} className="text-amber-600" /> :
                   <Package size={24} className="text-green-600" />}
                </div>
                <div className="mt-auto">
                  <h3 className="font-semibold text-slate-800 text-sm mb-1 leading-tight">{product.name}</h3>
                  <p className="text-blue-600 font-bold">{formatRupiah(product.price)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Cart */}
        <div className="w-full lg:w-96 bg-white rounded-3xl shadow-sm border border-slate-200 flex flex-col h-[500px] lg:h-full shrink-0">
          <div className="p-5 border-b border-slate-100 flex items-center justify-between">
            <h2 className="font-bold text-lg flex items-center">
              <ShoppingCart className="mr-2 text-blue-600" size={20} />
              Pesanan
            </h2>
            <span className="bg-blue-100 text-blue-700 text-xs font-bold px-2.5 py-1 rounded-full">
              {cart.reduce((sum, item) => sum + item.qty, 0)} Item
            </span>
          </div>

          <div className="flex-1 overflow-y-auto p-5 space-y-4">
            {cart.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-slate-400">
                <Receipt size={48} className="mb-4 opacity-20" />
                <p>Belum ada pesanan</p>
              </div>
            ) : (
              cart.map(item => (
                <div key={item.product.id} className="flex justify-between items-center group">
                  <div className="flex-1 pr-4">
                    <h4 className="font-medium text-slate-800 text-sm truncate">{item.product.name}</h4>
                    <p className="text-slate-500 text-xs">{formatRupiah(item.product.price)}</p>
                  </div>
                  <div className="flex items-center space-x-3 bg-slate-50 rounded-lg p-1 border border-slate-100">
                    <button onClick={() => updateQty(item.product.id, -1)} className="w-7 h-7 flex items-center justify-center bg-white rounded shadow-sm text-slate-600 hover:text-blue-600">-</button>
                    <span className="font-semibold text-sm w-4 text-center">{item.qty}</span>
                    <button onClick={() => updateQty(item.product.id, 1)} className="w-7 h-7 flex items-center justify-center bg-white rounded shadow-sm text-slate-600 hover:text-blue-600">+</button>
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="p-5 bg-slate-50 rounded-b-3xl border-t border-slate-100">
            <div className="flex justify-between items-center mb-4">
              <span className="text-slate-500 font-medium">Total Harga</span>
              <span className="text-2xl font-bold text-slate-900">{formatRupiah(cartTotal)}</span>
            </div>
            <button 
              onClick={handleCheckout}
              disabled={cart.length === 0}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-bold py-4 rounded-xl shadow-lg shadow-blue-600/20 transition-all active:scale-[0.98] flex justify-center items-center"
            >
              Proses Pembayaran
            </button>
          </div>
        </div>

        {/* Success Alert */}
        {showCheckoutSuccess && (
          <div className="fixed top-6 left-1/2 -translate-x-1/2 bg-emerald-50 text-emerald-700 px-6 py-3 rounded-full shadow-lg shadow-emerald-900/10 border border-emerald-200 flex items-center z-50 animate-in slide-in-from-top-10 fade-in duration-300">
            <CheckCircle2 size={20} className="mr-2" />
            <span className="font-medium">Pembayaran Berhasil!</span>
          </div>
        )}
      </div>
    );
  };

  const DashboardView = () => {
    const todayTotal = transactions.reduce((sum, trx) => sum + trx.total, 0);
    const todayItems = transactions.reduce((sum, trx) => sum + trx.items.length, 0);

    return (
      <div className="space-y-6">
        {/* Metric Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 flex items-center">
            <div className="w-14 h-14 rounded-2xl bg-blue-50 flex items-center justify-center mr-4">
              <Receipt className="text-blue-600" size={28} />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500 mb-1">Pendapatan Hari Ini</p>
              <h3 className="text-2xl font-bold text-slate-900">{formatRupiah(todayTotal)}</h3>
            </div>
          </div>
          <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 flex items-center">
            <div className="w-14 h-14 rounded-2xl bg-amber-50 flex items-center justify-center mr-4">
              <ShoppingCart className="text-amber-600" size={28} />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500 mb-1">Total Transaksi</p>
              <h3 className="text-2xl font-bold text-slate-900">{transactions.length} Trx</h3>
            </div>
          </div>
          <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 flex items-center">
            <div className="w-14 h-14 rounded-2xl bg-emerald-50 flex items-center justify-center mr-4">
              <Package className="text-emerald-600" size={28} />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500 mb-1">Layanan Terjual</p>
              <h3 className="text-2xl font-bold text-slate-900">{todayItems} Item</h3>
            </div>
          </div>
        </div>

        {/* Recent Transactions */}
        <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
          <div className="px-6 py-5 border-b border-slate-100">
            <h3 className="font-bold text-lg text-slate-800">Riwayat Transaksi Terakhir</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 text-slate-500 text-sm">
                  <th className="px-6 py-4 font-medium">ID Transaksi</th>
                  <th className="px-6 py-4 font-medium">Waktu</th>
                  <th className="px-6 py-4 font-medium">Item</th>
                  <th className="px-6 py-4 font-medium text-right">Total</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {transactions.length === 0 ? (
                  <tr>
                    <td colSpan="4" className="px-6 py-8 text-center text-slate-400">Belum ada transaksi</td>
                  </tr>
                ) : (
                  transactions.map(trx => (
                    <tr key={trx.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="px-6 py-4 font-medium text-slate-900">{trx.id}</td>
                      <td className="px-6 py-4 text-slate-500 text-sm">
                        {new Date(trx.date).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })}
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {trx.items.map(i => `${i.qty}x ${i.name}`).join(', ')}
                      </td>
                      <td className="px-6 py-4 font-semibold text-slate-900 text-right">{formatRupiah(trx.total)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  };

  const AdminProductsView = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState({ name: '', price: '', category: 'Car Wash' });

    const handleSave = (e) => {
      e.preventDefault();
      const newProduct = {
        id: Date.now(),
        name: formData.name,
        price: parseInt(formData.price),
        category: formData.category,
        icon: formData.category === 'Car Wash' ? 'Car' : 'Coffee'
      };
      setProducts([...products, newProduct]);
      setIsModalOpen(false);
      setFormData({ name: '', price: '', category: 'Car Wash' });
    };

    const handleDelete = (id) => {
      setProducts(products.filter(p => p.id !== id));
    };

    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-slate-800">Manajemen Layanan & Produk</h2>
          <button 
            onClick={() => setIsModalOpen(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-medium transition-colors flex items-center shadow-sm"
          >
            <Plus size={18} className="mr-1.5" /> Tambah Produk
          </button>
        </div>

        <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 text-slate-500 text-sm">
                <th className="px-6 py-4 font-medium">Nama Produk</th>
                <th className="px-6 py-4 font-medium">Kategori</th>
                <th className="px-6 py-4 font-medium">Harga</th>
                <th className="px-6 py-4 font-medium text-right">Aksi</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {products.map(p => (
                <tr key={p.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-slate-900 flex items-center">
                    <span className={`w-8 h-8 rounded-lg flex items-center justify-center mr-3 ${p.category === 'Car Wash' ? 'bg-blue-50 text-blue-600' : 'bg-amber-50 text-amber-600'}`}>
                      {p.category === 'Car Wash' ? <Car size={16}/> : <Coffee size={16}/>}
                    </span>
                    {p.name}
                  </td>
                  <td className="px-6 py-4 text-slate-500 text-sm">
                    <span className={`px-2.5 py-1 rounded-md text-xs font-medium ${p.category === 'Car Wash' ? 'bg-blue-100 text-blue-700' : 'bg-amber-100 text-amber-700'}`}>
                      {p.category}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-900 font-medium">{formatRupiah(p.price)}</td>
                  <td className="px-6 py-4 text-right">
                    <button onClick={() => handleDelete(p.id)} className="text-red-500 hover:bg-red-50 p-2 rounded-lg transition-colors">
                      <Trash2 size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Tambah Produk Baru">
          <form onSubmit={handleSave} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Nama Layanan/Produk</label>
              <input 
                required
                type="text" 
                value={formData.name}
                onChange={e => setFormData({...formData, name: e.target.value})}
                className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none"
                placeholder="Misal: Cuci Hidrolik"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Harga (Rp)</label>
              <input 
                required
                type="number" 
                value={formData.price}
                onChange={e => setFormData({...formData, price: e.target.value})}
                className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none"
                placeholder="50000"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Kategori</label>
              <select 
                value={formData.category}
                onChange={e => setFormData({...formData, category: e.target.value})}
                className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none"
              >
                <option value="Car Wash">Car Wash</option>
                <option value="F&B">F&B / Kedai Kopi</option>
              </select>
            </div>
            <div className="pt-4 flex justify-end space-x-3">
              <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-xl font-medium transition-colors">Batal</button>
              <button type="submit" className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-medium transition-colors">Simpan Data</button>
            </div>
          </form>
        </Modal>
      </div>
    );
  };

  const AdminEmployeesView = () => {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-slate-800">Manajemen Pegawai</h2>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-medium transition-colors flex items-center shadow-sm">
            <Plus size={18} className="mr-1.5" /> Tambah Pegawai
          </button>
        </div>
        <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 text-slate-500 text-sm">
                <th className="px-6 py-4 font-medium">Nama Pegawai</th>
                <th className="px-6 py-4 font-medium">Posisi (Role)</th>
                <th className="px-6 py-4 font-medium">No. Telepon</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {employees.map(emp => (
                <tr key={emp.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-slate-900">{emp.name}</td>
                  <td className="px-6 py-4 text-slate-500">
                    <span className={`px-2.5 py-1 rounded-md text-xs font-medium ${emp.role === 'Washer' ? 'bg-indigo-100 text-indigo-700' : 'bg-orange-100 text-orange-700'}`}>
                      {emp.role}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-600">{emp.phone}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  const AdminUsersView = () => {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-slate-800">Manajemen Akun Pengguna</h2>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-medium transition-colors flex items-center shadow-sm">
            <Plus size={18} className="mr-1.5" /> Tambah User
          </button>
        </div>
        <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 text-slate-500 text-sm">
                <th className="px-6 py-4 font-medium">Nama Lengkap</th>
                <th className="px-6 py-4 font-medium">Username</th>
                <th className="px-6 py-4 font-medium">Role Akses</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {users.map(u => (
                <tr key={u.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-slate-900">{u.name}</td>
                  <td className="px-6 py-4 text-slate-600">{u.username}</td>
                  <td className="px-6 py-4 text-slate-500">
                    <span className={`px-2.5 py-1 rounded-md text-xs font-medium ${u.role === 'Admin' ? 'bg-purple-100 text-purple-700' : 'bg-slate-100 text-slate-700'}`}>
                      {u.role}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  // --- RENDER ROUTER ---
  return (
    <Layout>
      {activeTab === 'pos' && <POSView />}
      {activeTab === 'dashboard' && <DashboardView />}
      {activeTab === 'products' && <AdminProductsView />}
      {activeTab === 'employees' && <AdminEmployeesView />}
      {activeTab === 'users' && <AdminUsersView />}
    </Layout>
  );
}
