#!/usr/bin/env python3
"""Build the SA Refugees in the USA guide into site/. Run: python3 tools/build.py"""
import os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); sys.path.insert(0,HERE)
from sitelib import Site,CSS,D,NOTICE,esc,a
BASE="https://sa-refugees-usa-guide.vercel.app"
PP="https://sa-passport-id-usa-guide-w1ab.vercel.app/"; PPC=PP+"citizenship/"
S=dict(
 emb="https://za.usembassy.gov/refugee-admissions-program-for-south-africans/",
 embfaq="https://za.usembassy.gov/u-s-refugee-admissions-program-faqs/",
 emb2025="https://za.usembassy.gov/president-trumps-executive-order-on-addressing-egregious-actions-of-the-republic-of-south-africa/",
 pd26="https://www.federalregister.gov/documents/2026/05/27/2026-10598/emergency-presidential-determination-on-refugee-admissions-for-fiscal-year-2026",
 pd27="https://www.federalregister.gov/documents/2026/10/02/2026-20318/presidential-determination-on-refugee-admissions-for-fiscal-year-2027",
 frrma="https://www.federalregister.gov/documents/2026/10/01/2026-20111/period-for-refugee-cash-assistance-and-refugee-medical-assistance-correction",
 pir="https://acf.gov/orr/programs-services/refugees/pir",
 roles="https://acf.gov/orr/programs-services/refugees/resettlement-program",
 ben="https://acf.gov/orr/programs-services/refugees/eligibility/benefits-refugees",
 dcl="https://acf.gov/orr/policy-guidance/refugees/policy-instructions/dcl-26-05",
 src="https://acf.gov/orr/programs-services/refugees/contacts/state-contacts",
 gc="https://www.uscis.gov/green-card/green-card-eligibility/green-card-for-refugees",
 i131="https://www.uscis.gov/i-131",
 td="https://www.uscis.gov/travel-documents",
 scam="https://www.uscis.gov/scams-fraud-and-misconduct/avoid-scams/common-scams",
 ssnr="https://secure.ssa.gov/poms.nsf/lnx/0110211185",
 ssnw="https://secure.ssa.gov/poms.nsf/lnx/0110205005",
 ssncfr="https://www.ssa.gov/OP_Home/cfr20/422/422-0103.htm",
 ssa="https://www.ssa.gov/ssnumber/")
def src(*k): return ' <span class="src">['+', '.join(a(S[x]) for x in k)+']</span>'
G=[("1. Applying",[('eligibility/index.html','Eligibility and referral'),('programme-status/index.html','Programme status and caps'),('avoiding-scams/index.html','Avoiding scams')]),
 ("2. Arriving",[('first-90-days/index.html','First 90 days'),('social-security-card/index.html','Social Security card')]),
 ("3. First 90 days",[('benefits/index.html','Benefits checklist'),('health-cover/index.html','Health cover (RMA and Medicaid)'),('jobs/index.html','Jobs and employment services'),('agency-not-helping/index.html','When your agency is not helping')]),
 ("4. First year",[('travel-document/index.html','Refugee travel document (I-131)'),('sa-passport-citizenship/index.html','SA passport and citizenship risks')]),
 ("5. Green card and beyond",[('green-card/index.html','Green card after 1 year (I-485)')]),
 ("About",[('about/index.html','About this site')])]
ORDER=['index.html']+[p for g,it in G for p,t in it]
STAGE={p:g for g,it in G for p,t in it}
FOOT=f'<p>This is an independent, unofficial guide. It is not affiliated with any government or agency, including the U.S. Department of State, the U.S. Embassy in South Africa, ORR/ACF, USCIS, SSA, any resettlement agency or the South African government. Read more on the <a href="/about/">About page</a>. Facts link to official pages; always check the linked source.</p>'
s=Site(ROOT,BASE,"South African Refugees in the USA: plain-language guide",G,ORDER,FOOT,CSS)
def P(path,title,desc,body): s.page(path,title,desc,body,STAGE.get(path))
def L(path,text,frm): return f'<a href="{"../"*frm.count("/")}{path}">{text}</a>'

