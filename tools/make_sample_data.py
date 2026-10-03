"""Generates PLACEHOLDER data so every chart renders before you have real numbers.
Every number produced here is made up. Replace each CSV with real data
(same column names) from the sources listed in README.md."""
import csv, math, random
random.seed(23)

# region, state, coastal, capital, lat, lon
REGIONS = [
 ("Sydney","NSW","Coastal","Yes",-33.87,151.21), ("Central Coast","NSW","Coastal","No",-33.43,151.34),
 ("Hunter","NSW","Coastal","No",-32.70,151.50), ("North Coast NSW","NSW","Coastal","No",-29.80,153.00),
 ("South Coast","NSW","Coastal","No",-35.90,150.10), ("Blue Mountains","NSW","Inland","No",-33.70,150.30),
 ("Snowy Mountains","NSW","Inland","No",-36.40,148.50), ("Riverina","NSW","Inland","No",-35.10,147.40),
 ("Outback NSW","NSW","Inland","No",-31.90,143.00),
 ("Melbourne","VIC","Coastal","Yes",-37.81,144.96), ("Great Ocean Road","VIC","Coastal","No",-38.50,143.50),
 ("Phillip Island","VIC","Coastal","No",-38.49,145.23), ("Peninsula","VIC","Coastal","No",-38.35,145.00),
 ("Gippsland","VIC","Coastal","No",-37.90,147.20), ("Goldfields","VIC","Inland","No",-36.90,144.00),
 ("High Country","VIC","Inland","No",-36.80,146.90), ("Spa Country","VIC","Inland","No",-37.35,144.15),
 ("Brisbane","QLD","Coastal","Yes",-27.47,153.03), ("Gold Coast","QLD","Coastal","No",-28.02,153.40),
 ("Sunshine Coast","QLD","Coastal","No",-26.65,153.07), ("Fraser Coast","QLD","Coastal","No",-25.30,152.85),
 ("Whitsundays","QLD","Coastal","No",-20.30,148.70), ("Tropical North Queensland","QLD","Coastal","No",-16.90,145.77),
 ("Outback Queensland","QLD","Inland","No",-23.40,144.30), ("Southern Queensland Country","QLD","Inland","No",-27.50,151.00),
 ("Adelaide","SA","Coastal","Yes",-34.93,138.60), ("Kangaroo Island","SA","Coastal","No",-35.80,137.25),
 ("Fleurieu Peninsula","SA","Coastal","No",-35.50,138.60), ("Barossa","SA","Inland","No",-34.50,139.00),
 ("Flinders Ranges and Outback","SA","Inland","No",-31.50,138.60),
 ("Destination Perth","WA","Coastal","Yes",-31.95,115.86), ("Australia's South West","WA","Coastal","No",-33.90,115.30),
 ("Australia's Coral Coast","WA","Coastal","No",-25.00,114.00), ("Australia's North West","WA","Coastal","No",-18.00,122.20),
 ("Australia's Golden Outback","WA","Inland","No",-30.75,121.50),
 ("Hobart and the South","TAS","Coastal","Yes",-42.88,147.33), ("East Coast","TAS","Coastal","No",-41.90,148.20),
 ("Launceston and the North","TAS","Coastal","No",-41.44,147.14),
 ("Darwin","NT","Coastal","Yes",-12.46,130.84), ("Lasseter","NT","Inland","No",-24.50,132.00),
 ("Canberra","ACT","Inland","Yes",-35.28,149.13),
]

with open("data/regions.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["region","state","coastal","capital","lat","lon","visitors_k","nights_k",
                "spend_m","dom_spend_m","intl_spend_m","jobs_share_2019","jobs_share_2024"])
    for r,s,c,cap,lat,lon in REGIONS:
        CAPS = {"Sydney":14000,"Melbourne":13000,"Brisbane":8000,"Destination Perth":5000,"Adelaide":4000,"Canberra":2500,"Hobart and the South":2000,"Darwin":900}
        base = CAPS[r]*random.uniform(0.9,1.1) if cap=="Yes" else random.uniform(150,4000)
        visitors = round(base)
        nights = round(visitors*random.uniform(2.4,4.6))
        spend = round(nights*random.uniform(0.15,0.42))            # $m
        intl = round(spend*random.uniform(0.05,0.35))
        dom = spend-intl
        j19 = round(random.uniform(2.5,6) if cap=="Yes" else random.uniform(3,24),1)
        j24 = round(max(1.0, j19*random.uniform(0.8,1.3)),1)
        w.writerow([r,s,c,cap,lat,lon,visitors,nights,spend,dom,intl,j19,j24])

# Monthly overnight trips for coastal regions (southern regions peak in summer, tropical north in winter)
MONTHLY = [("Tropical North Queensland",-16.9),("Whitsundays",-20.3),("Sunshine Coast",-26.65),
           ("Gold Coast",-28.02),("North Coast NSW",-29.8),("South Coast",-35.9),
           ("Great Ocean Road",-38.5),("Phillip Island",-38.49),("East Coast",-41.9)]
with open("data/monthly_regions.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["region","lat","month","trips_k"])
    for r,lat in MONTHLY:
        amp = (abs(lat)-23)/20                                     # >0 south (summer peak), <0 tropics
        base = random.uniform(40,300)
        for m in range(1,13):
            season = math.cos((m-1)/12*2*math.pi)                  # +1 in Jan, -1 in Jul
            w.writerow([r,lat,m,round(base*(1+0.45*amp*season+random.uniform(-0.05,0.05)),1)])

# International short-term visitor arrivals by state of stay, 2017-2025, with a COVID collapse
SHARE = {"NSW":.38,"VIC":.27,"QLD":.19,"WA":.09,"SA":.035,"TAS":.01,"NT":.01,"ACT":.005}
with open("data/arrivals_monthly.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["year","month","state","arrivals"])
    for y in range(2017,2026):
        for m in range(1,13):
            t = (y-2017)*12+m
            if (y==2020 and m>=4) or y==2021: level = 0.03
            elif y==2020 and m==3: level = 0.5
            elif y==2022: level = 0.35+0.035*m
            elif y>=2023: level = min(1.0, 0.8+0.03*(t-72)/4)
            else: level = 1+0.004*t
            seas = 1+0.22*math.cos((m-1)/12*2*math.pi)+ (0.12 if m in (10,11,12) else 0)
            for s,sh in SHARE.items():
                w.writerow([y,m,s,round(760000*level*seas*sh*random.uniform(.95,1.05))])

# Great Barrier Reef visitor days, average by month
with open("data/reef_monthly.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["month","visitor_days"])
    for m in range(1,13):
        w.writerow([m, round(180000+45000*math.cos((m-8)/12*2*math.pi)+random.uniform(-8000,8000))])

# Marine industry output by sector, whole-number percentages that sum to 100
SECT = [("Domestic marine tourism",1,"Tourism",36),("International marine tourism",2,"Tourism",8),
        ("Natural gas",3,"Other marine industry",31),("Water transport",4,"Other marine industry",9),
        ("Ship and boat building",5,"Other marine industry",6),("Fishing and aquaculture",6,"Other marine industry",4),
        ("Everything else",7,"Other marine industry",6)]
assert sum(s[3] for s in SECT)==100
with open("data/marine_sectors.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["sector","order","group","share_pct"])
    for s in SECT: w.writerow(s)
print("Sample data written to data/")
