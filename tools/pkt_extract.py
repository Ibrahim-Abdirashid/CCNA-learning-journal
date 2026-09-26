"""
pkt_extract.py - Extract topology, IP addressing and device configs from Packet Tracer files.

Usage:
  python pkt_extract.py <file.pkt> <out_dir>

Writes into <out_dir>:
  topology.svg         - auto-drawn logical topology
  summary.json         - devices, IPs, links (machine readable)
  configs/<Device>.txt - running-config of every IOS device (router / switch)
"""
import sys, os, re, json, html
import xml.etree.ElementTree as ET
from pkt2xml import decrypt

SKIP_TYPES = {'PowerDistributionDevice', 'Power Distribution Device', 'Sniffer'}


def load(path):
    with open(path, 'rb') as f:
        return ET.fromstring(decrypt(f.read()))


def first(el, tag, default=''):
    x = el.find(tag)
    return (x.text or '').strip() if x is not None and x.text else default


def parse_config(lines):
    """Return hostname and list of (interface, ip, mask) from a running-config."""
    ifaces, cur, hostname = [], None, None
    for ln in lines:
        s = ln.rstrip()
        if s.startswith('hostname '):
            hostname = s.split(None, 1)[1]
        m = re.match(r'^interface (\S+)', s)
        if m:
            cur = m.group(1)
            continue
        if cur and s.startswith(' ip address '):
            parts = s.split()
            if len(parts) >= 4 and parts[2] != 'dhcp':
                ifaces.append((cur, parts[2], parts[3]))
            elif len(parts) >= 3 and parts[2] == 'dhcp':
                ifaces.append((cur, 'dhcp', ''))
        elif cur and s.startswith(' ipv6 address ') and 'link-local' not in s:
            ifaces.append((cur, s.split()[2], 'ipv6'))
        if s and not s.startswith(' '):
            cur = None
    return hostname, ifaces


HIGHLIGHT_RE = re.compile(r'^(hostname |enable |username |ip domain|crypto key|line (vty|con)|transport input|login|password|banner|vtp |vlan \d|name |interface|switchport|channel-group|encapsulation|no shutdown|shutdown| ip address| ipv6 address|ip route|ipv6 route|ipv6 unicast|router |network |passive|default-information|ip nat|access-list|ip dhcp|ip helper|spanning-tree|cdp |lldp |ip default-gateway|service password|no ip domain|ip ssh|exec-timeout|logging sync|description)', re.I)

def highlights(cfg):
    out, cur_if, if_lines = [], None, []
    def flush():
        nonlocal cur_if, if_lines
        if cur_if and if_lines:
            out.append(cur_if); out.extend(if_lines)
        cur_if, if_lines = None, []
    for ln in cfg:
        s = ln.rstrip()
        if not s or s == '!':
            continue
        if s.startswith('interface '):
            flush(); cur_if = s; continue
        if cur_if is not None:
            if s.startswith(' '):
                if re.match(r'^ (ip address|ipv6 address|switchport|channel-group|encapsulation|no shutdown|description|ip nat|ip helper|ip ospf|ipv6 ospf|spanning-tree|duplex|speed)', s) and 'link-local' not in s:
                    if_lines.append(s)
                continue
            flush()
        if s.startswith(' ') or HIGHLIGHT_RE.match(s):
            if re.match(r'^(version|no service|service timestamps|boot-|license|ip cef|ipv6 cef|end$|spanning-tree extend|spanning-tree mode pvst)', s):
                continue
            out.append(s)
    flush()
    return out

def extract(path):
    root = load(path)
    devices, byref = [], {}
    for dev in root.iter('DEVICE'):
        eng = dev.find('ENGINE')
        if eng is None:
            continue
        t = eng.find('TYPE')
        dtype = (t.text or '').strip() if t is not None else ''
        model = t.get('model', '') if t is not None else ''
        name = first(eng, 'NAME')
        if dtype in SKIP_TYPES or not name:
            continue
        ref = first(eng, 'SAVE_REF_ID')
        x = y = None
        ws = dev.find('WORKSPACE/LOGICAL')
        if ws is not None:
            xs, ys = ws.find('X'), ws.find('Y')
            if xs is not None and ys is not None:
                x, y = float(xs.text), float(ys.text)
        cfg_el = eng.find('RUNNINGCONFIG')
        cfg = [(l.text or '') for l in cfg_el.findall('LINE')] if cfg_el is not None else []
        hostname, ifaces = parse_config(cfg) if cfg else (None, [])
        host_ips = []
        if not cfg:
            for port in eng.iter('PORT'):
                ip = first(port, 'IP')
                if ip and ip != '0.0.0.0':
                    host_ips.append((ip, first(port, 'SUBNET'),
                                     first(port, 'PORT_GATEWAY') or first(eng, 'GATEWAY')))
                elif first(port, 'PORT_DHCP_ENABLE') == 'true':
                    host_ips.append(('dhcp', '', ''))
        vlans, vtp = [], None
        vl = eng.find('.//VLANS')
        if vl is not None:
            vlans = [dict(id=int(v.get('number')), name=v.get('name')) for v in vl.findall('VLAN')
                     if int(v.get('number')) not in (1, 1002, 1003, 1004, 1005)]
        vt = eng.find('.//VTP')
        if vt is not None:
            mode = {'0': 'server', '1': 'client', '2': 'transparent', '3': 'off'}.get(first(vt, 'MODE'), first(vt, 'MODE'))
            vtp = dict(domain=first(vt, 'DOMAIN_NAME'), mode=mode, version=first(vt, 'VERSION'),
                       password=first(vt, 'PASSWORD'), revision=first(vt, 'CONFIG_REVISION'))
        d = dict(name=name, hostname=hostname or name, type=dtype, model=model, ref=ref, vlans=vlans, vtp=vtp,
                 x=x, y=y,
                 interfaces=[dict(iface=i, ip=a, mask=m) for i, a, m in ifaces],
                 host_ips=[dict(ip=a, mask=m, gateway=g) for a, m, g in host_ips],
                 has_config=bool(cfg))
        d['_cfg'] = cfg
        d['highlights'] = highlights(cfg) if cfg else []
        devices.append(d)
        byref[ref] = d
    links = []
    for link in root.iter('LINK'):
        cab = link.find('CABLE')
        if cab is None:
            continue
        ports = cab.findall('PORT')
        fr, to = first(cab, 'FROM'), first(cab, 'TO')
        if fr in byref and to in byref and len(ports) >= 2:
            links.append(dict(a=byref[fr]['name'], a_port=ports[0].text or '',
                              b=byref[to]['name'], b_port=ports[1].text or '',
                              type=first(link, 'TYPE')))
    return devices, links