# HOME
cards=''
blurb={'eligibility/index.html':'Who can be referred and how the questionnaire works.','programme-status/index.html':'FY2026 and FY2027 refugee ceilings.','avoiding-scams/index.html':'The programme is free. Spot fake helpers.',
 'first-90-days/index.html':'What your local resettlement provider arranges.','social-security-card/index.html':'How refugees get an SSN and card.',
 'benefits/index.html':'Cash, medical, food and services to sign up for.','health-cover/index.html':'Refugee Medical Assistance now lasts up to 12 months.','jobs/index.html':'Work rights from day one, EAD and I-9.','agency-not-helping/index.html':'Contact your State Refugee Coordinator.',
 'travel-document/index.html':'You need one before leaving the USA.','sa-passport-citizenship/index.html':'What to check before using your SA passport.','green-card/index.html':'You must apply after 1 year; no fee for principal refugees.','about/index.html':'Independent site, sources and method.'}
for g,it in G:
    cards+=f'<section class="card stage"><h2>{esc(g)}</h2><div class="cards">'+''.join(f'<a class="card" href="{p}"><strong>{esc(t)}</strong><br>{blurb[p]}</a>' for p,t in it)+'</div></section>'
body=f'''<h1>South African refugees coming to the USA: where are you in the journey?</h1>
<p>A plain-language, factual guide for South Africans being processed through, or recently resettled by, the U.S. Refugee Admissions Program (USRAP). Pick your stage below.</p>
<div class="card note"><ul><li>The FY2026 refugee ceiling was raised from 7,500 to 17,500 by Presidential Determination 2026-14{src("pd26")}.</li><li>The FY2027 ceiling is up to 17,500 under Presidential Determination 2026-24{src("pd27")}.</li><li>Since 1 January 2026 the Office of Refugee Resettlement (ORR) runs initial resettlement{src("pir")}.</li></ul></div>
<div class="card warn"><strong>{NOTICE}</strong></div>
{cards}'''
s.page('index.html',"South African refugees in the USA: plain-language USRAP guide","Independent guide for South African refugees under USRAP: referral, arrival, first 90 days, benefits, health cover, Social Security, travel documents and the green card.",body)

f='eligibility/index.html'
P(f,"USRAP eligibility and referral for South Africans","Criteria and referral steps published by the U.S. Embassy in South Africa for refugee resettlement consideration.",f'''<h1>Eligibility and referral</h1>
<h2>Who the Embassy says can be considered</h2><div class="card"><p>The U.S. Mission South Africa page (dated 7 October 2026) lists all of these criteria{src("emb")}:</p><ul><li>South African nationality</li><li>Afrikaner ethnicity, or a member of a racial minority in South Africa</li><li>Able to describe past persecution or fear of future persecution on account of race, religion, nationality, membership in a particular social group or political opinion</li><li>At least 18, or referred with a parent</li><li>Living inside South Africa; the programme does not expect out-of-country processing</li></ul></div>
<h2>How to ask for referral</h2><div class="card"><ul><li>If no USRAP partner has contacted you yet, complete the online USRAP Intake Questionnaire (UIQ), linked from the Embassy page. This applies even if you sent an earlier Statement of Interest{src("emb")}.</li><li>Referral partners are RSC Africa (operated by Church World Service) and Amerikaners{src("emb","embfaq")}.</li><li>Not everyone is referred. The authority to grant access rests with the U.S. government{src("emb")}.</li><li>If accepted, next steps include a pre-screen interview, security vetting, a USCIS interview and a medical exam{src("embfaq")}.</li><li>There is no standard timeline. Case questions: SouthAfrica@cwsafrica.org with your case number{src("embfaq")}.</li></ul></div>
<h2>Conflicts and gaps</h2><div class="card conf"><ul><li>The Embassy's February 2025 notice says to email PretoriaPRMInfo@state.gov{src("emb2025")}; the October 2026 page says to complete the UIQ{src("emb")}. Follow the newer page.</li><li>The Presidential Determinations refer to "Afrikaners from South Africa"{src("pd26","pd27")}; the Embassy criteria also mention "a member of a racial minority"{src("emb")}.</li><li>Processing time: not stated by source.</li></ul></div>
<p>Next: read {L("avoiding-scams/index.html","Avoiding scams",f)} before you share documents with anyone.</p>''')

