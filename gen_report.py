import json

with open('analysis.json') as f:
    D = json.load(f)

data_json = json.dumps(D, ensure_ascii=False)

html = open('report_template.html').read() if False else """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ozon 深度分析报告</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
*{M0Mpadding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f0f13;color:#e0e0e0;padding:20px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}
.header h1{font-size:22px;font-weight:600;color:#fff}
.header h1 span{color:#6c8cff}
.header a{color:#6c8cff;text-decoration:none;font-size:13px;padding:6px 14px;border:1px solid #2a2a3a;border-radius:8px;transition:all .15s}
.header a:hover{background:#1a1a24}
.tabs{display:flex;gap:0;margin-bottom:16px;border-bottom:1px solid #2a2a3a;overflow-x:auto}
.tab-btn{background:transparent;border:none;padding:10px 20px;color:#666;font-size:13px;cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap;transition:all .2s}
.tab-btn.active{color:#6c8cff;border-bottom-color:#6c8cff}
.tab-btn:hover{color:#aaa}
.tab-content{display:none}
.tab-content.active{display:block}
.stats-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:20px}
.stat-card{background:#1a1a24;border-radius:12px;padding:16px;border:1px solid #2a2a3a}
.stat-card .label{font-size:11px;color:#888;margin-bottom:4px}
.stat-card .value{font-size:20px;font-weight:600;color:#fff}
.stat-card .sub{font-size:11px;color:#666;margin-top:2px}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px}
.chart-card{background:#1a1a24;border-radius:12px;padding:20px;border:1px solid #2a2a3a;overflow:hidden}
.chart-card.full{grid-column:1/-1}
.chart-card h3{font-size:14px;color:#aaa;margin-bottom:12px;font-weight:500}
.chart-card canvas{max-height:300px;height:300px;width:100%!important}
.insight-box{background:linear-gradient(135deg,#1a1a44,#1a1a24);border:1px solid #2a2a5a;border-radius:12px;padding:16px;margin-bottom:16px}
.insight-box h3{font-size:14px;color:#6c8cff;margin-bottom:8px}
.insight-box ul{margin-left:16px;font-size:13px;color:#ccc;line-height:1.8}
.insight-box strong{color:#fff}
table{width:100%;border-collapse:collapse;font-size:12px}
th{background:#14141e;color:#888;font-weight:500;padding:8px 10px;text-align:left;position:sticky;top:0;white-space:nowrap}
td{padding:6px 10px;border-top:1px solid #22222e}
tr:hover td{background:#1e1e2c}
.text-right{text-align:right}
.green{color:#51cf66}
.red{color:#ff6b6b}
.brand-filter{margin-bottom:12px;display:flex;gap:8px;flex-wrap:wrap}
.brand-tag{padding:4px 12px;border-radius:20px;border:1px solid #2a2a3a;font-size:12px;cursor:pointer;color:#888;background:transparent;transition:all .15s}
.brand-tag.active{border-color:#6c8cff;color:#6c8cff;background:rgba(108,140,255,.1)}
.brand-tag:hover{border-color:#555;color:#ccc}
.filter-row{display:flex;gap:12px;margin-bottom:12px;flex-wrap:wrap}
.filter-row select,.filter-row input{background:#1a1a24;border:1px solid #2a2a3a;border-radius:8px;padding:6px 10px;color:#e0e0e0;font-size:13px;outline:none}
.filter-row select:focus,.filter-row input:focus{border-color:#6c8cff}
@media(max-width:900px){.chart-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="header"><h1>📈 Ozon <span>深度分析报告</span></h1><a href="index.html">← 返回仪表板</a></div>
<div class="tabs" id="tabHeaders">
  <button class="tab-btn active" data-tab="overview">📋 总览</button>
  <button class="tab-btn" data-tab="brands">🏷️ 品牌明细</button>
  <button class="tab-btn" data-tab="growth">📈 增长分析</button>
  <button class="tab-btn" data-tab="skus">📦 SKU诊断</button>
</div>
<div id="tab-overview" class="tab-content active">
  <div class="insight-box"><h3>🔍 核心发现</h3><ul id="coreInsights"></ul></div>
  <div class="stats-row" id="overviewStats"></div>
  <div class="chart-grid">
    <div class="chart-card full"><h3>📈 月度趋势（销售额 + 展现量 + 加购率 + 转化率）</h3><canvas id="ovTrendChart"></canvas></div>
    <div class="chart-card"><h3>🥧 品牌占比 TOP8</h3><canvas id="ovBrandPie"></canvas></div>
    <div class="chart-card"><h3>🏆 TOP5 品牌月度走势</h3><canvas id="ovBrandTrend"></canvas></div>
  </div>
</div>
<div id="tab-brands" class="tab-content">
  <div class="brand-filter" id="brandFilterTags"></div>
  <div id="brandDetails"></div>
</div>
<div id="tab-growth" class="tab-content">
  <div class="chart-grid">
    <div class="chart-card"><h3>品牌增长排行（收入>5万₽）</h3><canvas id="gBrandRank"></canvas></div>
    <div class="chart-card"><h3>📈 SKU涨幅 TOP10</h3><canvas id="gSkuGainers"></canvas></div>
    <div class="chart-card"><h3>📉 SKU跌幅 TOP10</h3><canvas id="gSkuLosers"></canvas></div>
    <div class="chart-card"><h3>📊 品牌健康度指数（2月=100）</h3><canvas id="gBrandIndex"></canvas></div>
  </div>
</div>
<div id="tab-skus" class="tab-content">
  <div class="filter-row">
    <select id="skuBrandFilter"><option value="all">全部品牌</option></select>
    <input id="skuSearchFilter" placeholder="🔍 搜索offer_id...">
    <select id="skuSortFilter">
      <option value="revenue">销售额 ↓</option>
      <option value="units">销量 ↓</option>
      <option value="views">展现量 ↓</option>
      <option value="growth">5月增长 ↓</option>
      <option value="conversion">转化率 ↓</option>
      <option value="cartRate">加购率 ↓</option>
    </select>
  </div>
  <div class="chart-card full" style="padding:0">
    <div style="max-height:600px;overflow-y:auto"><table>
      <thead><tr>
        <th>offer_id</th><th>品牌</th>
        <th class="text-right">总销售额</th><th class="text-right">总销量</th>
        <th class="text-right">展现量</th><th class="text-right">加购率</th>
        <th class="text-right">转化率</th><th class="text-right">均价</th>
        <th class="text-right">5月收入</th><th class="text-right">6月收入</th>
        <th class="text-right">4→5月</th><th class="text-right">月数</th>
      </tr></thead>
      <tbody id="skuDetailTable"></tbody>
    </table></div>
  </div>
  <div id="skuCount" style="padding:12px;text-align:center;font-size:12px;color:#888"></div>
</div>
<script>
const D = __DATA_JSON__;

const months = D.months;
const colors = ['#6c8cff','#ff6b6b','#ffb86c','#51cf66','#cc5de8','#20c997','#fcc419','#ff922b','#748ffc','#e599f7'];
const fm = x => x.toLocaleString('ru-RU', {minimumFractionDigits:2});
const fi = x => x.toLocaleString();
const f1 = x => x.toFixed(1);
document.getElementById('tabHeaders').addEventListener('click', e => {
  const btn = e.target.closest('.tab-btn');
  if (!btn) return;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
});
function renderOverview() {
  const mt = D.monthlyTrend;
  const totalR = mt.reduce((s,m) => s + m.revenue, 0);
  const totalU = mt.reduce((s,m) => s + m.units, 0);
  const totalV = mt.reduce((s,m) => s + m.views, 0);
  const totalC = mt.reduce((s,m) => s + m.carts, 0);
  const totalRt = mt.reduce((s,m) => s + (m.returns||0), 0);
  document.getElementById('overviewStats').innerHTML =
    '<div class="stat-card"><div class="label">2-6月总销售额</div><div class="value">₽'+fm(totalR)+'</div></div>'+
    '<div class="stat-card"><div class="label">总销量</div><div class="value">'+fi(totalU)+'</div><div class="sub">件</div></div>'+
    '<div class="stat-card"><div class="label">展现量</div><div class="value">'+fi(totalV)+'</div><div class="sub">次</div></div>'+
    '<div class="stat-card"><div class="label">加购率</div><div class="value">'+f1(totalC/totalV*100)+'%</div></div>'+
    '<div class="stat-card"><div class="label">转化率</div><div class="value">'+(totalU/totalV*100).toFixed(3)+'%</div></div>'+
    '<div class="stat-card"><div class="label">退换率</div><div class="value">'+f1(totalRt/totalU*100)+'%</div></div>'+
    '<div class="stat-card"><div class="label">5月销售额</div><div class="value">₽'+fm(mt[3].revenue)+'</div></div>'+
    '<div class="stat-card"><div class="label">6月(11天)</div><div class="value">₽'+fm(mt[4].revenue)+'</div><div class="sub">进行中</div></div>';
  const topB = D.brandRanking[0];
  const fastest = D.brandRanking.reduce((a,b) => a.growth > b.growth ? a : b);
  const slowest = D.brandRanking.reduce((a,b) => a.growth < b.growth ? a : b);
  document.getElementById('coreInsights').innerHTML =
    '<li><strong>总销售额:</strong> ₽'+fm(totalR)+'（2-6月累计），峰值在3月（₽'+fm(mt[1].revenue)+'），之后连续下滑</li>'+
    '<li><strong>增长最快:</strong> '+fastest.brand+'（'+f1(fastest.growth)+'%）</li>'+
    '<li><strong>下滑最严重:</strong> '+slowest.brand+'（'+f1(slowest.growth)+'%）</li>'+
    '<li><strong>加购率趋势:</strong> '+mt.map(m=>m.month+' '+f1(m.cartRate)+'%').join(' → ')+'，逐月下降</li>'+
    '<li><strong>转化率趋势:</strong> '+mt.map(m=>m.month+' '+f1(m.conversion)+'%').join(' → ')+'</li>'+
    '<li><strong>Top品牌:</strong> '+topB.brand+' 占总收入 '+f1(topB.totalRevenue/totalR*100)+'%（₽'+fm(topB.totalRevenue)+'）</li>';
  new Chart(document.getElementById('ovTrendChart').getContext('2d'), {
    type:'line', data:{labels:mt.map(m=>m.month),
      datasets:[
        {label:'销售额(₽)',data:mt.map(m=>m.revenue),borderColor:'#6c8cff',backgroundColor:'rgba(108,140,255,0.1)',fill:true,tension:.3,yAxisID:'y',pointRadius:4},
        {label:'展现量',data:mt.map(m=>m.views),borderColor:'#51cf66',tension:.3,yAxisID:'y1',pointRadius:3,borderDash:[4,4]},
        {label:'加购率(%)',data:mt.map(m=>m.cartRate),borderColor:'#ffb86c',tension:.3,yAxisID:'y2',pointRadius:3,borderWidth:2},
        {label:'转化率(%)',data:mt.map(m=>m.conversion),borderColor:'#cc5de8',tension:.3,yAxisID:'y2',pointRadius:3,borderWidth:2,borderDash:[4,4]}
      ]},
    options:{
      responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
      plugins:{legend:{labels:{color:'#888',usePointStyle:true,padding:12}}},
      scales:{
        x:{ticks:{color:'#666'},grid:{color:'#22222e'}},
        y:{type:'linear',position:'left',ticks:{color:'#888',callback:v=>v>=1e6?(v/1e6).toFixed(1)+'M':v>=1e3?(v/1e3).toFixed(0)+'K':v},grid:{color:'#22222e'}},
        y1:{type:'linear',position:'right',grid:{display:false},ticks:{color:'#51cf66',callback:v=>v>=1e6?(v/1e6).toFixed(1)+'M':v>=1e3?(v/1e3).toFixed(0)+'K':v}},
        y2:{type:'linear',position:'right',grid:{display:false},ticks:{color:'#888',callback:v=>v.toFixed(1)+'%'}}
      }
    }
  });
  const top8 = D.brandRanking.slice(0,8);
  new Chart(document.getElementById('ovBrandPie').getContext('2d'), {
    type:'doughnut',
    data:{labels:top8.map(b=>b.brand),datasets:[{data:top8.map(b=>b.totalRevenue),backgroundColor:colors.slice(0,8),borderWidth:0}]},
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{
        legend:{position:'right',labels:{color:'#888',padding:8,font:{size:11}}},
        tooltip:{backgroundColor:'#1a1a24',titleColor:'#e0e0e0',bodyColor:'#ccc',borderColor:'#2a2a3a',borderWidth:1,
          callbacks:{label:ctx=>{const t=ctx.dataset.data.reduce((a,b)=>a+b,0);return ctx.label+': ₽'+(+ctx.parsed).toLocaleString()+' ('+(+ctx.parsed/t*100).toFixed(1)+'%)'}}}
      }
    }
  });
  const top5 = D.brandRanking.slice(0,5);
  const bm={};top5.forEach(b=>{bm[b.brand]={};b.monthly.forEach(m=>{bm[b.brand][m.month]=m.revenue})});
  new Chart(document.getElementById('ovBrandTrend').getContext('2d'), {
    type:'line',
    data:{labels:months,datasets:top5.map((b,i)=>({label:b.brand,data:months.map(m=>bm[b.brand][m]||0),borderColor:colors[i],tension:.3,pointRadius:3}))},
    options:{
      responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
      plugins:{legend:{labels:{color:'#888',usePointStyle:true,padding:10}}},
      scales:{x:{ticks:{color:'#666'},grid:{color:'#22222e'}},y:{ticks:{color:'#888',callback:v=>v>=1e3?(v/1e3).toFixed(0)+'K':v},grid:{color:'#22222e'}}}
    }
  });
}
function renderBrands() {
  const tags = document.getElementById('brandFilterTags');
  const allB = D.brandRanking.map(b=>b.brand);
  let selBrand = null;
  tags.innerHTML = '<button class="brand-tag active" data-brand="all">全部</button>'+allB.map(b=>'<button class="brand-tag" data-brand="'+b+'">'+b+'</button>').join('');
  tags.addEventListener('click',e=>{const btn=e.target.closest('.brand-tag');if(!btn)return;tags.querySelectorAll('.brand-tag').forEach(t=>t.classList.remove('active'));btn.classList.add('active');selBrand=btn.dataset.brand==='all'?null:btn.dataset.brand;renderBrandCards();});
  renderBrandCards();
}
function renderBrandCards() {
  let brands = D.brandRanking;
  if(selBrand) brands=brands.filter(b=>b.brand===selBrand);
  document.getElementById('brandDetails').innerHTML = brands.map(b=>{
    const m=b.monthly,lastM=m[m.length-1],prevM=m.length>=2?m[m.length-2]:null;
    const moM=prevM?((lastM.revenue-prevM.revenue)/prevM.revenue*100).toFixed(1):'—';
    return '<div class="chart-card" style="margin-bottom:12px">'+
      '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap">'+
        '<span style="font-size:16px;font-weight:600;color:#fff">'+b.brand+'</span>'+
        '<span style="font-size:12px;color:#888">₽'+fm(b.totalRevenue)+' | '+fi(b.totalUnits)+'件 | '+fi(b.totalViews)+'展现</span>'+
      '</div>'+
      '<div style="display:flex;gap:16px;margin-bottom:8px;font-size:12px;color:#888;flex-wrap:wrap">'+
        '<span>加购率: <b style="color:#e0e0e0">'+f1(b.cartRate)+'%</b></span>'+
        '<span>转化率: <b style="color:#e0e0e0">'+f1(b.conversion)+'%</b></span>'+
        '<span>2→5月增长: <b class="'+(b.growth>=0?'green':'red')+'">'+(b.growth>=0?'+':'')+f1(b.growth)+'%</b></span>'+
        '<span>环比: <b class="'+(moM>=0?'green':'red')+'">'+(moM>=0?'+':'')+moM+'%</b></span>'+
      '</div>'+
      '<div style="aspect-ratio:4;max-height:100px"><canvas id="bc_'+b.brand.replace(/[^a-z0-9]/gi,'_')+'"></canvas></div>'+
    '</div>';
  }).join('');
  brands.forEach(b=>{
    const el=document.getElementById('bc_'+b.brand.replace(/[^a-z0-9]/gi,'_'));if(!el)return;
    new Chart(el.getContext('2d'),{type:'line',data:{labels:b.monthly.map(m=>m.month),datasets:[{label:'销售额',data:b.monthly.map(m=>m.revenue),borderColor:'#6c8cff',tension:.3,fill:true,backgroundColor:'rgba(108,140,255,0.05)'}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#555',font:{size:10}}},y:{ticks:{color:'#555',font:{size:10},callback:v=>v>=1e3?(v/1e3).toFixed(0)+'K':v}}}}
    });
  });
}
function renderGrowth() {
  const sb=[...D.brandRanking].filter(b=>b.growth!==0&&b.totalRevenue>50000).sort((a,b)=>b.growth-a.growth);
  new Chart(document.getElementById('gBrandRank').getContext('2d'),{type:'bar',data:{labels:sb.map(b=>b.brand),datasets:[{label:'增长率(%)',data:sb.map(b=>b.growth),backgroundColor:sb.map(b=>b.growth>=0?'rgba(81,207,102,0.6)':'rgba(255,107,107,0.6)'),borderColor:sb.map(b=>b.growth>=0?'#51cf66':'#ff6b6b'),borderWidth:1}]},
  options:{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#888'}},y:{ticks:{color:'#888',font:{size:10}}}}}});
  const gn=D.skuGrowthLeaders.filter(s=>s.sku!=='unknown').slice(0,10);
  new Chart(document.getElementById('gSkuGainers').getContext('2d'),{type:'bar',data:{labels:gn.map(s=>s.sku.substring(0,15)+'...'),datasets:[{label:'4→5月增长(%)',data:gn.map(s=>s.growthMayApr),backgroundColor:'rgba(81,207,102,0.6)',borderColor:'#51cf66',borderWidth:1}]},
  options:{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#888'}},y:{ticks:{color:'#888',font:{size:10}}}}}});
  const fl=D.skuGrowthFallers.filter(s=>s.sku!=='unknown').slice(0,10);
  new Chart(document.getElementById('gSkuLosers').getContext('2d'),{type:'bar',data:{labels:fl.map(s=>s.sku.substring(0,15)+'...'),datasets:[{label:'4→5月增长(%)',data:fl.map(s=>s.growthMayApr),backgroundColor:'rgba(255,107,107,0.6)',borderColor:'#ff6b6b',borderWidth:1}]},
  options:{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#888'}},y:{ticks:{color:'#888',font:{size:10}}}}}});
  const ib=D.brandRanking.filter(b=>b.monthly[0]&&b.monthly[0].revenue>0&&b.totalRevenue>30000).slice(0,8);
  const bix={};ib.forEach(b=>{bix[b.brand]={};b.monthly.forEach(m=>{bix[b.brand][m.month]=m.revenue})});
  new Chart(document.getElementById('gBrandIndex').getContext('2d'),{type:'line',data:{labels:months,datasets:ib.map((b,i)=>({label:b.brand,data:months.map(m=>{const v=bix[b.brand][m]||0;const bv=bix[b.brand][months[0]]||1;return v/bv*100}),borderColor:colors[i],tension:.3,pointRadius:2}))},
  options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{labels:{color:'#888',font:{size:10},usePointStyle:true,padding:8}}},scales:{x:{ticks:{color:'#666'}},y:{ticks:{color:'#888',callback:v=>v.toFixed(0)}}}}});
}
function renderSkuTable() {
  const bf=document.getElementById('skuBrandFilter');
  if(bf.options.length<=1){const brands=[...new Set(D.allSkuDetails.map(s=>s.brand))].sort();brands.forEach(b=>bf.add(new Option(b,b)));}
  let data=[...D.allSkuDetails];
  const bfv=bf.value;if(bfv!=='all')data=data.filter(s=>s.brand===bfv);
  const q=document.getElementById('skuSearchFilter').value.trim().toLowerCase();if(q)data=data.filter(s=>s.sku.toLowerCase().includes(q));
  const sortBy=document.getElementById('skuSortFilter').value;
  const order={revenue:'totalRevenue',units:'totalUnits',views:'totalViews',growth:'growthMayApr',conversion:'conversion',cartRate:'cartRate'};
  const field=order[sortBy]||'totalRevenue';
  data.sort((a,b)=>b[field]-a[field]);
  document.getElementById('skuDetailTable').innerHTML=data.map(s=>{
    const g=s.growthMayApr||0;
    return '<tr><td style="max-width:180px;overflow:hidden;text-overflow:ellipsis">'+s.sku+'</td><td>'+s.brand+'</td>'+
      '<td class="text-right">₽'+fm(s.totalRevenue)+'</td><td class="text-right">'+fi(s.totalUnits)+'</td>'+
      '<td class="text-right">'+fi(s.totalViews)+'</td><td class="text-right">'+f1(s.cartRate)+'%</td>'+
      '<td class="text-right">'+f1(s.conversion)+'%</td>'+
      '<td class="text-right">₽'+fm(s.aov)+'</td><td class="text-right">₽'+fm(s.mayRevenue)+'</td>'+
      '<td class="text-right">₽'+fm(s.junRevenue)+'</td>'+
      '<td class="text-right"><span class="'+(g>=0?'green':'red')+'">'+(g>=0?'+':'')+f1(g)+'%</span></td>'+
      '<td class="text-right">'+s.monthsActive+'</td></tr>';
  }).join('');
  document.getElementById('skuCount').textContent=data.length+' 条记录';
}
document.getElementById('skuBrandFilter').addEventListener('change',renderSkuTable);
document.getElementById('skuSearchFilter').addEventListener('input',renderSkuTable);
document.getElementById('skuSortFilter').addEventListener('change',renderSkuTable);
renderOverview();renderBrands();renderGrowth();renderSkuTable();
</script>
</body>
</html>
"""

html = html.replace('__DATA_JSON__', data_json)
# Replace M0M with {margin:0 (to avoid f-string issues)
html = html.replace('M0M', '{margin:0')

with open('report.html', 'w') as f:
    f.write(html)
print('Written', len(html), 'bytes')
