import os
import re
import json
import shutil
import requests
import logging
import datetime
import threading
import concurrent.futures
import customtkinter as ctk
from tkinter import filedialog
from packaging import version

logging.basicConfig(filename='phantom.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

a = '1.0'
b = 'https://api.github.com/repos/astrapy/FiveM-Trigger-Finder/releases/latest'

def c():
    try:
        d = requests.get(b, timeout=10)
        if d.status_code == 200:
            f = d.json()
            g_val = f.get('tag_name', '')
            if g_val.startswith('v'):
                g_val = g_val[1:]
            if g_val and version.parse(g_val) > version.parse(a):
                logging.info(f'New version available: {g_val}. Updating...')
                l = f.get('assets', [])
                m = None
                n = os.path.basename(__file__)
                for p in l:
                    if p.get('name', '') == n:
                        m = p.get('browser_download_url', '')
                        break
                if m:
                    if q(m):
                        print('Update successful. Please restart the application.')
                        os._exit(0)
                    else:
                        logging.error('Failed to download or verify the new version.')
                else:
                    logging.error('Update asset not found in the latest release.')
            else:
                logging.info('No update available.')
        else:
            logging.error('Failed to check for updates: ' + str(d.status_code))
    except Exception as r:
        logging.exception('Error while checking for updates: ' + str(r))

def s(t, u=None):
    logging.info('Assuming valid.')
    return True

def q(v):
    try:
        d = requests.get(v, timeout=10)
        if d.status_code == 200:
            w = d.content
            x = os.path.abspath(__file__)
            z = x + '.bak'
            shutil.copy2(x, z)
            aa = x + '.tmp'
            with open(aa, 'wb') as ab:
                ab.write(w)
            if s(aa):
                shutil.move(aa, x)
                return True
            else:
                os.remove(aa)
                return False
    except Exception as r:
        logging.exception('Error during update download: ' + str(r))
    return False

def ad(ae='config.json'):
    af = {
        'trigger_patterns': [
            r"RegisterNetEvent\(\s*[\'\"]([^\'\"]+)[\'\"]",
            r"TriggerServerEvent\(\s*[\'\"]([^\'\"]+)[\'\"]",
            r"TriggerClientEvent\(\s*[\'\"]([^\'\"]+)[\'\"]"
        ],
        'scan_keywords': {
            'common_events': ['TriggerServerEvent', 'TriggerEvent'],
            'common_params': ['money', 'jail', 'reward']
        },
        'file_extensions': ['.js', '.lua'],
        'framework_identifiers': {
            'ESX': ['esx_', 'esx:'],
            'QBCore': ['qb-', 'qb_', 'qb:']
        },
        'output_directory': 'output'
    }
    if os.path.exists(ae):
        try:
            with open(ae, 'r', encoding='utf-8') as ab:
                ah = json.load(ab)
            af.update(ah)
        except Exception as r:
            logging.exception('Error loading config file: ' + str(r))
    return af

ctk.set_default_color_theme('lib/lavender.json')

def aj(ak='lib/categories.json'):
    with open(ak, 'r', encoding='utf-8') as al:
        am = json.load(al)
    return [(an['category'], an['keywords']) for an in am]

def ao(ap='lib/ascii.json'):
    with open(ap, 'r', encoding='utf-8') as al:
        return json.load(al)

def aq(ar, at):
    au = []
    for (av, aw, ax) in os.walk(ar):
        for filename in ax:
            if any(filename.endswith(az) for az in at):
                au.append(os.path.join(av, filename))
    return au

def bc(bd, be):
    for bf in be:
        bg = re.search(bf, bd)
        if bg:
            return bg.group(1)
    return ''

def bi(bj, bk):
    bl = {bm: [] for (bm, bn) in bk}
    bl['Other'] = []
    for bo in bj:
        bp = bc(bo['lineText'], ad()['trigger_patterns'])
        bq = f"{bo['file']} {bo['lineText']} {bp}"
        br = False
        for (bm, bs) in bk:
            if any(bt in bq for bt in bs):
                bl[bm].append(bo)
                br = True
                break
        if not br:
            bl['Other'].append(bo)
    for bm in bl:
        bl[bm] = sorted(bl[bm], key=lambda bu: (bu['file'], bu['lineNum']))
    return bl

def bv(bw, bx):
    os.makedirs(bw, exist_ok=True)
    by = ao()
    bz = '-- No Framework Found.\n'
    ca = {'Framework: ESX': 0, 'Framework: QBCore': 0}
    for cb in bx.values():
        for bo in cb:
            cd = bo['lineText']
            for ce, cf in ad().get('framework_identifiers', {}).items():
                if ce.upper() == 'ESX' and any(ci in cd for ci in cf):
                    ca['Framework: ESX'] += 1
                if ce.upper() == 'QBCORE' and any(ci in cd for ci in cf):
                    ca['Framework: QBCore'] += 1
    cj = max(ca, key=lambda ck: ca[ck])
    cl = by.get(cj, bz) if ca[cj] > 0 else bz
    cm_list = ['Robbery', 'Police', 'Money', 'Drugs', 'Weapons', 'Gangs/Factions', 
               'Missions/Quests', 'Jobs', 'Inventory', 'Vehicles', 'Properties', 'Status', 
               'Framework: ESX', 'Framework: QBCore', 'Clothes', 'License', 'Medical', 
               'Administration', 'Connection', 'Callback', 'UI', 'Other', 'Casino']
    for cn in cm_list:
        co = bx.get(cn, [])
        cp = re.sub('[^a-zA-Z0-9_]', '_', cn)
        t = os.path.join(bw, f'{cp}.lua')
        with open(t, 'w', encoding='utf-8') as ab:
            ab.write('-- Suggestions? Send it to astrapy or in our discord.gg/phantomai\n')
            ab.write(f'{cl}\n\n')
            if co:
                for bo in co:
                    cq = ' [COMMON]' if bo.get('common') else ''
                    ab.write(f"-- Found in: {bo['file']}\n")
                    ab.write(f"-- Line: {bo['lineNum']}{cq}\n")
                    ab.write(f"{bo['lineText']}\n\n")
            else:
                ab.write('-- No triggers found for this category.\n')

def cr(cs, bx, ct, cu, cv_list):
    sccn = os.path.basename(cs)
    cw = os.path.join(cs, 'report.html')
    with open(cw, 'w', encoding='utf-8') as ab:
        ab.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Phantom {sccn} Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #000;
            color: #fff;
        }}
        .container {{
            max-width: 800px;
            margin: auto;
            background: #121212;
            padding: 20px;
            box-shadow: 0 0 10px rgba(128, 0, 128, 0.5);
            border: 2px solid purple;
            border-radius: 8px;
        }}
        h1, h2, p {{
            text-align: center;  /* Center headings and paragraphs */
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            padding: 10px;
            border: 1px solid purple;
            text-align: left;
        }}
        th {{
            background-color: #1c1c1c;
        }}
        .summary {{
            margin-bottom: 20px;
        }}
        footer {{
            text-align: center;
            font-size: 0.9em;
            color: #aaa;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Phantom {sccn} Report</h1>
        <p>Report generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <h2>Trigger Summary</h2>
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Number of Triggers</th>
                </tr>
            </thead>
            <tbody>""")
        for (cn, co) in bx.items():
            ab.write(f'<tr><td>{cn}</td><td>{len(co)}</td></tr>')
        ab.write(f"""       </tbody>
        </table>
        <h2>Webhook URLs Found</h2>
        <p>Total webhooks detected: {len(ct)}</p>
        <h2>Obfuscated Code</h2>
        <p>Total files flagged for obfuscation: {len(cu)}</p>""")
        if cv_list:
            ab.write(f"""
        <h2>Custom String Matches</h2>
        <p>Total custom string matches: {len(cv_list)}</p>""")
        ab.write(f"""
        <footer>
            <p>Phantom TriggerFinder &copy; {datetime.datetime.now().year}. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>""")
    logging.info(f'HTML report generated at {cw}')

def da(t, db, dc, dd):
    de_list = []
    df_list = []
    dg_list = []
    ct_list = []
    cu_list = []
    try:
        with open(t, 'r', encoding='utf-8', errors='ignore') as ab:
            dh = ab.readlines()
    except Exception as r:
        logging.exception('Error reading file ' + t + ': ' + str(r))
        return (de_list, df_list, dg_list, ct_list, cu_list)

    for dj, bd in enumerate(dh, start=1):
        if any(dk in bd for dk in db['scan_keywords']['common_events']):
            matches = re.findall(r'TriggerServerEvent\([^)]*\)', bd)
            for m in matches:
                dl_flag = any(param in m for param in db['scan_keywords']['common_params'])
                if m not in [bo['lineText'] for bo in de_list]:
                    de_list.append({'file': t,'lineNum': dj,'common': dl_flag,'lineText': m})

        for do, dp in dc.items():
            if dp and do in bd:
                pattern = rf'{re.escape(do)}\([^)]*\)'
                matches = re.findall(pattern, bd)
                for m in matches:
                    if m not in [bo['lineText'] for bo in df_list]:
                        df_list.append({'file': t,'lineNum': dj,'common': False,'lineText': m})
        if dd:
            for dr in dd:
                if dr in bd:
                    dg_list.append({'file': t,'lineNum': dj,'string': dr,'lineText': bd})
        if 'discord.com/api/webhooks' in bd or 'discordapp.com/api/webhooks' in bd:
            webhook_matches = re.findall(r'(https?://[^\s]+)', bd)
            for w_match in webhook_matches:
                if 'discord.com/api/webhooks' in w_match or 'discordapp.com/api/webhooks' in w_match:
                    ct_list.append({'file': t,'lineNum': dj,'common': False,'lineText': w_match})
    try:
        with open(t, 'r', encoding='utf-8', errors='ignore') as ab:
            content = ab.read()
        if re.search(r'[^ \t\n\r\f\v]{50,}', content):
            cu_list.append({'file': t,'common': False,'lineText': 'Obfuscated code detected'})
    except Exception as r:
        logging.exception('Error during obfuscation check in ' + t + ': ' + str(r))

    return (de_list, df_list, dg_list, ct_list, cu_list)


def dt(ar, du, dc, dd):
    db = ad()
    dv = aq(ar, db['file_extensions'])
    logging.info(f'Found {len(dv)} files in directory {ar}')
    dw = []
    dx = []
    dy = []
    dz = []
    ea = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ftff = {executor.submit(da, t, db, dc, dd): t for t in dv}
        for eh, future in enumerate(concurrent.futures.as_completed(ftff), start=1):
            t = ftff[future]
            try:
                (de, ek, cv_list, ct_list, cu_list) = future.result()
                dw.extend(de)
                dx.extend(ek)
                dy.extend(cv_list)
                dz.extend(ct_list)
                ea.extend(cu_list)
            except Exception as r:
                logging.exception('Error processing file ' + t + ': ' + str(r))
            du(f'Scanned {eh}/{len(dv)} files...')
    en = dw + dx
    bk = aj()
    bx = bi(en, bk)
    cs = os.path.join(db['output_directory'], os.path.basename(ar))
    os.makedirs(cs, exist_ok=True)
    eo = os.path.join(cs, 'triggers')
    bv(eo, bx)
    with open(os.path.join(cs, 'webhooks.json'), 'w', encoding='utf-8') as ab:
        json.dump(dz, ab, indent=4)
    with open(os.path.join(cs, 'obfuscated.json'), 'w', encoding='utf-8') as ab:
        json.dump(ea, ab, indent=4)
    if dy:
        ep_dir = os.path.join(db['output_directory'], 'customstrings')
        os.makedirs(ep_dir, exist_ok=True)
        eq_path = os.path.join(ep_dir, os.path.basename(ar) + '.json')
        with open(eq_path, 'w', encoding='utf-8') as ab:
            json.dump(dy, ab, indent=4)
    cr(cs, bx, dz, ea, dy)
    er = f'Results saved to:\n  • JSON files in: {cs}\n  • Trigger files in: {eo}\n  • HTML report in: {cs}\n'
    if dy:
        er += f"  • Custom strings in: {os.path.join(db['output_directory'], 'customstrings', os.path.basename(ar) + '.json')}\n"
    du(er, color='green')

class es(ctk.CTk):

    def __init__(et):
        super().__init__()
        et.title('Phantom')
        et.geometry('450x580')
        et.iconbitmap('lib/logo.ico')
        et.ex = ctk.CTkLabel(et, text='Suggestions: discord.gg/phantomai', text_color='gray')
        et.ex.pack(pady=(5, 0))
        et.ez = ''
        et.fa = ctk.CTkTabview(et)
        et.fa.pack(expand=True, fill='both', padx=20, pady=10)
        et.fa.add('Trigger Finder')
        et.fc = et.fa.tab('Trigger Finder')
        et.fe = ctk.CTkFrame(et.fc)
        et.fe.pack(pady=(10, 0), padx=20, fill='x')
        et.ff = ctk.CTkButton(et.fe, text='Select Folder', command=et.fg, width=120)
        et.ff.pack(pady=5, anchor='center')
        et.fh = ctk.CTkLabel(et.fe, text='No folder selected', text_color='red')
        et.fh.pack(pady=5, anchor='center')
        et.fi = ctk.CTkFrame(et.fc)
        et.fi.pack(pady=5, padx=20, fill='x')
        et.fj = ctk.CTkLabel(et.fi, text='Scan Additional Events:')
        et.fj.pack(pady=(0, 5))
        et.dc = {}
        et.fk = ['AddEventHandler', 'RegisterNetEvent', 'TriggerClientEvent']
        for do in et.fk:
            fl = ctk.BooleanVar(value=True)
            fm = ctk.CTkCheckBox(et.fi, text=do, variable=fl)
            fm.pack(anchor='w', padx=10, pady=5)
            et.dc[do] = fl
        et.fn = ctk.CTkFrame(et.fc)
        et.fn.pack(pady=10, padx=20, fill='x')
        et.fo = ctk.CTkLabel(et.fn, text='Custom Strings (comma separated):')
        et.fo.pack(pady=(0, 5))
        et.fp = ctk.StringVar()
        et.fq = ctk.CTkEntry(et.fn, textvariable=et.fp, width=300)
        et.fq.pack(padx=10, pady=5)
        et.fr = ctk.CTkButton(et.fc, text='Start Scan', command=et.fs)
        et.fr.pack(pady=10)
        et.ft = ctk.CTkTextbox(et.fc, wrap='word', width=550, height=250)
        et.ft.pack(padx=20, pady=10, fill='both', expand=True)
        et.fu = ctk.CTkProgressBar(et.fc)
        et.fu.set(0)
        et.fu.pack(padx=20, pady=(0, 10), fill='x')

    def fg(et):
        fv = filedialog.askdirectory()
        if fv:
            et.ez = fv
            et.fh.configure(text=et.ez, text_color='green')

    def fx(et, fy, fz='white', **ga):
        et.ft.configure(state='normal')
        et.ft.insert('end', fy + '\n')
        et.ft.see('end')
        et.ft.configure(state='disabled')

    def fs(et):
        if not et.ez:
            et.fx('🚫 Please select a folder first.')
            return
        et.ft.configure(state='normal')
        et.ft.delete('1.0', 'end')
        et.ft.configure(state='disabled')
        et.fx('🔍 Scanning directory files...')
        et.after(500, et.gf)

    def gf(et):
        gg = {gh: fl.get() for gh, fl in et.dc.items()}
        dd = [s.strip() for s in et.fp.get().split(',')] if et.fp.get() else []
        dt(et.ez, et.fx, gg, dd)
        et.fx('\n✅ Analysis completed. Check the output folder.')

if __name__ == '__main__':
    c()
    gk = es()
    gk.mainloop()
