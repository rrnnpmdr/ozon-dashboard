import json
from collections import defaultdict

with open('data.json') as f:
    raw = json.load(f)

# ── Parse ──
month_order = ['2月','3月','4月','5月','6月']
brands_order = ['FANCL','Centrum','Lacto-fit','Asahi','Earth','foodology','Kao','3CE','Kate','Gucci']

month_label_ru = {'2月':'Фев','3月':'Мар','4月':'Апр','5月':'Май','6月':'Июн'}

# Group by month
by_month = defaultdict(list)
for r in raw:
    by_month[r['monthLabel']].append(r)

# months present
months_present = sorted(set(r['monthLabel'] for r in raw), key=lambda m: month_order.index(m) if m in month_order else 99)
print(f"Months: {months_present}")

# ── 1. Monthly trend ──
monthly = []
for m in months_present:
    recs = by_month[m]
    rev = sum(r['revenue'] for r in recs)
    units = sum(r['ordered_units'] for r in recs)
    returns = sum(r['returns_qty'] for r in recs)
    carts = sum(r['hits_tocart'] for r in recs)
    views = sum(r['hits_view'] for r in recs)
    monthly.append({
        'month': m, 'monthRu': month_label_ru.get(m, m),
        'revenue': round(rev, 2), 'units': units,
        'returns': returns, 'cartRate': round(carts/views*100, 2) if views else 0,
        'aov': round(rev/units, 2) if units else 0
    })

# ── 2. Brand monthly breakdown ──
brand_monthly = defaultdict(lambda: defaultdict(lambda: {'revenue':0,'units':0,'returns':0,'views':0,'carts':0}))
for r in raw:
    b = r['brand'] or '其他'
    m = r['monthLabel']
    brand_monthly[b][m]['revenue'] += r['revenue']
    brand_monthly[b][m]['units'] += r['ordered_units']
    brand_monthly[b][m]['returns'] += r['returns_qty']
    brand_monthly[b][m]['views'] += r['hits_view']
    brand_monthly[b][m]['carts'] += r['hits_tocart']

# Brand summary
brand_summary = []
for b in sorted(brand_monthly.keys()):
    total_rev = sum(d['revenue'] for d in brand_monthly[b].values())
    total_units = sum(d['units'] for d in brand_monthly[b].values())
    months_with_data = [m for m in months_present if m in brand_monthly[b]]
    first_month = months_with_data[0] if months_with_data else ''
    last_month = months_with_data[-1] if months_with_data else ''
    
    # Growth from first to last
    if len(months_with_data) >= 2:
        first_rev = sum(brand_monthly[b][first_month]['revenue'] for m in [first_month])
        last_rev = sum(brand_monthly[b][last_month]['revenue'] for m in [last_month])
        growth = round((last_rev - first_rev) / first_rev * 100, 1) if first_rev > 0 else 0
    else:
        growth = 0
    
    monthly_breakdown = []
    for m in months_present:
        if m in brand_monthly[b]:
            d = brand_monthly[b][m]
            monthly_breakdown.append({
                'month': m,
                'revenue': round(d['revenue'], 2),
                'units': d['units'],
                'returns': d['returns'],
                'cartRate': round(d['carts']/d['views']*100, 2) if d['views'] else 0
            })
    
    brand_summary.append({
        'brand': b,
        'totalRevenue': round(total_rev, 2),
        'totalUnits': total_units,
        'growth': growth,
        'months': months_with_data,
        'monthly': monthly_breakdown
    })

brand_summary.sort(key=lambda x: x['totalRevenue'], reverse=True)

# ── 3. SKU analysis ──
# Aggregate per SKU
sku_all = defaultdict(lambda: {'revenue':0,'units':0,'returns':0,'views':0,'carts':0,'brand':'','months':set()})
sku_monthly = defaultdict(dict)
for r in raw:
    key = r['offer_id'] or 'unknown'
    b = r['brand'] or '其他'
    m = r['monthLabel']
    sku_all[key]['revenue'] += r['revenue']
    sku_all[key]['units'] += r['ordered_units']
    sku_all[key]['returns'] += r['returns_qty']
    sku_all[key]['views'] += r['hits_view']
    sku_all[key]['carts'] += r['hits_tocart']
    sku_all[key]['brand'] = b
    sku_all[key]['months'].add(m)
    sku_monthly[key][m] = {
        'revenue': r['revenue'],
        'units': r['ordered_units']
    }