def short_port(p):
    return (p.replace('GigabitEthernet', 'G').replace('FastEthernet', 'F')
             .replace('Serial', 'S').replace('Ethernet', 'E'))


ICON = {'Router': ('#1f77b4', 'R'), 'Switch': ('#2ca02c', 'SW'), 'MultiLayerSwitch': ('#17becf', 'L3'),
        'Pc': ('#7f7f7f', 'PC'), 'Laptop': ('#7f7f7f', 'LT'), 'Server': ('#d62728', 'SRV'),
        'Printer': ('#9467bd', 'PR'), 'WirelessRouter': ('#ff7f0e', 'WR'), 'AccessPoint': ('#ff7f0e', 'AP'),
        'Cloud': ('#8c564b', 'WAN')}


def draw_svg(devices, links, out):
    pts = [d for d in devices if d['x'] is not None]
    if not pts:
        return
    minx, maxx = min(d['x'] for d in pts), max(d['x'] for d in pts)
    miny, maxy = min(d['y'] for d in pts), max(d['y'] for d in pts)
    pad = 90
    W = max(520, int(maxx - minx) + 2 * pad)
    H = max(300, int(maxy - miny) + 2 * pad + 40)

    def P(d):
        return d['x'] - minx + pad, d['y'] - miny + pad

    pos = {d['name']: P(d) for d in pts}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Segoe UI, Arial, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    for l in links:
        if l['a'] in pos and l['b'] in pos:
            (x1, y1), (x2, y2) = pos[l['a']], pos[l['b']]
            dash = ' stroke-dasharray="6 4"' if 'Serial' in l['a_port'] else ''
            o.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                     f'stroke="#555" stroke-width="2"{dash}/>')
            for (x, y, xo, yo, p) in ((x1, y1, x2, y2, l['a_port']), (x2, y2, x1, y1, l['b_port'])):
                tx = x + (xo - x) * 0.22
                ty = y + (yo - y) * 0.22
                lab = html.escape(short_port(p))
                w = len(lab) * 7.2 + 6
                o.append(f'<rect x="{tx - w / 2:.0f}" y="{ty - 8:.0f}" width="{w:.0f}" height="15" rx="3" '
                         f'fill="#fff8dc" stroke="#ccc"/>')
                o.append(f'<text x="{tx:.0f}" y="{ty + 3:.0f}" font-size="10" text-anchor="middle" '
                         f'fill="#333">{lab}</text>')
    for d in pts:
        x, y = pos[d['name']]
        color, tag = ICON.get(d['type'], ('#999', d['type'][:3]))
        if d['type'] in ('Router', 'WirelessRouter'):
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{color}" stroke="#123" stroke-width="1.5"/>')
        elif d['type'] in ('Switch', 'MultiLayerSwitch'):
            o.append(f'<rect x="{x - 30:.0f}" y="{y - 16:.0f}" width="60" height="32" rx="4" fill="{color}" '
                     f'stroke="#123" stroke-width="1.5"/>')
        else:
            o.append(f'<rect x="{x - 20:.0f}" y="{y - 20:.0f}" width="40" height="40" rx="6" fill="{color}" '
                     f'stroke="#123" stroke-width="1.5"/>')
        o.append(f'<text x="{x:.0f}" y="{y + 4:.0f}" font-size="11" font-weight="bold" text-anchor="middle" '
                 f'fill="#fff">{tag}</text>')
        label = d['name']
        o.append(f'<text x="{x:.0f}" y="{y + 38:.0f}" font-size="12" font-weight="600" text-anchor="middle" '
                 f'fill="#111">{html.escape(label)}</text>')
        ips = [i['ip'] for i in d['interfaces'] if i['mask'] != 'ipv6'] + [h['ip'] for h in d['host_ips']]
        if ips:
            o.append(f'<text x="{x:.0f}" y="{y + 52:.0f}" font-size="10" text-anchor="middle" fill="#444">'
                     f'{html.escape(", ".join(ips[:3]))}</text>')
    o.append('</svg>')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(o))


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(os.path.join(out, 'configs'), exist_ok=True)
    devices, links = extract(src)
    for d in devices:
        if d['has_config']:
            safe = re.sub(r'[^A-Za-z0-9_-]+', '_', d['hostname'])
            with open(os.path.join(out, 'configs', safe + '.txt'), 'w', encoding='utf-8') as f:
                f.write('\n'.join(d['_cfg']) + '\n')
    draw_svg(devices, links, os.path.join(out, 'topology.svg'))
    for d in devices:
        d.pop('_cfg', None)
    with open(os.path.join(out, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(dict(source=os.path.basename(src), devices=devices, links=links), f, indent=1,
                  ensure_ascii=False)
    print(f"{os.path.basename(src)}: {len(devices)} devices, {len(links)} links")


if __name__ == '__main__':
    main()