f='programme-status/index.html'
P(f,"USRAP programme status and refugee caps FY2026 and FY2027","FY2026 and FY2027 refugee admission ceilings from the Federal Register.",f'''<h1>Programme status and caps</h1>
<h2>FY2026 (1 October 2025 to 30 September 2026)</h2><div class="card"><ul><li>PD 2026-14 of 21 May 2026 raised the FY2026 ceiling from 7,500 (set by PD 2025-13) to 17,500{src("pd26")}.</li><li>The additional admissions are allocated among Afrikaners from South Africa, consistent with Executive Order 14204{src("pd26")}.</li><li>Published 27 May 2026, 91 FR 31645{src("pd26")}.</li></ul></div>
<h2>FY2027 determination</h2><div class="card"><ul><li>Yes, there is one. PD 2026-24 of 25 September 2026 authorises up to 17,500 refugee admissions in FY2027{src("pd27")}.</li><li>Admissions are "primarily" allocated among Afrikaners from South Africa under Executive Order 14204{src("pd27")}.</li><li>Published 2 October 2026{src("pd27")}.</li></ul></div>
<h2>Who runs what</h2><div class="card"><ul><li>The State Department identifies and refers applicants; USCIS interviews and checks them; CDC-approved doctors do the medical exam; CBP admits refugees at the port of entry; ORR starts services on arrival{src("roles")}.</li><li>ORR took over initial resettlement (now the Program of Initial Resettlement) on 1 January 2026{src("pir")}.</li></ul></div>
<p class="src">How many places are left in FY2027: not stated by source.</p>''')

f='avoiding-scams/index.html'
P(f,"Avoiding refugee programme scams","Official warnings about fees, fake partners and impersonators.",f'''<h1>Avoiding scams</h1>
<h2>The referral process is free</h2><div class="card warn"><ul><li>Access to USRAP is free, including the questionnaire. Referral partners do not charge fees{src("emb")}.</li><li>It is not necessary to have documents verified{src("emb")}.</li><li>Do not pay anyone who claims to expedite your case or guarantee approval. Only RSC Africa/CWS and Amerikaners are official referral and USRAP implementers in South Africa. Report fraud with the USRAP Tip Form{src("embfaq")}.</li></ul></div>
<h2>After you arrive</h2><div class="card"><ul><li>USCIS will never ask you to send money to a person, or to pay by Western Union, gift cards or similar{src("scam")}.</li><li>Notarios are not authorised to give immigration legal services. Only an attorney or an accredited representative of a DOJ-recognised organisation can{src("scam")}.</li><li>Forms are free on USCIS's site.{src("scam")}.</li><li>Government email addresses end in .gov{src("scam")}.</li></ul></div>
<h2>Where to report</h2><p>Suspect immigration fraud: the Federal Trade Commission or your state consumer protection office{src("scam")}. Suspicious USCIS-style email: USCIS.Webmaster@uscis.dhs.gov{src("scam")}.</p>''')

f='first-90-days/index.html'
P(f,"First 90 days: what your resettlement provider arranges","ORR Program of Initial Resettlement services in the first 30 to 90 days.",f'''<h1>First 90 days</h1>
<h2>Who helps you</h2><div class="card"><p>ORR coordinates placement and initial resettlement services up to 90 days through the Program of Initial Resettlement (PIR). Refugees are typically assigned a local resettlement provider{src("pir")}.</p><p>PIR is delivered by eight organisations: Catholic Charities USA, Church World Service, Ethiopian Community Development Council, Global Refuge, HIAS, International Rescue Committee, U.S. Committee for Refugees and Immigrants, and World Relief{src("pir")}.</p></div>
<h2>What the provider helps with</h2><div class="card"><ul><li>Airport welcome</li><li>Temporary or longer-term housing with food, necessities, furnishings and household items (hotels may be used where housing is limited)</li><li>Personal case management and a resettlement plan</li><li>Connections to cash and medical assistance</li><li>Referrals for the domestic medical screening, jobs, social services and school enrolment</li></ul>{src("pir")}</div>
<h2>Do these early</h2><ul><li>Sign up for benefits immediately: they are time-limited. See {L("benefits/index.html","Benefits checklist",f)}{src("ben")}.</li><li>Get the ORR-funded domestic medical screening soon after arrival{src("ben")}.</li><li>Check your {L("social-security-card/index.html","Social Security card",f)} arrives.</li><li>Keep your I-94 safe; it proves refugee status and work authorisation{src("ben","gc")}.</li></ul>
<p class="src">Minimum service period of 30 days: not stated by the ACF page; it says services "up to 90 days"{src("pir")}.</p>''')

