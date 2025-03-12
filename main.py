import os
import re
import json
import shutil
import subprocess
import customtkinter as ctk
from tkinter import filedialog
import requests

cvs = "1.0"
cfu = f"https://api.github.com/repos/astrapy/FiveM-Trigger-Finder/releases/latest"

def b():
    try:
        response = requests.get(cfu, timeout=10)
        if response.status_code == 200:
            d = response.json()
            lv = d.get("tag_name", "").strip()
            if lv.lower().startswith("v"):
                lv = lv[1:]
            if lv and lv > cvs:
                print(f"New version available: {lv}. Updating...")
                assets = d.get("assets", [])
                du = None
                cf = os.path.basename(__file__)
                for asset in assets:
                    if asset.get("name", "").lower() == cf.lower():
                        du = asset.get("browser_du", "")
                        break
                if du:
                    nfs = requests.get(du, timeout=10)
                    if nfs.status_code == 200:
                        cfc = nfs.content
                        cff = os.path.abspath(__file__)
                        backup_file = cff + ".bak"
                        shutil.copy2(cff, backup_file)
                        with open(cff, "wb") as f:
                            f.write(cfc)
                        print("Update successful. Please restart the application.")
                        os._exit(0)
                    else:
                        print("Failed to download the new version.")
                else:
                    print("Update asset not found in the latest release.")
            else:
                print("No update available.")
        else:
            print("Failed to check for updates:", response.status_code)
    except Exception as e:
        print("Error while checking for updates:", e)

ctk.set_default_color_theme('lib/lavender.json')

def a(b='lib/categories.json'):
    with open(b, 'r', encoding='utf-8') as c:
        d = json.load(c)
    return [(e['category'], e['keywords']) for e in d]

def f(b='lib/ascii.json'):
    with open(b, 'r', encoding='utf-8') as c:
        return json.load(c)

def g(h, i):
    j = []
    for (k, l, m) in os.walk(h):
        for n in m:
            if any(n.endswith(p) for p in i):
                j.append(os.path.join(k, n))
    return j

def s(t):
    patterns = [
        r"RegisterNetEvent\(\s*[\'\"]([^\'\"]+)[\'\"]",
        r"TriggerServerEvent\(\s*[\'\"]([^\'\"]+)[\'\"]",
        r"TriggerClientEvent\(\s*[\'\"]([^\'\"]+)[\'\"]"
    ]
    for pattern in patterns:
        w = re.search(pattern, t)
        if w:
            return w.group(1)
    return ''

def y(z):
    categories = a()
    ab = {cat: [] for (cat, keywords) in categories}
    ab['Other'] = []
    for ad in z:
        ae = s(ad['lineTxt'])
        af = f"{ad['file']} {ad['lineTxt']} {ae}".lower()
        found = False
        for (cat, keywords) in categories:
            if any(kw in af for kw in keywords):
                ab[cat].append(ad)
                found = True
                break
        if not found:
            ab['Other'].append(ad)
    for cat in ab:
        ab[cat] = sorted(ab[cat], key=lambda al: (al['file'], al['lineNum']))
    return ab

def am(an, ab):
    os.makedirs(an, exist_ok=True)
    ascii_art = f()
    nyf = '-- No Framework Found.\n'
    ek = ('esx_', 'esx:')
    qk = ('qb-', 'qb_', 'qb:')
    fc = {'Framework: ESX': 0, 'Framework: QBCore': 0}
    for z in ab.values():
        for ad in z:
            line = ad['lineTxt'].lower()
            if any(kw in line for kw in ek):
                fc['Framework: ESX'] += 1
            if any(kw in line for kw in qk):
                fc['Framework: QBCore'] += 1
    fch = max(fc, key=lambda aw: fc[aw])
    if fc[fch] > 0:
        header = ascii_art.get(fch, nyf)
    else:
        header = nyf
    ct = ['Robbery', 'Police', 'Money', 'Drugs', 'Weapons', 'Gangs/Factions', 'Missions/Quests', 'Jobs', 'Inventory', 'Vehicles', 'Properties', 'Status', 'Framework: ESX', 'Framework: QBCore', 'Clothes', 'License', 'Medical', 'Administration', 'Connection', 'Callback', 'UI', 'Other', 'Casino']
    for cat in ct:
        z = ab.get(cat, [])
        cf = re.sub('[^a-zA-Z0-9_]', '_', cat)
        fp = os.path.join(an, f'{cf}.lua')
        with open(fp, 'w', encoding='utf-8') as c:
            c.write('-- Suggestions? Send it to astrapy or in our discord.gg/phantomai\n')
            c.write(f'{header}\n\n')
            if z:
                for ad in z:
                    c_ta = ' [COMMON]' if ad.get('common') else ''
                    c.write(f"-- Found in: {ad['file']}\n")
                    c.write(f"-- Line: {ad['lineNum']}{c_ta}\n")
                    c.write(f"{ad['lineTxt']}\n\n")
            else:
                c.write('-- No triggers found for this category.\n')

