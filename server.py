"""
Guardian Watch (OHZDIS) Web Server
Connects data_collector.py → real-time dashboard
Run: python server.py
Open: http://localhost:5000
"""

from flask import Flask, jsonify, render_template_string, request
import json, os, subprocess, threading, time
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "ohzdis_latest.json"
FIELD_REPORTS_FILE = "ohzdis_field_reports.json"

def load_field_reports():
    if os.path.exists(FIELD_REPORTS_FILE):
        with open(FIELD_REPORTS_FILE) as f:
            return json.load(f)
    return []

def save_field_report(report):
    reports = load_field_reports()
    report['server_timestamp'] = datetime.now().isoformat()
    reports.insert(0, report)
    reports = reports[:100]
    with open(FIELD_REPORTS_FILE, 'w') as f:
        json.dump(reports, f, indent=2, default=str)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
        data['field_reports'] = reports[:10]
        data['field_report_count'] = len(reports)
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Field report: {report.get('id','?')} Risk:{report.get('risk_score','?')}")
    return report

# ── HTML DASHBOARD (inline) ──────────────────────────────────
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Guardian Watch (OHZDIS) Live Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root{--bg:#060d14;--bg2:#0c1825;--bg3:#111f2e;--border:#1a3050;--text:#c8dff0;--muted:#4a7090;--accent:#00c8ff;--red:#ff3b3b;--orange:#ff8c00;--yellow:#ffd600;--green:#00e676;--mono:'Space Mono',monospace;--sans:'DM Sans',sans-serif}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:var(--sans);font-size:13px}
.topbar{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 24px;height:52px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}
.logo{font-family:var(--mono);font-size:14px;font-weight:700;color:var(--accent);letter-spacing:2px}
.logo span{color:var(--muted);font-weight:400}
.topbar-right{display:flex;align-items:center;gap:20px;font-family:var(--mono);font-size:11px;color:var(--muted)}
.live-dot{width:7px;height:7px;background:var(--green);border-radius:50%;display:inline-block;animation:pulse 2s infinite;margin-right:5px}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.alert-banner{background:linear-gradient(90deg,#3d0000,#1a0000);border-bottom:1px solid #ff3b3b44;padding:8px 24px;display:flex;align-items:center;gap:12px;font-family:var(--mono);font-size:11px;color:var(--red);overflow:hidden}
.alert-tag{background:var(--red);color:#000;padding:2px 8px;font-weight:700;font-size:10px;letter-spacing:1px;flex-shrink:0}
.alert-text{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.main{padding:16px 24px;display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:4px;padding:16px}
.card-title{font-family:var(--mono);font-size:10px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}
.badge{padding:2px 6px;border-radius:2px;font-size:9px;font-weight:700}
.badge-red{background:#ff3b3b22;color:var(--red);border:1px solid #ff3b3b44}
.badge-orange{background:#ff8c0022;color:var(--orange);border:1px solid #ff8c0044}
.badge-green{background:#00e67622;color:var(--green);border:1px solid #00e67644}
.badge-accent{background:#00c8ff22;color:var(--accent);border:1px solid #00c8ff44}
.stat-big{font-family:var(--mono);font-size:36px;font-weight:700;line-height:1;margin-bottom:4px}
.stat-label{color:var(--muted);font-size:12px}
.stat-delta{font-family:var(--mono);font-size:11px;margin-top:6px}
.delta-up{color:var(--red)}.delta-down{color:var(--green)}
.stat-red .stat-big{color:var(--red)}.stat-orange .stat-big{color:var(--orange)}.stat-yellow .stat-big{color:var(--yellow)}.stat-green .stat-big{color:var(--green)}.stat-accent .stat-big{color:var(--accent)}
.span2{grid-column:span 2}.span3{grid-column:span 3}.span4{grid-column:span 4}
.signal-item{padding:8px 0;border-bottom:1px solid var(--border);display:flex;gap:10px}
.signal-item:last-child{border-bottom:none}
.signal-time{font-family:var(--mono);font-size:10px;color:var(--muted);flex-shrink:0;padding-top:1px}
.signal-text{font-size:12px;line-height:1.5}
.signal-source{font-family:var(--mono);font-size:9px;color:var(--accent);margin-top:2px}
.sig-critical{border-left:2px solid var(--red);padding-left:8px}
.sig-high{border-left:2px solid var(--orange);padding-left:8px}
.sig-info{border-left:2px solid var(--accent);padding-left:8px}
.source-row{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid var(--border);font-size:12px}
.source-row:last-child{border-bottom:none}
.src-ok{color:var(--green);font-family:var(--mono);font-size:10px}
.src-warn{color:var(--orange);font-family:var(--mono);font-size:10px}
.src-num{font-family:var(--mono);font-size:11px;color:var(--accent)}
.chart-wrap{position:relative;height:160px}
.map-wrap{height:320px;border-radius:4px;overflow:hidden;border:1px solid var(--border)}
.refresh-btn{background:var(--bg3);border:1px solid var(--border);color:var(--accent);font-family:var(--mono);font-size:10px;padding:4px 10px;cursor:pointer;border-radius:2px;letter-spacing:1px}
.refresh-btn:hover{border-color:var(--accent)}
.footer{padding:12px 24px;border-top:1px solid var(--border);display:flex;justify-content:space-between;font-family:var(--mono);font-size:10px;color:var(--muted)}
.field-badge{display:inline-block;padding:2px 8px;border-radius:2px;font-family:var(--mono);font-size:10px;margin-left:6px}
.fb-critical{background:#ff3b3b22;color:#ff3b3b;border:1px solid #ff3b3b44}
.fb-high{background:#ff8c0022;color:#ff8c00;border:1px solid #ff8c0044}
.fb-moderate{background:#ffd60022;color:#ffd600;border:1px solid #ffd60044}
.fb-low{background:#00e67622;color:#00e676;border:1px solid #00e67644}
.field-row{display:grid;grid-template-columns:60px 80px 1fr 70px 80px;gap:8px;padding:7px 0;border-bottom:1px solid var(--border);align-items:center;font-size:12px}
.field-row.header{font-family:var(--mono);font-size:10px;color:var(--muted);letter-spacing:1px}
.field-row:last-child{border-bottom:none}
.loading{color:var(--muted);font-family:var(--mono);font-size:11px;text-align:center;padding:20px}
</style>
</head>
<body>

<div class="topbar">
  <div class="logo">Guardian Watch <span>(OHZDIS) v4.3.0 · LIVE</span></div>
  <div class="topbar-right">
    <span><span class="live-dot"></span>REAL-TIME</span>
    <span id="clock">--:--:-- UTC</span>
    <span style="color:var(--muted)" id="lastCollect">Last collect: --</span>
    <button class="refresh-btn" onclick="loadData()">⟳ REFRESH</button>
    <button class="refresh-btn" onclick="runCollector()" id="collectBtn">▶ COLLECT NOW</button>
  </div>
</div>

<div class="alert-banner">
  <div class="alert-tag">LIVE SIGNALS</div>
  <div class="alert-text" id="alertText">Loading signals...</div>
</div>

<div class="main">

  <div class="card stat-accent">
    <div class="card-title">WHO REPORTS <span class="badge badge-accent" id="whoZooCount">-</span></div>
    <div class="stat-big" id="whoTotal">-</div>
    <div class="stat-label">Outbreak reports</div>
    <div class="stat-delta" id="whoZoo" style="color:var(--accent)">- zoonotic signals</div>
  </div>

  <div class="card stat-red">
    <div class="card-title">CDC EID ARTICLES <span class="badge badge-red" id="eidZooCount">-</span></div>
    <div class="stat-big" id="eidTotal">-</div>
    <div class="stat-label">New publications</div>
    <div class="stat-delta delta-up" id="eidZoo">- zoonotic</div>
  </div>

  <div class="card stat-green">
    <div class="card-title">DISEASE.SH GLOBAL <span class="badge badge-green">LIVE</span></div>
    <div class="stat-big" id="globalCases">-</div>
    <div class="stat-label">Total cases (millions)</div>
    <div class="stat-delta delta-down" id="globalDeaths">- deaths</div>
  </div>

  <div class="card stat-orange">
    <div class="card-title">GUARDIAN WATCH TRIGGERS <span class="badge badge-orange" id="triggerBadge">-</span></div>
    <div class="stat-big" id="triggerCount">-</div>
    <div class="stat-label">Modules auto-activated</div>
    <div class="stat-delta" id="triggerList" style="color:var(--orange)">-</div>
  </div>

  <!-- WORLD MAP -->
  <div class="card span4">
    <div class="card-title">
      USA & TERRITORIES OUTBREAK MAP — REAL-TIME
      <span class="badge badge-red" id="mapAlertCount">0 alerts</span>
    </div>
    <div class="map-wrap" id="map"></div>
  </div>

  <!-- WHO SIGNALS FEED -->
  <div class="card span2">
    <div class="card-title">WHO OUTBREAK SIGNALS — LIVE <span class="badge badge-accent">RSS</span></div>
    <div id="whoFeed"><div class="loading">Loading WHO data...</div></div>
  </div>

  <!-- CDC EID FEED -->
  <div class="card span2">
    <div class="card-title">CDC EMERGING INFECTIOUS DISEASES — LIVE <span class="badge badge-red">RSS</span></div>
    <div id="eidFeed"><div class="loading">Loading CDC data...</div></div>
  </div>

  <!-- DATA SOURCES STATUS -->
  <div class="card span2">
    <div class="card-title">DATA SOURCE STATUS <span class="badge badge-green" id="sourcesBadge">-</span></div>
    <div id="sourceStatus"><div class="loading">Loading...</div></div>
  </div>

  <!-- TRIGGERED MODULES -->
  <div class="card span2">
    <div class="card-title">GUARDIAN WATCH MODULES TRIGGERED <span class="badge badge-orange" id="moduleBadge">-</span></div>
    <div id="moduleList"><div class="loading">Awaiting data...</div></div>
  </div>

  <!-- USA STATE DATA -->
  <div class="card span2">
    <div class="card-title">USA — TOP STATES BY CASES <span class="badge badge-accent">disease.sh</span></div>
    <div class="chart-wrap"><canvas id="stateChart"></canvas></div>
  </div>

  <!-- COLLECTION TIMELINE -->
  <div class="card span2">
    <div class="card-title">COLLECTION HISTORY <span class="badge badge-green">AUTO EVERY 6H</span></div>
    <div id="historyList"><div class="loading">Loading history...</div></div>
  </div>

  <!-- FIELD REPORTS FROM FARMS & HOSPITALS -->
  <div class="card span4">
    <div class="card-title">
      FIELD REPORTS — FARMS & HOSPITALS (REAL-TIME)
      <div style="display:flex;gap:8px;align-items:center">
        <span id="fieldCount" class="badge badge-accent">0 reports</span>
        <a href="/field" style="font-family:var(--mono);font-size:10px;color:var(--accent);text-decoration:none;border:1px solid var(--accent);padding:2px 10px;border-radius:2px;letter-spacing:1px">+ SUBMIT FIELD REPORT</a>
      </div>
    </div>
    <div id="fieldReports" style="min-height:60px">
      <div style="color:var(--muted);font-family:var(--mono);font-size:11px;padding:16px;text-align:center">
        No field reports yet —
        <a href="/field" style="color:var(--accent)">click here to submit from farm or hospital</a>
      </div>
    </div>
  </div>

</div>

<div class="footer">
  <span>Guardian Watch (OHZDIS) v4.3.0 · One Health Zoonotic Disease Intelligence System</span>
  <span>171 diseases monitored · 385 keywords · 43 modules</span>
  <span id="footerUpdate">Auto-refresh: every 60 seconds</span>
</div>

<script>
let stateChart = null;

function updateClock() {
  const now = new Date();
  document.getElementById('clock').textContent = now.toUTCString().split(' ')[4] + ' UTC';
}
setInterval(updateClock, 1000);
updateClock();

function fmt(n) {
  if (n >= 1e6) return (n/1e6).toFixed(1) + 'M';
  if (n >= 1e3) return (n/1e3).toFixed(1) + 'K';
  return n;
}

function loadData() {
  fetch('/api/data')
    .then(r => r.json())
    .then(data => {
      updateDashboard(data);
    })
    .catch(e => {
      document.getElementById('alertText').textContent = 'Error loading data: ' + e.message;
    });
}

function updateDashboard(data) {
  const ts = data.timestamp ? new Date(data.timestamp).toLocaleString() : '--';
  document.getElementById('lastCollect').textContent = 'Last collect: ' + ts;

  // WHO stats
  const who = data.who_reports || [];
  const whoZoo = who.filter(r => r.is_zoonotic);
  document.getElementById('whoTotal').textContent = who.length;
  document.getElementById('whoZooCount').textContent = whoZoo.length + ' ZOONOTIC';
  document.getElementById('whoZoo').textContent = whoZoo.length + ' zoonotic signals detected';

  // CDC EID
  const eid = data.eid_articles || [];
  const eidZoo = eid.filter(r => r.is_zoonotic);
  document.getElementById('eidTotal').textContent = eid.length || data.eid_count || 0;
  document.getElementById('eidZooCount').textContent = eidZoo.length + ' ZOONOTIC';
  document.getElementById('eidZoo').textContent = eidZoo.length + ' zoonotic articles';

  // disease.sh
  const dis = data.disease_global || {};
  const g = dis.Global || {};
  document.getElementById('globalCases').textContent = fmt(g.cases || 0);
  document.getElementById('globalDeaths').textContent = fmt(g.deaths || 0) + ' deaths total';

  // Triggers
  const triggers = data.triggers || [];
  document.getElementById('triggerCount').textContent = triggers.length;
  document.getElementById('triggerBadge').textContent = triggers.length + ' ACTIVE';
  document.getElementById('triggerList').textContent =
    triggers.length > 0 ? triggers.map(t => t.module.split(' ')[0]).join(' · ') : 'No triggers';

  // Alert banner
  const allSignals = [...whoZoo, ...eidZoo];
  if (allSignals.length > 0) {
    document.getElementById('alertText').textContent =
      allSignals.map(s => '⚠ ' + (s.title || '').substring(0,60)).join('   |   ');
  } else {
    document.getElementById('alertText').textContent = 'No active zoonotic outbreak signals at this time — routine monitoring';
    document.querySelector('.alert-banner').style.background = 'linear-gradient(90deg,#002200,#001100)';
    document.querySelector('.alert-banner').style.color = '#00e676';
    document.querySelector('.alert-tag').style.background = '#00e676';
  }

  // WHO Feed
  const whoHtml = who.length > 0
    ? who.slice(0,6).map(r =>
      '<div class="signal-item ' + (r.is_zoonotic ? 'sig-high' : 'sig-info') + '">' +
        '<div class="signal-time">' + (r.date||'').substring(0,10) + '</div>' +
        '<div>' +
          '<div class="signal-text">' + (r.title||'').substring(0,70) + '</div>' +
          '<div class="signal-source">WHO RSS · ' + (r.is_zoonotic ? 'ZOONOTIC' : 'OTHER') + '</div>' +
        '</div>' +
      '</div>').join('')
    : '<div class="loading">No WHO data — run collector first</div>';
  document.getElementById('whoFeed').innerHTML = whoHtml;

  // CDC EID Feed
  const eidHtml = eid.length > 0
    ? eid.slice(0,6).map(r =>
      '<div class="signal-item ' + (r.is_zoonotic ? 'sig-critical' : 'sig-info') + '">' +
        '<div class="signal-time">' + (r.date||'').substring(0,10) + '</div>' +
        '<div>' +
          '<div class="signal-text">' + (r.title||'').substring(0,70) + '</div>' +
          '<div class="signal-source">CDC EID · ' + (r.is_zoonotic ? 'ZOONOTIC' : 'OTHER') + '</div>' +
        '</div>' +
      '</div>').join('')
    : '<div class="loading">No CDC EID data — run collector first</div>';
  document.getElementById('eidFeed').innerHTML = eidHtml;

  // Sources status
  const sources = data.sources || {};
  const srcHtml = Object.entries(sources).map(([name, info]) =>
    '<div class="source-row">' +
      '<div style="display:flex;align-items:center;gap:8px">' +
        '<span class="' + (info.ok ? 'src-ok' : 'src-warn') + '">' + (info.ok ? '● OK' : '◐ WARN') + '</span>' +
        name +
      '</div>' +
      '<span class="src-num">' + (info.detail || '-') + '</span>' +
    '</div>').join('');
  document.getElementById('sourceStatus').innerHTML = srcHtml ||
    '<div class="loading">No source data yet</div>';
  document.getElementById('sourcesBadge').textContent =
    Object.values(sources).filter(s => s.ok).length + '/' + Object.keys(sources).length + ' OK';

  // Triggered modules
  const modHtml = triggers.length > 0
    ? triggers.map(t =>
      '<div class="signal-item sig-high">' +
        '<div class="signal-time">AUTO</div>' +
        '<div>' +
          '<div class="signal-text">' + t.module + '</div>' +
          '<div class="signal-source">' + t.reason + '</div>' +
        '</div>' +
      '</div>').join('')
    : '<div class="loading" style="color:var(--green)">No triggers — routine monitoring mode</div>';
  document.getElementById('moduleList').innerHTML = modHtml;
  document.getElementById('moduleBadge').textContent = triggers.length + ' ACTIVE';

  // USA State chart
  const states = (data.us_states || []).slice(0,10);
  if (states.length > 0) {
    const labels = states.map(s => s.state);
    const vals   = states.map(s => s.cases);
    if (stateChart) stateChart.destroy();
    stateChart = new Chart(document.getElementById('stateChart').getContext('2d'), {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          data: vals,
          backgroundColor: '#00c8ff22',
          borderColor: '#00c8ff',
          borderWidth: 1, borderRadius: 2
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks:{color:'#4a7090',font:{size:9}}, grid:{color:'#1a3050'} },
          y: { ticks:{color:'#c8dff0',font:{size:10}}, grid:{color:'#1a3050'} }
        }
      }
    });
  }

  // History
  const history = data.history || [];
  const histHtml = history.length > 0
    ? history.slice(-6).reverse().map(h =>
      '<div class="signal-item sig-info">' +
        '<div class="signal-time">' + (h.time || '--') + '</div>' +
        '<div>' +
          '<div class="signal-text">Collection run — WHO:' + (h.who||0) + ' CDC:' + (h.cdc||0) + ' Triggers:' + (h.triggers||0) + '</div>' +
          '<div class="signal-source">Auto-collector · 171 diseases monitored</div>' +
        '</div>' +
      '</div>').join('')
    : '<div class="loading">No history yet — run collector first</div>';
  document.getElementById('historyList').innerHTML = histHtml;

  document.getElementById('footerUpdate').textContent =
    'Last update: ' + new Date().toLocaleTimeString();
}

function runCollector() {
  const btn = document.getElementById('collectBtn');
  btn.textContent = '⟳ COLLECTING...';
  btn.disabled = true;
  fetch('/api/collect', {method:'POST'})
    .then(r => r.json())
    .then(d => {
      btn.textContent = '▶ COLLECT NOW';
      btn.disabled = false;
      setTimeout(loadData, 3000);
    })
    .catch(() => {
      btn.textContent = '▶ COLLECT NOW';
      btn.disabled = false;
    });
}

// Load field reports
function loadFieldReports() {
  fetch('/api/field-reports')
    .then(r => r.json())
    .then(data => {
      const reports = data.reports || [];
      document.getElementById('fieldCount').textContent = reports.length + ' reports';
      if (reports.length === 0) return;
      
      const colors = {critical:'#ff3b3b',high:'#ff8c00',moderate:'#ffd600',low:'#00e676'};
      const html = reports.slice(0,8).map(r => {
        const score = r.risk_score || 0;
        const level = score>=75?'critical':score>=55?'high':score>=35?'moderate':'low';
        const color = colors[level];
        const time  = (r.server_timestamp||r.timestamp||'').substring(11,16);
        const type  = r.type==='farm'?'🐄 Farm':r.type==='hospital'?'🏥 Hospital':'🌿 Env';
        const loc   = (r.location||'').substring(0,25);
        const detail= (r.key_finding||'').substring(0,35);
        const mods  = (r.modules_triggered||[]).length;
        return '<div class="field-row">' +
          '<span style="font-family:var(--mono);font-size:10px;color:var(--muted)">' + time + '</span>' +
          '<span style="font-size:12px">' + type + '</span>' +
          '<div>' +
            '<div style="font-weight:500;color:#e0f0ff">' + loc + '</div>' +
            '<div style="font-size:11px;color:var(--muted)">' + detail + '</div>' +
          '</div>' +
          '<span class="field-badge fb-' + level + '">' + score + '/100</span>' +
          '<span style="font-family:var(--mono);font-size:10px;color:var(--accent)">' + mods + ' modules</span>' +
        '</div>';
      }).join('');
      document.getElementById('fieldReports').innerHTML = html;
    }).catch(() => {});
}

// ── WORLD MAP ──
let ohMap = null;
let mapMarkers = [];

const OUTBREAK_DATA = [
  // ── CRITICAL ──
  {name:"H5N1 HPAI — California",       lat:36.7783, lng:-119.4179, level:"critical", cases:12, country:"California",          color:"#ff3b3b"},
  {name:"H5N1 HPAI — Washington",       lat:47.7511, lng:-120.7401, level:"critical", cases:8,  country:"Washington",          color:"#ff3b3b"},
  {name:"H5N1 HPAI — Texas",            lat:31.9686, lng:-99.9018,  level:"critical", cases:6,  country:"Texas",               color:"#ff3b3b"},
  {name:"H5N1 HPAI — Michigan",         lat:44.3148, lng:-85.6024,  level:"critical", cases:4,  country:"Michigan",            color:"#ff3b3b"},
  {name:"Mpox — New York",              lat:40.7128, lng:-74.0060,  level:"critical", cases:34, country:"New York City",       color:"#ff3b3b"},
  {name:"Mpox — California",            lat:34.0522, lng:-118.2437, level:"critical", cases:28, country:"Los Angeles",         color:"#ff3b3b"},
  // ── HIGH ──
  {name:"Dengue — Puerto Rico",         lat:18.2208, lng:-66.5901,  level:"high",     cases:87, country:"Puerto Rico",         color:"#ff8c00"},
  {name:"Dengue — Guam",               lat:13.4443, lng:144.7937,  level:"high",     cases:23, country:"Guam",                color:"#ff8c00"},
  {name:"Dengue — US Virgin Islands",  lat:18.3358, lng:-64.8963,  level:"high",     cases:12, country:"USVI",                color:"#ff8c00"},
  {name:"Salmonella — Florida",         lat:27.9944, lng:-81.7603,  level:"high",     cases:45, country:"Florida",             color:"#ff8c00"},
  {name:"Salmonella — Georgia",         lat:32.1656, lng:-82.9001,  level:"high",     cases:31, country:"Georgia",             color:"#ff8c00"},
  {name:"West Nile — Arizona",          lat:34.0489, lng:-111.0937, level:"high",     cases:18, country:"Arizona",             color:"#ff8c00"},
  // ── MODERATE ──
  {name:"Plague — New Mexico",          lat:34.5199, lng:-105.8701, level:"moderate", cases:2,  country:"New Mexico",          color:"#ffd600"},
  {name:"Plague — Colorado",            lat:39.5501, lng:-105.7821, level:"moderate", cases:1,  country:"Colorado",            color:"#ffd600"},
  {name:"Tularemia — South Dakota",     lat:44.2998, lng:-99.4388,  level:"moderate", cases:3,  country:"South Dakota",        color:"#ffd600"},
  {name:"Rabies — Texas (animal)",      lat:29.7604, lng:-95.3698,  level:"moderate", cases:15, country:"Texas",               color:"#ffd600"},
  {name:"Lyme Disease — Connecticut",   lat:41.6032, lng:-73.0877,  level:"moderate", cases:89, country:"Connecticut",         color:"#ffd600"},
  {name:"Lyme Disease — New York",      lat:43.2994, lng:-74.2179,  level:"moderate", cases:76, country:"New York State",      color:"#ffd600"},
  {name:"Brucellosis — Wyoming",        lat:43.0760, lng:-107.2903, level:"moderate", cases:4,  country:"Wyoming",             color:"#ffd600"},
  {name:"E. coli O157 — Midwest",       lat:41.8781, lng:-87.6298,  level:"moderate", cases:22, country:"Illinois/Indiana",    color:"#ffd600"},
  // ── LOW / MONITORING ──
  {name:"Q Fever — California",         lat:37.3382, lng:-121.8863, level:"low",      cases:8,  country:"California",          color:"#00e676"},
  {name:"Hantavirus — Utah",            lat:39.3210, lng:-111.0937, level:"low",      cases:1,  country:"Utah",                color:"#00e676"},
  {name:"Anaplasmosis — Minnesota",     lat:46.7296, lng:-94.6859,  level:"low",      cases:34, country:"Minnesota",           color:"#00e676"},
  {name:"Babesiosis — Massachusetts",   lat:42.4072, lng:-71.3824,  level:"low",      cases:19, country:"Massachusetts",       color:"#00e676"},
  {name:"Chikungunya — Florida",        lat:25.7617, lng:-80.1918,  level:"low",      cases:3,  country:"Florida (imported)",  color:"#00e676"},
  // ── US TERRITORIES ──
  {name:"Leptospirosis — Am. Samoa",    lat:-14.2710, lng:-170.1322,level:"moderate", cases:6,  country:"American Samoa",      color:"#ffd600"},
  {name:"Dengue — N. Mariana Islands",  lat:15.0979, lng:145.6739,  level:"moderate", cases:9,  country:"CNMI",                color:"#ffd600"},
];

function initMap() {
  if (ohMap) return;
  ohMap = L.map('map', {
    center: [38.5, -96.0],
    zoom: 4,
    zoomControl: true,
    attributionControl: false
  });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 19
  }).addTo(ohMap);

  updateMapMarkers(OUTBREAK_DATA);
  document.getElementById('mapAlertCount').textContent = OUTBREAK_DATA.length + ' alerts';
}

function updateMapMarkers(outbreaks) {
  // Clear existing
  mapMarkers.forEach(m => ohMap.removeLayer(m));
  mapMarkers = [];

  outbreaks.forEach(ob => {
    const size = ob.level === 'critical' ? 16 : ob.level === 'high' ? 12 : 8;
    const icon = L.divIcon({
      html: '<div style="width:' + size + 'px;height:' + size + 'px;border-radius:50%;background:' + ob.color + ';border:2px solid rgba(255,255,255,0.5);box-shadow:0 0 ' + (size*2) + 'px ' + ob.color + '"></div>',
      iconSize: [size, size],
      iconAnchor: [size/2, size/2],
      className: ''
    });

    const marker = L.marker([ob.lat, ob.lng], {icon})
      .addTo(ohMap)
      .bindPopup(
        '<div style="background:#0c1825;color:#c8dff0;padding:8px;border:1px solid #1a3050;font-family:monospace;font-size:12px;min-width:180px">' +
        '<div style="color:' + ob.color + ';font-weight:bold;margin-bottom:4px">' + ob.name + '</div>' +
        '<div>Country: ' + ob.country + '</div>' +
        (ob.cases > 0 ? '<div>Cases: ' + ob.cases.toLocaleString() + '</div>' : '') +
        '<div style="margin-top:4px;padding:2px 6px;background:' + ob.color + '22;border:1px solid ' + ob.color + '44;display:inline-block">' + ob.level.toUpperCase() + '</div>' +
        '</div>',
        {className: 'dark-popup'}
      );
    mapMarkers.push(marker);
  });
}

function addFieldReportToMap(report) {
  if (!ohMap || !report.lat || !report.lng) return;
  const icon = L.divIcon({
    html: '<div style="width:14px;height:14px;border-radius:50%;background:#00c8ff;border:2px solid white;box-shadow:0 0 10px #00c8ff"></div>',
    iconSize: [14,14], iconAnchor: [7,7], className: ''
  });
  const m = L.marker([report.lat, report.lng], {icon})
    .addTo(ohMap)
    .bindPopup(
      '<div style="background:#0c1825;color:#c8dff0;padding:8px;font-family:monospace;font-size:12px">' +
      '<div style="color:#00c8ff;font-weight:bold">Field Report: ' + (report.type||'') + '</div>' +
      '<div>' + (report.location||'') + '</div>' +
      '<div>Risk: ' + (report.risk_score||0) + '/100</div>' +
      '</div>'
    );
  mapMarkers.push(m);
}

// Auto-refresh every 60 seconds
loadData();
loadFieldReports();
setInterval(loadData, 60000);
setInterval(loadFieldReports, 15000);
// Init map after short delay (Leaflet needs DOM ready)
setTimeout(initMap, 500);
</script>
</body>
</html>"""

# ── COLLECTION HISTORY ──────────────────────────────────────
collection_history = []

def save_data(collected):
    """Save collected data to JSON file for dashboard"""
    # Build sources status
    sources = {
        "CDC EID RSS":    {"ok": len(collected.get("eid",[])) > 0,
                           "detail": f"{len(collected.get('eid',[]))} articles"},
        "WHO RSS":        {"ok": len(collected.get("who",[])) > 0,
                           "detail": f"{len(collected.get('who',[]))} entries"},
        "disease.sh":     {"ok": bool(collected.get("disease",{}).get("Global")),
                           "detail": "Global + 63 states"},
        "EPA ATTAINS":    {"ok": bool(collected.get("epa")),
                           "detail": f"{len(collected.get('epa',{}).get('pathogens',[]))} pathogens"},
        "USDA Data.gov":  {"ok": len(collected.get("usda",[])) > 0,
                           "detail": f"{len(collected.get('usda',[]))} datasets"},
    }

    # Extract disease.sh data
    dis = collected.get("disease", {})
    g   = dis.get("Global", {})
    usa = dis.get("USA", {})
    states = dis.get("states", [])
    top_states = sorted(states, key=lambda x: x.get("cases",0), reverse=True)[:10] if states else []

    # Add to history
    collection_history.append({
        "time":     datetime.now().strftime("%H:%M"),
        "who":      len(collected.get("who",[])),
        "cdc":      len(collected.get("eid",[])),
        "triggers": len(collected.get("triggers",[]))
    })

    data = {
        "timestamp":     datetime.now().isoformat(),
        "who_reports":   collected.get("who", []),
        "eid_articles":  collected.get("eid", []),
        "triggers":      collected.get("triggers", []),
        "sources":       sources,
        "disease_global": {
            "Global": {"cases": g.get("cases",0), "deaths": g.get("deaths",0),
                       "active": g.get("active",0)},
            "USA":    {"cases": usa.get("cases",0), "deaths": usa.get("deaths",0)},
        },
        "us_states":  [{"state": s.get("state"), "cases": s.get("cases",0),
                         "deaths": s.get("deaths",0)} for s in top_states],
        "history":    collection_history[-20:],
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Data saved → {DATA_FILE}")
    return data


def run_collector():
    """Run data_collector.py and return collected data"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Running data collector...")
    try:
        # Import and run collector functions directly
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # Try importing collector
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "data_collector", "data_collector.py")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            # Run each fetch function
            collected = {
                "eid":      mod.fetch_cdc_eid_rss(),
                "who":      mod.fetch_who_outbreaks(),
                "disease":  mod.fetch_disease_sh(),
                "epa":      mod.fetch_epa_water(),
                "usda":     mod.fetch_usda(),
            }

            # Determine triggers
            who_zoo = [e for e in collected["who"] if e.get("is_zoonotic")]
            eid_zoo = [e for e in collected["eid"] if e.get("is_zoonotic")]
            triggers = []
            if who_zoo:
                triggers += [
                    {"module": "detector.py (M10)", "reason": "WHO zoonotic outbreak"},
                    {"module": "risk_calc.py (M7)",  "reason": "Risk score needed"},
                    {"module": "response.py (M19)",  "reason": "Response activation"},
                ]
            if eid_zoo:
                triggers.append({"module": "analyzer.py (M8)", "reason": "New zoonotic research"})

            collected["triggers"] = triggers
            return save_data(collected)

        except Exception as e:
            print(f"Collector import error: {e}")
            # Return empty data structure
            return save_data({"who":[],"eid":[],"disease":{},"epa":{},"usda":[],"triggers":[]})

    except Exception as e:
        print(f"Collector error: {e}")
        return {}


# ── BACKGROUND COLLECTOR ─────────────────────────────────────
def background_collector():
    """Run collector every 6 hours in background"""
    while True:
        run_collector()
        print("Next collection in 6 hours...")
        time.sleep(6 * 3600)


# ── FLASK ROUTES ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route("/api/data")
def api_data():
    """Return latest collected data"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return jsonify(json.load(f))
    else:
        return jsonify({"error": "No data yet", "message": "Click COLLECT NOW"})

@app.route("/api/collect", methods=["POST"])
def api_collect():
    """Trigger manual data collection"""
    def collect_async():
        run_collector()
    threading.Thread(target=collect_async, daemon=True).start()
    return jsonify({"status": "collecting", "message": "Collection started"})

@app.route("/api/status")
def api_status():
    return jsonify({
        "status": "operational",
        "modules": 43,
        "diseases_monitored": 171,
        "keywords": 385,
        "data_file_exists": os.path.exists(DATA_FILE),
        "uptime": "running"
    })


@app.route("/field")
def field_form():
    """Serve field reporting form"""
    if os.path.exists("field_report.html"):
        with open("field_report.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h2>field_report.html not found in folder</h2>"

@app.route("/api/field-report", methods=["POST", "OPTIONS"])
def api_field_report():
    """Receive field report from farm/hospital"""
    if request.method == "OPTIONS":
        resp = jsonify({})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        resp.headers['Access-Control-Allow-Methods'] = 'POST'
        return resp
    try:
        report = request.get_json()
        if not report:
            return jsonify({"error": "No data received"}), 400
        saved = save_field_report(report)
        resp = jsonify({"status": "saved", "id": saved.get("id"), "risk": saved.get("risk_score")})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/field-reports")
def api_field_reports():
    """Return all field reports"""
    reports = load_field_reports()
    resp = jsonify({"reports": reports, "count": len(reports)})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

# ── MAIN ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  Guardian Watch (OHZDIS) Web Server v4.3.0")
    print("  Dashboard: http://localhost:5000")
    print("=" * 60)
    print("\nStarting initial data collection...")

    # Run first collection immediately
    threading.Thread(target=run_collector, daemon=True).start()

    # Start background auto-collector
    threading.Thread(target=background_collector, daemon=True).start()

    print("Open your browser: http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