f='social-security-card/index.html'
P(f,"Social Security number and card for refugees","How refugees get an SSN: at entry or at an SSA office.",f'''<h1>Social Security card</h1>
<h2>If you asked for an SSN during processing</h2><div class="card"><p>When a number is requested in the immigration process, DHS sends the data to SSA, SSA assigns the number and mails the card to the address you gave, or to your sponsoring agency if you had no address{src("ssncfr","ssnw")}.</p></div>
<h2>If you apply at an SSA office</h2><div class="card"><ul><li>SSA treats refugees as having permanent work authorisation and issues an unrestricted card (no legend){src("ssnr")}.</li><li>One document can prove age, identity and status, for example the I-94 website printout with the State Department transportation boarding letter carrying the refugee admission stamp{src("ssnr")}.</li><li>An I-94 with the refugee admission stamp, or an EAD with category A3, is also accepted{src("ssnr")}.</li></ul></div>
<h2>Lost card or stolen number</h2><p>Replacement and identity theft options are on {a(S["ssa"],"SSA's Social Security number page")}{src("ssa")}.</p>
<p class="src">How long the card takes to arrive: not stated by source.</p>''')

f='benefits/index.html'
P(f,"Benefits checklist for new refugees","ORR cash, medical and service benefits and what to bring.",f'''<h1>Benefits checklist</h1>
<h2>Sign up now</h2><div class="card warn">ORR says sign up immediately: cash and medical help are limited to a period from your ORR eligibility date{src("ben")}.</div>
<h2>Checklist</h2><div class="card"><ul>
<li><strong>Bring proof:</strong> I-94 showing admission under section 207, or I-94 code Visa 93, or EAD code A03{src("ben")}.</li>
<li><strong>Mainstream benefits:</strong> you may be eligible for TANF, SSI, Medicaid or SNAP{src("ben")}.</li>
<li><strong>Refugee Cash Assistance (RCA):</strong> if not eligible for TANF or SSI. Up to 12 months for an ORR eligibility date on or after 1 January 2026{src("dcl","frrma")}.</li>
<li><strong>Matching Grant:</strong> an alternative to TANF or RCA with limited slots; 240-day service period{src("ben")}.</li>
<li><strong>Refugee Medical Assistance (RMA):</strong> see {L("health-cover/index.html","Health cover",f)}.</li>
<li><strong>Domestic medical screening</strong> soon after arrival{src("ben")}.</li>
<li><strong>Refugee Support Services:</strong> jobs, English, childcare, transport, interpreting, case management, up to 5 years{src("ben")}.</li></ul></div>
<h2>Where to apply</h2><p>Your state benefits office or nearest resettlement agency. For local providers, contact your {L("agency-not-helping/index.html","State Refugee Coordinator",f)}{src("ben","src")}.</p>
<h2>Conflict between sources</h2><div class="card conf">The ACF benefits fact sheet (page dated 9 October 2026) still says four months of RCA and RMA for an eligibility date on or after 5 May 2025{src("ben")}. ORR's Dear Colleague Letter 26-05 (revised 1 October 2026) and the Federal Register correction say up to 12 months for an eligibility date on or after 1 January 2026{src("dcl","frrma")}. The newer policy letter appears to govern; confirm with your provider.</div>''')