def bg(bh, bi, bj=None, bk=None):
    if bj is None:
        bj = {}
    if bk is None:
        bk = []
    try:
        bk = [bl.strip() for bl in bk if bl.strip()]
        bn = {'search': ['TriggerServerEvent', 'TriggerEvent'], 'params': ['money', 'jail', 'reward']}
        m = g(bh, ['.js', '.lua'])
        bo = []
        bp = []
        bq = []
        for n in m:
            try:
                with open(n, 'r', encoding='utf-8', errors='ignore') as c:
                    br = c.readlines()
            except Exception:
                continue
            for bt, t in enumerate(br, start=1):
                if any(bu in t for bu in bn['search']):
                    w = re.search(r'TriggerServerEvent\([^)]*\)', t)
                    if w:
                        bv = any(bw in w.group(0) for bw in bn['params'])
                        if w.group(0) not in [ad['lineTxt'] for ad in bo]:
                            bo.append({'file': n, 'lineNum': bt, 'common': bv, 'lineTxt': w.group(0)})
                for bx, by in bj.items():
                    if by and bx in t:
                        pattern = f'{re.escape(bx)}\\([^)]*\\)'
                        bz = re.search(pattern, t)
                        if bz:
                            if bz.group(0) not in [ad['lineTxt'] for ad in bp]:
                                bp.append({'file': n, 'lineNum': bt, 'common': False, 'lineTxt': bz.group(0)})
                if bk:
                    ca = t.lower()
                    for cb in bk:
                        if cb.lower() in ca:
                            bq.append({'file': n, 'lineNum': bt, 'string': cb, 'lineTxt': t.strip()})
        cc = os.path.basename(bh)
        cf = os.path.join('output', cc)
        os.makedirs(cf, exist_ok=True)
        cg = []
        for n in m:
            try:
                with open(n, 'r', encoding='utf-8', errors='ignore') as c:
                    br = c.readlines()
            except Exception:
                continue
            for bt, t in enumerate(br, start=1):
                ca = t.lower()
                if 'discord.com/api/webhooks' in ca or 'discordapp.com/api/webhooks' in ca:
                    w = re.search(r'(https?://[^\s]+)', t)
                    if w:
                        cg.append({'file': n, 'lineNum': bt, 'common': False, 'lineTxt': w.group(0)})
        with open(os.path.join(cf, 'webhooks.json'), 'w', encoding='utf-8') as ch:
            json.dump(cg, ch, indent=4)
        ci = []
        for n in m:
            try:
                with open(n, 'r', encoding='utf-8', errors='ignore') as c:
                    content = c.read()
            except Exception:
                continue
            if re.search(r'[^\s]{50,}', content):
                ci.append({'file': n, 'common': False, 'lineTxt': 'Obfuscated code detected'})
        with open(os.path.join(cf, 'obfuscated.json'), 'w', encoding='utf-8') as ck:
            json.dump(ci, ck, indent=4)
        cl = bo + bp
        ab = y(cl)
        an_path = os.path.join(cf, 'triggers')
        am(an_path, ab)
        if bq:
            cm = os.path.join('output', 'customstrings')
            os.makedirs(cm, exist_ok=True)
            cn = os.path.join(cm, f'{cc}.json')
            with open(cn, 'w', encoding='utf-8') as co:
                json.dump(bq, co, indent=4)
        cp = f'Results saved to:\n  • JSON files in: {cf}\n  • Trigger files in: {an_path}\n'
        if bq:
            cp += f"  • Custom strings in: {os.path.join('output', 'customstrings', cc + '.json')}\n"
        bi(cp, color='green')
    except Exception as cq:
        bi(f'❌ Error: {cq}\n', color='red')

