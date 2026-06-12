import json

with open('data.json') as f:
    raw = json.load(f)

# ── Build analysis ──
from collections import defaultdict

month_order = ['2月','3月','4月','5月','6月']
month_label_ru = {'2月':'Фев','3月':'Мар','4月':'Апр','5月':'Май','6月':'Июн'}

by_month = defaultdict(list)
for r in raw:
    by_month[r['monthLabel']].append(r)

months_present = sorted(set(r['monthLabel'] for r in raw), key=lambda m: month_order.index(m) if m in month_order else 99)

# Monthly trend
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
        'returns': returns,
        'views': views, 'carts': carts,
        'cartRate': round(carts/views*100, 2) if views else 0,
        'conversion': round(units/views*100, 2) if views else 0,
        'returnRate': round(returns/units*100, 2) if units else 0,
        'aov': round(rev/units, 2) if units else 0
    })

# Brand monthly
brand_monthly = defaultdict(lambda: defaultdict(lambda: {'revenue':0,'units':0,'returns':0,'views':0,'carts':0}))
for r in raw:
    b = r['brand'] or '其他'
    m = r['monthLabel']
    brand_monthly[b][m]['revenue'] += r['revenue']
    brand_monthly[b][m]['units'] += r['ordered_units']
    brand_monthly[b][m]['returns'] += r['returns_qty']
    brand_monthly[b][m]['views'] += r['hits_view']
    brand_monthly[b][m]['carts'] += r['hits_tocart']

brand_summary = []
for b in sorted(brand_monthly.keys()):
    d_monthly = brand_monthly[b]
    total_rev = sum(d['revenue'] for d in d_monthly.values())
    total_units = sum(d['units'] for d in d_monthly.values())
    total_returns = sum(d['returns'] for d in d_monthly.values())
    total_views = sum(d['views'] for d in d_monthly.values())
    total_carts = sum(d['carts'] for d in d_monthly.values())
    
    months_with_data = sorted([m for m in months_present if m in d_monthly], key=lambda x: month_order.index(x))
    
    if len(months_with_data) >= 2:
        first_rev = d_monthly[months_with_data[0]]['revenue']
        last_rev = d_monthly[months_with_data[-1]]['revenue']
        growth = round((last_rev - first_rev) / first_rev * 100, 1) if first_rev > 0 else 0
    else:
        growth = 0
    
    monthly_b = []
    for m in months_present:
        if m in d_monthly:
            d = d_monthly[m]
            monthly_b.append({
                'month': m,
                'revenue': round(d['revenue'], 2),
                'units': d['units'],
                'returns': d['returns'],
                'views': d['views'],
                'carts': d['carts'],
                'cartRate': round(d['carts']/d['views']*100, 2) if d['views'] else 0,
                'conversion': round(d['units']/d['views']*100, 2) if d['views'] else 0
            })
    
    brand_summary.append({
        'brand': b,
        'totalRevenue': round(total_rev, 2),
        'totalUnits': total_units,
        'totalReturns': total_returns,
        'totalViews': total_views,
        'totalCarts': total_carts,
        'cartRate': round(total_carts/total_views*100, 2) if total_views else 0,
        'conversion': round(total_units/total_views*100, 2) if total_views else 0,
        'returnRate': round(total_returns/total_units*100, 2) if total_units else 0,
        'growth': growth,
        'monthly': monthly_b
    })

brand_summary.sort(key=lambda x: x['totalRevenue'], reverse=True)

# SKU analysis
sku_data = defaultdict(lambda: {
    'revenue':0,'units':0,'returns':0,'views':0,'carts':0,
    'brand':'','months':set()
})
sku_monthly = defaultdict(lambda: defaultdict(lambda: {'revenue':0,'units':0,'returns':0,'views':0,'carts':0}))
for r in raw:
    key = r['offer_id'] or 'unknown'
    b = r['brand'] or '其他'
    m = r['monthLabel']
    sd = sku_data[key]
    sd['revenue'] += r['revenue']
    sd['units'] += r['ordered_units']
    sd['returns'] += r['returns_qty']
    sd['views'] += r['hits_view']
    sd['carts'] += r['hits_tocart']
    sd['brand'] = b
    sd['months'].add(m)
    
    sm = sku_monthly[key][m]
    sm['revenue'] = sm.get('revenue',0) + r['revenue']
    sm['units'] = sm.get('units',0) + r['ordered_units']
    sm['returns'] = sm.get('returns',0) + r['returns_qty']
    sm['views'] = sm.get('views',0) + r['hits_view']
    sm['carts'] = sm.get('carts',0) + r['hits_tocart']

