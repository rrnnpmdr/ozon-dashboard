"""Generate the enhanced index.html + report.html for ozon-dashboard"""
import json

with open('analysis.json') as f:
    data = json.load(f)

# ──────────────────────────────────────
# PART 1: Enhanced index.html (add views, cart rate, conversion, return rate)
# ──────────────────────────────────────

index_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ozon 销售仪表板</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f0f13;color:#e0e0e0;padding:20px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}
.header h1{font-size:24px;font-weight:600;color:#fff}
.header h1 span{color:#6c8cff}
.header .links{display:flex;gap:12px}
.header .links a{color:#6c8cff;text-decoration:none;font-size:13px;padding:6px 14px;border:1px solid #2a2a3a;border-radius:8px;transition:all .15s}
.header .links a:hover{background:#1a1a24;border-color:#6c8cff}
.last-update{font-size:13px;color:#888}
.filters{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap}
.filter-group{display:flex;flex-direction:column;gap:4px}
.filter-group label{font-size:12px;color:#888;font-weight:500}
.filter-group select,.filter-group input{background:#1a1a24;border:1px solid #2a2a3a;border-radius:8px;padding:8px 12px;color:#e0e0e0;font-size:13px;min-width:160px;outline:none}
.filter-group select:focus,.filter-group input:focus{border-color:#6c8cff}
.stats-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:24px}
.stat-card{background:#1a1a24;border-radius:12px;padding:16px;border:1px solid #2a2a3a}
.stat-card .label{font-size:11px;color:#888;margin-bottom:4px}
.stat-card .value{font-size:20px;font-weight:600;color:#fff}
.stat-card .sub{font-size:11px;color:#666;margin-top:2px}
.charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}
.chart-card{background:#1a1a24;border-radius:12px;padding:20px;border:1px solid #2a2a3a}
.chart-card.full{grid-column:1/-1}
.chart-card h3{font-size:14px;color:#aaa;margin-bottom:12px;font-weight:500}
.chart-card canvas{max-height:320px;height:320px;width:100%!important}
.chart-card .chart-small canvas{max-height:200px;height:200px}
.metrics-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:16px}
.metric-card{background:#1a1a24;border-radius:8px;padding:12px;border:1px solid #2a2a3a;display:flex;justify-content:space-between}
.metric-card .ml{font-size:12px;color:#888}
.metric-card .mv{font-size:16px;font-weight:600;color:#e0e0e0}
.sku-table-wrap{background:#1a1a24;border-radius:12px;border:1px solid #2a2a3a;overflow:hidden}
.sku-table-wrap h3{font-size:14px;color:#aaa;font-weight:500;padding:16px 20px 0}
.table-header{display:flex;justify-content:space-between;align-items:center;padding:12px 20px;flex-wrap:wrap;gap:8px}
.table-search input{background:#0f0f13;border:1px solid #2a2a3a;border-radius:6px;padding:6px 10px;color:#e0e0e0;font-size:13px;width:200px;outline:none}
.table-search input:focus{border-color:#6c8cff}
table{width:100%;border-collapse:collapse;font-size:12px}
th{background:#14141e;color:#888;font-weight:500;padding:8px 10px;text-align:left;position:sticky;top:0;cursor:pointer;user-select:none;white-space:nowrap}
th:hover{color:#ccc}
th .sort-icon{margin-left:3px;font-size:9px;color:#555}
th.sorted .sort-icon{color:#6c8cff}
td{padding:6px 10px;border-top:1px solid #22222e}
tr:hover td{background:#1e1e2c}
.sku-name{font-weight:500;color:#ddd;font-size:12px}
.badge{display:inline-block;padding:2px 6px;border-radius:4px;font-size:11px;font-weight:500}
.badge-up{color:#51cf66;background:rgba(81,207,102,.12)}
.badge-down{color:#ff6b6b;background:rgba(255,107,107,.12)}
.pagination{display:flex;justify-content:center;align-items:center;padding:16px;gap:12px}
.pagination button{background:#2a2a3a;border:none;border-radius:6px;padding:6px 14px;color:#ccc;cursor:pointer;font-size:13px}
.pagination button:hover{background:#3a3a4e}
.pagination button:disabled{opacity:.3;cursor:default}
.pagination span{font-size:13px;color:#888}
@media(max-width:900px){.charts-grid{grid-template-columns:1fr}}
</style>
</head>
<body>

<div class="header">
  <h1>📊 <span>Ozon</span> 销售仪表板</h1>
  <div style="display:flex;align-items:center;gap:16px">
    <div class="last-update" id="lastUpdate"></div>
    <div class="links">
      <a href="report.html" target="_blank">📈 深度分析</a>
    </div>
  </div>
</div>

<div class="filters">
  <div class="filter-group">
    <label>月份</label>
    <select id="monthFilter"><option value="all">全部月份</option></select>
  </div>
  <div class="filter-group">
    <label>品牌</label>
    <select id="brandFilter"><option value="all">全部品牌</option></select>
  </div>
  <div class="filter-group">
    <label>搜索 offer_id</label>
    <input type="text" id="skuSearch" placeholder="输入 offer_id...">
  </div>
  <div class="filter-group">
    <label>排序</label>
    <select id="sortBy">
      <option value="revenue">销售额 ↓</option>
      <option value="units">销量 ↓</option>
      <option value="views">展现量 ↓</option>
      <option value="cart_rate">加购率 ↓</option>
      <option value="conversion">转化率 ↓</option>
      <option value="returns">退货数 ↓</option>
      <option value="name">名称 ↑</option>
    </select>
  </div>
</div>

<div class="stats-row" id="statsRow">
  <div class="stat-card"><div class="label">总销售额</div><div class="value" id="statRevenue">—</div><div class="sub">₽</div></div>
  <div class="stat-card"><div class="label">总销量</div><div class="value" id="statUnits">—</div><div class="sub">件</div></div>
  <div class="stat-card"><div class="label">活跃 SKU</div><div class="value" id="statSku">—</div><div class="sub">有销量</div></div>
  <div class="stat-card"><div class="label">退货率</div><div class="value" id="statReturnRate">—</div><div class="sub">%</div></div>
  <div class="stat-card"><div class="label">平均客单价</div><div class="value" id="statAov">—</div><div class="sub">₽</div></div>
  <div class="stat-card"><div class="label">加购率</div><div class="value" id="statCartRate">—</div><div class="sub">%</div></div>
  <div class="stat-card"><div class="label">展现量</div><div class="value" id="statViews">—</div><div class="sub">次</div></div>
  <div class="stat-card"><div class="label">转化率</div><div class="value" id="statConv">—</div><div class="sub">%</div></div>
</div>

<div class="charts-grid">
  <div class="chart-card full">
    <h3>📈 月度趋势（销售额 + 展现量 + 加购率）</h3>
    <canvas id="trendChart"></canvas>
  </div>
  <div class="chart-card">
    <h3>🥧 品牌占比</h3>
    <canvas id="brandChart"></canvas>
  </div>
  <div class="chart-card">
    <h3>🏆 品牌 TOP5 月度走势</h3>
    <canvas id="brandTrendChart"></canvas>
  </div>
  <div class="chart-card full">
    <h3>🔥 TOP15 SKU 销售额</h3>
    <canvas id="topSkuChart"></canvas>
  </div>
</div>

<div class="sku-table-wrap" id="skuTableWrap">
  <h3>📋 SKU 明细</h3>
  <div class="table-header">
    <div class="table-search">
      <input type="text" id="tableSearch" placeholder="搜索 offer_id 或品牌...">
    </div>
    <span id="tableCount" style="font-size:13px;color:#888;"></span>
  </div>
  <div style="max-height:500px;overflow-y:auto;">
    <table>
      <thead>
        <tr>
          <th data-col="offer_id" class="sorted">offer_id <span class="sort-icon">▲</span></th>
          <th data-col="brand">品牌</th>
          <th data-col="revenue" style="text-align:right;">销售额 <span class="sort-icon">▼</span></th>
          <th data-col="ordered_units" style="text-align:right;">销量</th>
          <th data-col="views" style="text-align:right;">展现量</th>
          <th data-col="cart_rate" style="text-align:right;">加购率</th>
          <th data-col="conversion" style="text-align:right;">转化率</th>
          <th data-col="returns_qty" style="text-align:right;">退货</th>
          <th data-col="return_rate" style="text-align:right;">退货率</th>
          <th data-col="avg_price" style="text-align:right;">均价</th>
        </tr>
      </thead>
      <tbody id="skuTableBody"></tbody>
    </table>
  </div>
  <div class="pagination">
    <button id="prevPage" disabled>← 上一页</button>
    <span id="pageInfo">1 / 1</span>
    <button id="nextPage" disabled>下一页 →</button>
  </div>
</div>

<script>
const DB_URL = 'data.json';
let allData = [];
let rawData = [];
let chartInstances = {};
const PAGE_SIZE = 20;
let currentPage = 1;
let sortCol = 'revenue';
let sortDir = 'desc';
let tableData = [];

async function loadData() {
  try {
    const resp = await fetch(DB_URL);
    rawData = await resp.json();
    allData = rawData;
    initFilters();
    render();
    document.getElementById('lastUpdate').textContent = '数据更新: ' + new Date().toLocaleString('zh-CN');
  } catch(e) {
    document.getElementById('statsRow').innerHTML = '<div style="padding:40px;text-align:center;color:#ff6b6b;">❌ 加载数据失败: ' + e.message + '</div>';
  }
}

function initFilters() {
  const months = [...new Set(rawData.map(d => d.monthLabel))].sort();
  const brands = [...new Set(rawData.map(d => d.brand).filter(Boolean))].sort();
  months.forEach(m => { const o = document.createElement('option'); o.value = m; o.textContent = m; document.getElementById('monthFilter').appendChild(o); });
  brands.forEach(b => { const o = document.createElement('option'); o.value = b; o.textContent = b; document.getElementById('brandFilter').appendChild(o); });
}

function getFiltered() {
  const month = document.getElementById('monthFilter').value;
  const brand = document.getElementById('brandFilter').value;
  const search = document.getElementById('skuSearch').value.trim().toLowerCase();
  let data = allData;
  if (month !== 'all') data = data.filter(d => d.monthLabel === month);
  if (brand !== 'all') data = data.filter(d => d.brand === brand);
  if (search) data = data.filter(d => d.offer_id && d.offer_id.toLowerCase().includes(search));
  return data;
}

function aggregateBySku(data) {
  const map = {};
  data.forEach(d => {
    const key = d.offer_id || 'unknown';
    if (!map[key]) map[key] = { offer_id: key, brand: d.brand || '', revenue: 0, ordered_units: 0, returns_qty: 0, hits_view: 0, hits_tocart: 0 };
    map[key].revenue += d.revenue || 0;
    map[key].ordered_units += d.ordered_units || 0;
    map[key].returns_qty += d.returns_qty || 0;
    map[key].hits_view += d.hits_view || 0;
    map[key].hits_tocart += d.hits_tocart || 0;
  });
  return Object.values(map);
}

function aggregateByMonth(data) {
  const map = {};
  data.forEach(d => {
    const key = d.monthLabel;
    if (!map[key]) map[key] = { month: key, revenue: 0, ordered_units: 0, hits_view: 0, hits_tocart: 0 };
    map[key].revenue += d.revenue || 0;
    map[key].ordered_units += d.ordered_units || 0;
    map[key].hits_view += d.hits_view || 0;
    map[key].hits_tocart += d.hits_tocart || 0;
  });
  return Object.values(map).sort((a, b) => a.month.localeCompare(b.month));
}

function aggregateByBrand(data) {
  const map = {};
  data.forEach(d => {
    const key = d.brand || '其他';
    if (!map[key]) map[key] = { brand: key, revenue: 0, ordered_units: 0 };
    map[key].revenue += d.revenue || 0;
    map[key].ordered_units += d.ordered_units || 0;
  });
  return Object.values(map).sort((a, b) => b.revenue - a.revenue);
}

function aggregateBrandMonthly(data) {
  const map = {};
  data.forEach(d => {
    const bk = d.brand || '其他';
    const mk = d.monthLabel;
    if (!map[bk]) map[bk] = {};
    if (!map[bk][mk]) map[bk][mk] = 0;
    map[bk][mk] += d.revenue || 0;
  });
  return map;
}

function render() {
  const filtered = getFiltered();
  const skuAgg = aggregateBySku(filtered);
  const monthAgg = aggregateByMonth(filtered);
  const brandAgg = aggregateByBrand(filtered);

  // Stats
  const totalRevenue = skuAgg.reduce((s, d) => s + d.revenue, 0);
  const totalUnits = skuAgg.reduce((s, d) => s + d.ordered_units, 0);
  const totalReturns = skuAgg.reduce((s, d) => s + d.returns_qty, 0);
  const totalViews = skuAgg.reduce((s, d) => s + d.hits_view, 0);
  const totalCarts = skuAgg.reduce((s, d) => s + d.hits_tocart, 0);
  const activeSku = skuAgg.filter(d => d.ordered_units > 0).length;
  const returnRate = totalUnits > 0 ? (totalReturns / totalUnits * 100) : 0;
  const aov = totalUnits > 0 ? (totalRevenue / totalUnits) : 0;
  const cartRate = totalViews > 0 ? (totalCarts / totalViews * 100) : 0;
  const conversion = totalViews > 0 ? (totalUnits / totalViews * 100) : 0;

  document.getElementById('statRevenue').textContent = totalRevenue.toLocaleString('ru-RU', {minimumFractionDigits:2});
  document.getElementById('statUnits').textContent = totalUnits.toLocaleString();
  document.getElementById('statSku').textContent = activeSku;
  document.getElementById('statReturnRate').textContent = returnRate.toFixed(2);
  document.getElementById('statAov').textContent = aov.toLocaleString('ru-RU', {minimumFractionDigits:2});
  document.getElementById('statCartRate').textContent = cartRate.toFixed(2);
  document.getElementById('statViews').textContent = totalViews.toLocaleString();
  document.getElementById('statConv').textContent = conversion.toFixed(3);

  renderTrend(monthAgg);
  renderBrandPie(brandAgg);
  renderTopSku(skuAgg);
  renderBrandTrend(filtered);
  renderTable(skuAgg);
}

function renderTrend(monthAgg) {
  const ctx = document.getElementById('trendChart').getContext('2d');
  if (chartInstances.trend) chartInstances.trend.destroy();
  const labels = monthAgg.map(d => d.month);
  const revenue = monthAgg.map(d => d.revenue);
  const units = monthAgg.map(d => d.ordered_units);
  const views = monthAgg.map(d => d.hits_view);
  const cartRates = monthAgg.map(d => d.hits_view > 0 ? +(d.hits_tocart / d.hits_view * 100).toFixed(2) : 0);

  chartInstances.trend = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        { label: '销售额 (₽)', data: revenue, borderColor: '#6c8cff', backgroundColor: 'rgba(108,140,255,0.1)', fill: true, tension: 0.3, yAxisID: 'y', pointRadius: 4 },
        { label: '展现量', data: views, borderColor: '#51cf66', backgroundColor: 'rgba(81,207,102,0.1)', fill: true, tension: 0.3, yAxisID: 'y1', pointRadius: 4, borderDash: [5,5] },
        { label: '加购率 (%)', data: cartRates, borderColor: '#ffb86c', tension: 0.3, yAxisID: 'y2', pointRadius: 3, borderWidth: 2 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { labels: { color: '#888', usePointStyle: true, padding: 16 } },
        tooltip: { backgroundColor: '#1a1a24', titleColor: '#e0e0e0', bodyColor: '#ccc', borderColor: '#2a2a3a', borderWidth: 1, padding: 10,
          callbacks: { label: ctx => ctx.dataset.label + ': ' + (ctx.parsed.y || 0).toLocaleString('ru-RU') }
        }
      },
      scales: {
        x: { ticks: { color: '#666' }, grid: { color: '#22222e' } },
        y: { type: 'linear', position: 'left', ticks: { color: '#888', callback: v => v >= 1000000 ? (v/1000000).toFixed(1)+'M' : v >= 1000 ? (v/1000).toFixed(0)+'K' : v }, grid: { color: '#22222e' } },
        y1: { type: 'linear', position: 'right', grid: { display: false }, ticks: { color: '#888', callback: v => v >= 1000000 ? (v/1000000).toFixed(1)+'M' : v >= 1000 ? (v/1000).toFixed(0)+'K' : v } },
        y2: { type: 'linear', position: 'right', grid: { display: false }, ticks: { color: '#ffb86c', callback: v => v.toFixed(1)+'%' }, max: Math.max(...cartRates) * 2 || 5 }
      }
    }
  });
}

function renderBrandPie(brandAgg) {
  const ctx = document.getElementById('brandChart').getContext('2d');
  if (chartInstances.brand) chartInstances.brand.destroy();
  const colors = ['#6c8cff','#ff6b6b','#ffb86c','#51cf66','#cc5de8','#20c997','#fcc419','#ff922b','#748ffc','#e599f7','#888'];
  const top = brandAgg.slice(0, 10);
  chartInstances.brand = new Chart(ctx, {
    type: 'doughnut',
    data: { labels: top.map(d => d.brand), datasets: [{ data: top.map(d => d.revenue), backgroundColor: colors.slice(0, top.length), borderWidth: 0 }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { color: '#888', padding: 10, font: { size: 11 } } },
        tooltip: { backgroundColor: '#1a1a24', titleColor: '#e0e0e0', bodyColor: '#ccc', borderColor: '#2a2a3a', borderWidth: 1,
          callbacks: { label: ctx => { const t = ctx.dataset.data.reduce((a,b)=>a+b,0); return ctx.label + ': ₽' + (+ctx.parsed).toLocaleString() + ' (' + (+ctx.parsed/t*100).toFixed(1) + '%)'; } }
        }
      }
    }
  });
}

function renderBrandTrend(filtered) {
  const ctx = document.getElementById('brandTrendChart').getContext('2d');
  if (chartInstances.brandTrend) chartInstances.brandTrend.destroy();

  const bm = {};
  filtered.forEach(d => {
    const b = d.brand || '其他';
    const m = d.monthLabel;
    if (!bm[b]) bm[b] = {};
    bm[b][m] = (bm[b][m] || 0) + (d.revenue || 0);
  });

  const months = [...new Set(filtered.map(d => d.monthLabel))].sort();
  const topBrands = Object.entries(bm)
    .map(([b, ms]) => [b, Object.values(ms).reduce((s,v)=>s+v,0)])
    .sort((a,b) => b[1] - a[1])
    .slice(0, 5)
    .map(x => x[0]);

  const colors = ['#6c8cff','#ff6b6b','#ffb86c','#51cf66','#cc5de8'];
  const datasets = topBrands.map((b, i) => ({
    label: b,
    data: months.map(m => bm[b][m] || 0),
    borderColor: colors[i],
    backgroundColor: colors[i] + '22',
    fill: false,
    tension: 0.3,
    pointRadius: 3
  }));

  chartInstances.brandTrend = new Chart(ctx, {
    type: 'line',
    data: { labels: months, datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { labels: { color: '#888', usePointStyle: true, padding: 12 } },
        tooltip: { backgroundColor: '#1a1a24', titleColor: '#e0e0e0', bodyColor: '#ccc', borderColor: '#2a2a3a', borderWidth: 1, callbacks: { label: ctx => ctx.dataset.label + ': ₽' + (+ctx.parsed.y).toLocaleString('ru-RU') } }
      },
      scales: {
        x: { ticks: { color: '#666' }, grid: { color: '#22222e' } },
        y: { ticks: { color: '#888', callback: v => v >= 1000 ? (v/1000).toFixed(0)+'K' : v }, grid: { color: '#22222e' } }
      }
    }
  });
}

function renderTopSku(skuAgg) {
  const ctx = document.getElementById('topSkuChart').getContext('2d');
  if (chartInstances.topSku) chartInstances.topSku.destroy();
  const sorted = [...skuAgg].sort((a, b) => b.revenue - a.revenue).slice(0, 15);
  chartInstances.topSku = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sorted.map(d => d.offer_id || 'unknown'),
      datasets: [
        { label: '销售额 (₽)', data: sorted.map(d => d.revenue), backgroundColor: '#6c8cff', borderRadius: 4, borderSkipped: false },
        { label: '销量 (件)', data: sorted.map(d => d.ordered_units), backgroundColor: '#ffb86c', borderRadius: 4, borderSkipped: false }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false, indexAxis: 'y',
      plugins: {
        legend: { labels: { color: '#888', usePointStyle: true, padding: 12 } },
        tooltip: { backgroundColor: '#1a1a24', titleColor: '#e0e0e0', bodyColor: '#ccc', borderColor: '#2a2a3a', borderWidth: 1, callbacks: { label: ctx => ctx.dataset.label + ': ' + (+ctx.parsed.x).toLocaleString('ru-RU') } }
      },
      scales: {
        x: { ticks: { color: '#888', callback: v => v >= 1000 ? (v/1000).toFixed(0)+'K' : v }, grid: { color: '#22222e' } },
        y: { ticks: { color: '#888', font: { size: 10 } }, grid: { display: false } }
      }
    }
  });
}

function renderTable(skuAgg) {
  tableData = [...skuAgg];
  tableData.sort((a, b) => {
    let va, vb;
    const s = document.getElementById('sortBy').value;
    if (s === 'revenue') { sortCol = 'revenue'; sortDir = 'desc'; va = a.revenue; vb = b.revenue; }
    else if (s === 'units') { sortCol = 'ordered_units'; sortDir = 'desc'; va = a.ordered_units; vb = b.ordered_units; }
    else if (s === 'views') { sortCol = 'hits_view'; sortDir = 'desc'; va = a.hits_view; vb = b.hits_view; }
    else if (s === 'cart_rate') { sortCol = 'cart_rate'; sortDir = 'desc'; va = a.hits_view > 0 ? a.hits_tocart/a.hits_view : 0; vb = b.hits_view > 0 ? b.hits_tocart/b.hits_view : 0; }
    else if (s === 'conversion') { sortCol = 'conversion'; sortDir = 'desc'; va = a.hits_view > 0 ? a.ordered_units/a.hits_view : 0; vb = b.hits_view > 0 ? b.ordered_units/b.hits_view : 0; }
    else if (s === 'returns') { sortCol = 'returns_qty'; sortDir = 'desc'; va = a.returns_qty; vb = b.returns_qty; }
    else if (s === 'name') { sortCol = 'offer_id'; sortDir = 'asc'; va = (a.offer_id || '').toLowerCase(); vb = (b.offer_id || '').toLowerCase(); }
    if (va < vb) return sortDir === 'asc' ? -1 : 1;
    if (va > vb) return sortDir === 'asc' ? 1 : -1;
    return 0;
  });

  const q = document.getElementById('tableSearch').value.trim().toLowerCase();
  let display = tableData;
  if (q) display = display.filter(d => (d.offer_id && d.offer_id.toLowerCase().includes(q)) || (d.brand && d.brand.toLowerCase().includes(q)));

  document.getElementById('tableCount').textContent = display.length + ' 条记录';
  const totalPages = Math.ceil(display.length / PAGE_SIZE) || 1;
  if (currentPage > totalPages) currentPage = totalPages;
  const start = (currentPage - 1) * PAGE_SIZE;
  const page = display.slice(start, start + PAGE_SIZE);

  document.getElementById('skuTableBody').innerHTML = page.map(d => {
    const rr = d.ordered_units > 0 ? (d.returns_qty / d.ordered_units * 100) : 0;
    const avg = d.ordered_units > 0 ? (d.revenue / d.ordered_units) : 0;
    const conv = d.hits_view > 0 ? (d.ordered_units / d.hits_view * 100) : 0;
    const cr = d.hits_view > 0 ? (d.hits_tocart / d.hits_view * 100) : 0;
    return `<tr>
      <td class="sku-name">${d.offer_id || '—'}</td>
      <td>${d.brand || '—'}</td>
      <td style="text-align:right;">₽${d.revenue.toLocaleString('ru-RU')}</td>
      <td style="text-align:right;">${d.ordered_units}</td>
      <td style="text-align:right;">${(d.hits_view || 0).toLocaleString()}</td>
      <td style="text-align:right;">${cr.toFixed(2)}%</td>
      <td style="text-align:right;">${conv.toFixed(3)}%</td>
      <td style="text-align:right;">${d.returns_qty}</td>
      <td style="text-align:right;">${rr.toFixed(1)}%</td>
      <td style="text-align:right;">₽${avg.toLocaleString('ru-RU', {minimumFractionDigits:2})}</td>
    </tr>`;
  }).join('');

  document.getElementById('pageInfo').textContent = currentPage + ' / ' + totalPages;
  document.getElementById('prevPage').disabled = currentPage <= 1;
  document.getElementById('nextPage').disabled = currentPage >= totalPages;
}

document.getElementById('monthFilter').addEventListener('change', () => { currentPage=1; render(); });
document.getElementById('brandFilter').addEventListener('change', () => { currentPage=1; render(); });
document.getElementById('skuSearch').addEventListener('input', () => { currentPage=1; render(); });
document.getElementById('tableSearch').addEventListener('input', () => { currentPage=1; render(); });
document.getElementById('sortBy').addEventListener('change', () => { currentPage=1; render(); });
document.getElementById('prevPage').addEventListener('click', () => { if(currentPage>1){currentPage--;render();} });
document.getElementById('nextPage').addEventListener('click', () => { const t=Math.ceil(tableData.length/PAGE_SIZE); if(currentPage<t){currentPage++;render();} });

loadData();
</script>
</body>
</html>"""

with open('index.html', 'w') as f:
    f.write(index_template)
print("✅ index.html written with new metrics")