# Per SKU growth (4月 vs 5月) and ranking
sku_growth = []
sku_fall = []
sku_details = []
for sku, d in sku_all.items():
    sm = sku_monthly[sku]
    
    # 4月 vs 5月
    apr_rev = sm.get('4月', {}).get('revenue', 0) or 0
    may_rev = sm.get('5月', {}).get('revenue', 0) or 0
    apr_units = sm.get('4月', {}).get('units', 0) or 0
    may_units = sm.get('5月', {}).get('units', 0) or 0
    jun_rev = sm.get('6月', {}).get('revenue', 0) or 0
    jun_units = sm.get('6月', {}).get('units', 0) or 0
    
    total_rev = d['revenue']
    total_units = d['units']
    return_rate = round(d['returns']/d['units']*100, 2) if d['units'] else 0
    cart_rate = round(d['carts']/d['views']*100, 2) if d['views'] else 0
    aov = round(total_rev/total_units, 2) if total_units else 0
    brand = d['brand']
    sku_details.append({
        'sku': sku, 'brand': brand,
        'totalRevenue': round(total_rev, 2), 'totalUnits': total_units,
        'aprRevenue': round(apr_rev, 2), 'mayRevenue': round(may_rev, 2),
        'junRevenue': round(jun_rev, 2),
        'aprUnits': apr_units, 'mayUnits': may_units, 'junUnits': jun_units,
        'growthMayApr': round((may_rev - apr_rev) / apr_rev * 100, 1) if apr_rev > 0 else 0,
        'returnRate': return_rate, 'cartRate': cart_rate, 'aov': aov,
        'monthsActive': len(d['months'])
    })

# Growth leaders (4→5月, min ₽5000 base in either month)
sku_details.sort(key=lambda x: x['totalRevenue'], reverse=True)
growth_leaders = sorted([s for s in sku_details if s['aprRevenue'] >= 5000 or s['mayRevenue'] >= 5000], key=lambda x: x['growthMayApr'], reverse=True)[:30]
growth_fallers = sorted([s for s in sku_details if s['aprRevenue'] >= 5000 or s['mayRevenue'] >= 5000], key=lambda x: x['growthMayApr'])[:30]

# Detect possible rename (old SKU drops → new SKU with similar name rises)
fancl_plus = [s for s in sku_details if 'Plus' in s['sku'] and s['brand'] == 'FANCL']
fancl_women = [s for s in sku_details if 'Women' in s['sku'] and 'Plus' not in s['sku'] and s['brand'] == 'FANCL']

# ── 4. Brand ranking ──
brand_ranking = sorted(brand_summary, key=lambda x: x['totalRevenue'], reverse=True)

# ── 5. Monthly brand share ──
brand_share = {}
for m in months_present:
    recs = by_month[m]
    total = sum(r['revenue'] for r in recs)
    brand_share[m] = {}
    for r in recs:
        b = r['brand'] or '其他'
        brand_share[m][b] = brand_share[m].get(b, 0) + r['revenue']
    for b in brand_share[m]:
        brand_share[m][b] = round(brand_share[m][b] / total * 100, 1)

# ── Output analysis JSON ──
output = {
    'months': months_present,
    'monthlyTrend': monthly,
    'brandRanking': [{
        'brand': b['brand'],
        'totalRevenue': b['totalRevenue'],
        'totalUnits': b['totalUnits'],
        'growth': b['growth'],
        'monthly': b['monthly']
    } for b in brand_ranking],
    'skuGrowthLeaders': [{
        'sku': s['sku'], 'brand': s['brand'],
        'aprRevenue': s['aprRevenue'], 'mayRevenue': s['mayRevenue'], 'junRevenue': s['junRevenue'],
        'growthMayApr': s['growthMayApr'], 'totalRevenue': s['totalRevenue']
    } for s in growth_leaders[:15]],
    'skuGrowthFallers': [{
        'sku': s['sku'], 'brand': s['brand'],
        'aprRevenue': s['aprRevenue'], 'mayRevenue': s['mayRevenue'], 'junRevenue': s['junRevenue'],
        'growthMayApr': s['growthMayApr'], 'totalRevenue': s['totalRevenue']
    } for s in growth_fallers[:15]],
    'brandShare': brand_share,
    'allSkuDetails': [{
        'sku': s['sku'], 'brand': s['brand'],
        'totalRevenue': s['totalRevenue'], 'totalUnits': s['totalUnits'],
        'mayRevenue': s['mayRevenue'], 'junRevenue': s['junRevenue'],
        'growthMayApr': s['growthMayApr'], 'returnRate': s['returnRate'],
        'cartRate': s['cartRate'], 'aov': s['aov'], 'monthsActive': s['monthsActive']
    } for s in sku_details]
}

with open('analysis.json', 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Months: {months_present}")
print(f"Brands: {len(brand_summary)}")
print(f"SKUs: {len(sku_details)}")
print(f"Growth leaders (4→5月): {len(growth_leaders)}")
print(f"Growth fallers (4→5月): {len(growth_fallers)}")
print("Analysis saved to analysis.json")