f='health-cover/index.html'
P(f,"Health cover for refugees after 1 October 2026: RMA versus Medicaid","Refugee Medical Assistance length and how it relates to Medicaid.",f'''<h1>Health cover after 1 October 2026: RMA versus Medicaid</h1>
<h2>Refugee Medical Assistance (RMA)</h2><div class="card"><ul><li>RMA is for people not eligible for Medicaid and provides the same coverage as Medicaid{src("ben")}.</li><li>From 1 October 2026, ORR provides up to 12 months of RMA for people whose ORR eligibility date is on or after 1 January 2026{src("dcl","frrma")}.</li><li>States had up to 30 days to implement{src("dcl")}.</li><li>Conditions include not being eligible for Medicaid and meeting income and resource rules{src("dcl")}.</li></ul></div>
<h2>Medicaid</h2><div class="card"><ul><li>The ACF fact sheet says refugees may be eligible for Medicaid{src("ben")}.</li><li>ORR's letter cites "reduced access to other benefits" as a reason reliance on ORR assistance is rising{src("dcl")}.</li><li>Exactly how refugee Medicaid eligibility changed on 1 October 2026: not stated by the official sources this site uses. Ask your state Medicaid office or resettlement provider.</li></ul></div>
<h2>What to do</h2><ul><li>Apply for health cover straight away through your resettlement provider or state benefits office{src("ben")}.</li><li>Already enrolled in RMA? Ask how the 12-month period under DCL 26-05 applies to you{src("dcl")}.</li><li>Problems: contact the State Refugee Health Coordinator on {a(S["src"],"ACF's state contacts list")}{src("src")}.</li></ul>
<div class="card conf">Conflict: the ACF fact sheet still lists four months of RMA{src("ben")}, while DCL 26-05 says up to 12{src("dcl")}.</div>''')

f='jobs/index.html'
P(f,"Jobs and employment services for refugees","Work authorisation, EAD, Form I-9 and ORR employment services.",f'''<h1>Jobs and employment services</h1>
<h2>Your right to work</h2><div class="card"><ul><li>Refugees may work immediately on arrival{src("gc")}.</li><li>USCIS creates a digital I-765 for principal refugees and accompanying family; the EAD usually arrives within a few weeks{src("gc")}.</li><li>For Form I-9, your I-94 is acceptable for 90 days after arrival; after that show an unexpired EAD or other documents such as a driver's licence plus an unrestricted Social Security card{src("gc")}.</li><li>No fee for an initial or renewal refugee EAD (category (a)(3)){src("gc")}.</li></ul></div>
<h2>Free employment help</h2><div class="card"><ul><li>Refugee Support Services: job training, search, placement and retention, English classes, childcare and transport, up to 5 years{src("ben")}.</li><li>RCA is provided alongside employment services through your provider{src("ben")}. Detailed participation rules: not stated by the pages checked.</li><li>Matching Grant: intensive case management and job help, aiming at self-sufficiency within 240 days{src("ben")}.</li></ul></div>
<h2>Watch for job scams</h2><p>Be wary of overseas or email job offers that ask for money{src("scam")}. See {L("avoiding-scams/index.html","Avoiding scams",f)}.</p>''')

f='agency-not-helping/index.html'
P(f,"When your resettlement agency is not helping","How to escalate: grievance policies and State Refugee Coordinators.",f'''<h1>When your agency is not helping</h1>
<h2>Step 1: use the provider's grievance process</h2><div class="card">ORR requires programmes to have grievance policies so you can raise concerns, and says it reviews complaints with the implementing organisations{src("pir")}.</div>
<h2>Step 2: contact your State Refugee Coordinator</h2><div class="card"><p>ACF publishes a State Refugee Coordinator and State Refugee Health Coordinator for each state, with email and phone{src("src")}. Find yours on {a(S["src"],"ACF Key State Contacts")}. They can also give a list of providers in your area{src("ben")}.</p></div>
<h2>Step 3: ORR</h2><div class="card">ORR's Program of Initial Resettlement contact: DRSAPrograms@acf.hhs.gov{src("pir")}.</div>
<h2>Gaps</h2><p class="src">Response times for complaints: not stated by source. Contact names change; check the ACF page (dated 18 September 2026){src("src")}.</p>''')

f='travel-document/index.html'
P(f,"Refugee travel document (Form I-131)","Why refugees need a refugee travel document before leaving the USA.",f'''<h1>Refugee travel document (I-131)</h1>
<h2>Do you need one?</h2><div class="card warn"><ul><li>If you have refugee status but no green card yet, or you are a derivative refugee, you must have a refugee travel document to return to the USA{src("td")}.</li><li>Leaving without one may mean you cannot re-enter or are placed in removal proceedings{src("td")}.</li><li>Apply before you leave{src("td")}.</li></ul></div>
<h2>How to apply</h2><div class="card"><ul><li>File Form I-131. Refugee travel documents (Part 1, Box 2 or 3) cannot be filed online; file by mail{src("i131")}.</li><li>USCIS changed the I-131 filing location on 7 October 2026, with a grace period for forms postmarked by 9 November 2026. Check the Direct Filing Addresses page{src("i131")}.</li><li>Do not put Form I-131 in the same envelope as Form I-485{src("gc")}.</li><li>Fee: see the USCIS Fee Schedule{src("i131")}. Amount for refugees: not stated by the pages checked.</li></ul></div>
<h2>Cautions</h2><div class="card note">Travel may have severe immigration consequences. Travelling while your I-485 is pending without the right document may lead to denial or the application being treated as abandoned{src("td")}.</div>
<p>Thinking of using your South African passport instead? Read {L("sa-passport-citizenship/index.html","SA passport and citizenship risks",f)} first.</p>''')