class cr(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title('Phantom')
        self.geometry('450x580')
        self.iconbitmap('lib/logo.ico')
        self.cw = ctk.CTkLabel(self, text='Suggestions: discord.gg/phantomai', text_color='gray')
        self.cw.pack(pady=(5, 0))
        self.cy = ''
        self.cz = ctk.CTkTabview(self)
        self.cz.pack(expand=True, fill='both', padx=20, pady=1)
        self.cz.add('Trigger Finder')
        self.db = self.cz.tab('Trigger Finder')
        self.dd = ctk.CTkFrame(self.db)
        self.dd.pack(pady=(10, 0), padx=20, fill='x')
        self.de = ctk.CTkButton(self.dd, text='Select Folder', command=self.df, width=120)
        self.de.pack(pady=5, anchor='center')
        self.dg = ctk.CTkFrame(self.db)
        self.dg.pack(pady=5, padx=20, fill='x')
        self.dh = ctk.CTkLabel(self.dg, text='No folder selected', text_color='red')
        self.dh.pack(padx=(10, 10), pady=5, anchor='center')
        self.di = ctk.CTkFrame(self.db)
        self.di.pack(pady=10, padx=20, fill='x')
        self.dj = ctk.CTkLabel(self.di, text='Scan Additional Events:')
        self.dj.pack(pady=(0, 5))
        self.dk = ['AddEventHandler', 'RegisterNetEvent', 'TriggerClientEvent']
        self.dl = {}
        for dm in self.dk:
            dn = ctk.BooleanVar(value=True)
            do = ctk.CTkCheckBox(self.di, text=dm, variable=dn)
            do.pack(anchor='w', padx=10, pady=5)
            self.dl[dm] = dn
        self.dp = ctk.CTkFrame(self.db)
        self.dp.pack(pady=10, padx=20, fill='x')
        self.dq = ctk.CTkLabel(self.dp, text='Custom Strings (comma separated):')
        self.dq.pack(pady=(0, 5))
        self.dr = ctk.StringVar()
        self.ds = ctk.CTkEntry(self.dp, textvariable=self.dr, width=300)
        self.ds.pack(padx=10, pady=5)
        self.dt = ctk.CTkButton(self.db, text='Start Scan', command=self.du)
        self.dt.pack(pady=10)
        self.dv = ctk.CTkTextbox(self.db, wrap='word', width=760, height=200)
        self.dv.pack(padx=20, pady=10, fill='both', expand=True)

    def df(self):
        dw = filedialog.askdirectory()
        if dw:
            self.cy = dw
            self.dh.configure(text=self.cy, text_color='green')

    def dy(self, dz, color='white', eb=None, **kwargs):
        self.dv.configure(state='normal')
        self.dv.insert('end', dz + '\n')
        self.dv.see('end')
        self.dv.configure(state='disabled')


    def du(self):
        if not self.cy:
            self.dy('🚫 Please select a folder first.')
            return
        self.dv.configure(state='normal')
        self.dv.delete('1.0', 'end')
        self.dv.configure(state='disabled')
        self.dy('🔍 Scanning directory files...')
        self.after(500, self.ek)

    def ek(self):
        self.dy('📝 Analyzing file contents for triggers, webhook and obfuscated code...')
        bj = {dm: dn.get() for dm, dn in self.dl.items()}
        el = self.dr.get().strip()
        em = [bl.strip() for bl in el.split(',')] if el else []
        bg(self.cy, self.dy, bj, em)
        self.dy('\n✅ Analyzation completed. Check the output folder.')

if __name__ == '__main__':
    b()
    en = cr()
    en.mainloop()