sku_details = []
for sku, d in sku_data.items():
    sm = sku_monthly[sku]
    apr = sm.get('4月', {'revenue':0,'units':0,'views':0,'carts':0})
    may = sm.get('5月', {'revenue':0,'units':0,'views':0,'carts':0})
    jun = sm.get('6月', {'revenue':0,'units':0,'views':0,'carts':0})
    
    total_rev = d['revenue']
    total_units = d['units']
    total_returns = d['returns']
    total_views = d['views']
    total_carts = d['carts']
    
    sku_details.append({
        'sku': sku, 'brand': d['brand'],
        'totalRevenue': round(total_rev, 2),
        'totalUnits': total_units,
        'totalReturns': total_returns,
        'totalViews': total_views,
        'totalCarts': total_carts,
        'cartRate': round(total_carts/total_views*100, 2) if total_views else 0,
        'conversion': round(total_units/total_views*100, 2) if total_views else 0,
        'returnRate': round(total_returns/total_units*100, 2) if total_units else 0,
        'aov': round(total_rev/total_units, 2) if total_units else 0,
        'aprRevenue': round(apr['revenue'], 2),
        'mayRevenue': round(may['revenue'], 2),
        'junRevenue': round(jun['revenue'], 2),
        'aprUnits': apr['units'],
        'mayUnits': may['units'],
        'junUnits': jun['units'],
        'growthMayApr': round((may['revenue'] - apr['revenue']) / apr['revenue'] * 100, 1) if apr['revenue'] > 0 else 0,
        'monthsActive': len(d['months'])
    })

sku_details.sort(key=lambda x: x['totalRevenue'], reverse=True)

# Growth leaders/fallers (base ≥₽5000)
growth_leaders = sorted(
    [s for s in sku_details if s['aprRevenue'] >= 5000 or s['mayRevenue'] >= 5000],
    key=lambda x: x['growthMayApr'], reverse=True
)[:15]

growth_fallers = sorted(
    [s for s in sku_details if s['aprRevenue'] >= 5000 or s['mayRevenue'] >= 5000],
    key=lambda x: x['growthMayApr']
)[:15]

# Brand share by month
brand_share = {}
for m in months_present:
    recs = by_month[m]
    total = sum(r['revenue'] for r in recs)
    share = defaultdict(float)
    for r in recs:
        b = r['brand'] or '其他'
        share[b] += r['revenue']
    brand_share[m] = {b: round(v/total*100, 1) for b, v in sorted(share.items(), key=lambda x: x[1], reverse=True)}

# Top brands for comparison
top_brands = [b['brand'] for b in brand_summary[:8]]

output = {
    'months': months_present,
    'monthlyTrend': monthly,
    'brandRanking': [{
        'brand': b['brand'],
        'totalRevenue': b['totalRevenue'],
        'totalUnits': b['totalUnits'],
        'totalViews': b['totalViews'],
        'totalCarts': b['totalCarts'],
        'cartRate': b['cartRate'],
        'conversion': b['conversion'],
        'returnRate': b['returnRate'],
        'growth': b['growth'],
        'monthly': b['monthly']
    } for b in brand_summary],
    'skuGrowthLeaders': [{
        'sku': s['sku'], 'brand': s['brand'],
        'aprRevenue': s['aprRevenue'], 'mayRevenue': s['mayRevenue'], 'junRevenue': s['junRevenue'],
        'growthMayApr': s['growthMayApr'], 'totalRevenue': s['totalRevenue'],
        'aprUnits': s['aprUnits'], 'mayUnits': s['mayUnits']
    } for s in growth_leaders],
    'skuGrowthFallers': [{
        'sku': s['sku'], 'brand': s['brand'],
        'aprRevenue': s['aprRevenue'], 'mayRevenue': s['mayRevenue'], 'junRevenue': s['junRevenue'],
        'growthMayApr': s['growthMayApr'], 'totalRevenue': s['totalRevenue'],
        'aprUnits': s['aprUnits'], 'mayUnits': s['mayUnits']
    } for s in growth_fallers],
    'brandShare': brand_share,
    'topBrands': top_brands,
    'allSkuDetails': [{
        'sku': s['sku'], 'brand': s['brand'],
        'totalRevenue': s['totalRevenue'],
        'totalUnits': s['totalUnits'],
        'totalReturns': s['totalReturns'],
        'totalViews': s['totalViews'],
        'totalCarts': s['totalCarts'],
        'cartRate': s['cartRate'],
        'conversion': s['conversion'],
        'returnRate': s['returnRate'],
        'aov': s['aov'],
        'mayRevenue': s['mayRevenue'],
        'junRevenue': s['junRevenue'],
        'growthMayApr': s['growthMayApr'],
        'monthsActive': s['monthsActive']
    } for s in sku_details]
}

with open('analysis.json', 'w') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Done! Months: {months_present}, Brands: {len(brand_summary)}, SKUs: {len(sku_details)}")
print(f"Growth leaders: {len(growth_leaders)}, Fallers: {len(growth_fallers)}")
print(f"Analysis JSON size: {len(json.dumps(output, ensure_ascii=False))} chars")