f='sa-passport-citizenship/index.html'
P(f,"South African passport and citizenship: risks for refugees","What US official sources say about refugee travel, and where to read about SA passports and citizenship.",f'''<h1>SA passport and citizenship risks for refugees</h1>
<h2>What U.S. official sources say</h2><div class="card"><ul><li>A refugee without a green card needs a refugee travel document to return to the USA{src("td")}.</li><li>Your refugee status must not have been terminated when you apply for a green card{src("gc")}.</li><li>Whether using a South African passport or travelling to South Africa affects U.S. refugee status: not stated by the official sources this site checked. Ask an immigration attorney or accredited representative before you travel or renew.</li></ul></div>
<h2>South African passports and citizenship</h2><div class="card"><p>For renewing an SA passport or ID from the USA, see the separate {a(PP,"SA Passport and ID Guide (USA)")}. For questions about keeping South African citizenship, see its {a(PPC,"citizenship page")}. These are independent guides, not official sources.</p></div>
<div class="card warn"><strong>{NOTICE}</strong></div>''')

f='green-card/index.html'
P(f,"Green card after 1 year for refugees (Form I-485)","USCIS rules for refugee adjustment of status after one year.",f'''<h1>Green card after 1 year (I-485)</h1>
<h2>You must apply</h2><div class="card">U.S. law requires refugees to apply for permanent residence after at least 1 year of physical presence{src("gc")}.</div>
<h2>Eligibility</h2><div class="card"><ul><li>Admitted as a refugee under INA section 207</li><li>Physically present in the USA when filing, and for at least 1 year after admission</li><li>Refugee status not terminated; not already a permanent resident</li><li>Admissible, or eligible for a waiver (Form I-602)</li></ul>{src("gc")}</div>
<h2>What to send (principal applicant)</h2><div class="card"><ul><li>Form I-485. Principal refugees pay no filing or biometrics fee{src("gc")}.</li><li>Proof of refugee admission (such as I-94), evidence of 1 year presence, two passport-style photos, photo ID, birth certificate if available{src("gc")}.</li><li>Vaccination record part of Form I-693{src("gc")}.</li><li>Form I-602 waiver, if applicable{src("gc")}.</li></ul></div>
<h2>Family members</h2><div class="card">Derivative spouses and children follow similar rules, but USCIS points derivatives to the Fee Schedule for the I-485 fee{src("gc")}. Whether derivatives pay: not stated clearly by source.</div>
<p>Travelling while your I-485 is pending: see {L("travel-document/index.html","Refugee travel document",f)}{src("td")}.</p>''')

f='about/index.html'
P(f,"About this guide","Independent, unofficial guide. Not affiliated with any government or agency.",f'''<h1>About this site</h1>
<div class="card warn"><strong>{NOTICE}</strong></div>
<h2>Independent</h2><div class="card">This site is independent. It is not affiliated with, endorsed by or run for any government or agency: not the U.S. Department of State, the U.S. Embassy and Consulates in South Africa, HHS, ACF or ORR, USCIS, SSA, any resettlement agency or referral partner, or the South African government.</div>
<h2>Method</h2><div class="card"><ul><li>Only official sources are cited: state.gov and za.usembassy.gov, acf.gov, uscis.gov, ssa.gov, federalregister.gov and congress.gov. Each was opened and checked on {D}.</li><li>A link sits beside every fact. Where a source is silent we write "not stated by source". Conflicts between sources are shown openly.</li><li>The site is factual and does not take a political position.</li></ul></div>
<h2>Sources used</h2><ul>{"".join(f"<li>{a(u,esc(u))}</li>" for u in S.values())}</ul>''')
s.finish(); print(len(s.pages),'pages')
