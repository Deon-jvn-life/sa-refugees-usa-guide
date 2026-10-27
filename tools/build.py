#!/usr/bin/env python3
"""Build the SA Refugees in the USA guide into site/. Run: python3 tools/build.py"""
import os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); sys.path.insert(0,HERE)
import re
from sitelib import Site,CSS,D,NOTICE,esc,a,slug,href,INTAKE_FORM,intake_button
BASE="https://www.sarefugeesusa.org"
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
 td="https://www.uscis.gov/green-card/green-card-processes-and-procedures/travel-documents",
 scam="https://www.uscis.gov/scams-fraud-and-misconduct/avoid-scams/common-scams",
 ssnr="https://secure.ssa.gov/poms.nsf/lnx/0110211185",
 ssnw="https://secure.ssa.gov/poms.nsf/lnx/0110205005",
 ssncfr="https://www.ssa.gov/OP_Home/cfr20/422/422-0103.htm",
 ssa="https://www.ssa.gov/ssnumber/",
 uiq=INTAKE_FORM,
 dha="https://www.dha.gov.za/",
 snapu="https://www.fns.usda.gov/snap",
 refu="https://www.uscis.gov/humanitarian/refugees-and-asylum/refugees",
 guide="https://www.uscis.gov/sites/default/files/document/guides/Asylees_Refugees.pdf",
 i131i="https://www.uscis.gov/sites/default/files/document/forms/i-131instr.pdf",
 afm="https://www.uscis.gov/sites/default/files/document/policy-manual-afm/afm53-external.pdf",
 pm11="https://www.uscis.gov/policy-manual/volume-11-part-d",
 pm7="https://www.uscis.gov/policy-manual/volume-7-part-l-chapter-2",
 pm12="https://www.uscis.gov/policy-manual/volume-12-part-d-chapter-3",
 ptime="https://egov.uscis.gov/processing-times/",
 g1055="https://www.uscis.gov/g-1055",
 fam="https://fam.state.gov/fam/01fam/01fam0520.html",
 cdc_dogs="https://www.cdc.gov/importation/dogs/index.html",
 cdc_hr="https://www.cdc.gov/importation/dogs/high-risk-countries.html",
 cdc_fv="https://www.cdc.gov/importation/dogs/foreign-vaccinated-high-risk-countries.html",
 cdc_form="https://www.cdc.gov/importation/dogs/dog-import-form-instructions.html",
 cdc_labs="https://www.cdc.gov/importation/dogs/approved-labs.html",
 cdc_ani="https://www.cdc.gov/importation/bringing-an-animal-into-the-us/index.html",
 aphis_dogs="https://www.aphis.usda.gov/pet-travel/another-country-to-us-import/dogs",
 aphis_dis="https://www.aphis.usda.gov/pet-travel/another-country-to-us-import/dogs/disease-status",
 aphis_cats="https://www.aphis.usda.gov/pet-travel/another-country-to-us-import/cats",
 fdacs="https://www.fdacs.gov/Consumer-Resources/Animals/Animal-Movement/Dog-and-Cat-Movement-Requirements",
 iata="https://www.iata.org/en/programs/cargo/live-animals/pets/",
 nda="https://www.nda.gov.za/index.php/publication/433-export-procedures",
    dalrrd="https://www.dlrrd.gov.za/images/Branches/Economica%20Development%20Trade%20and%20Marketing/international-trade-and-promotions/trade-facilitation/information-packs-18-august-2021/export-certification.pdf",
    i131addr="https://www.uscis.gov/i-131-addresses",
    cdc_acf="https://www.cdc.gov/importation/dogs/approved-care-facilities.html",
    pender="https://penderpetretreat.com/cdc-iad-acf/",
    gateway="https://gatewayacc.com/more-information/",
    qatar_pets="https://www.qatarairways.com/en/baggage/animals.html",
    emirates_pets="https://www.emirates.com/us/english/help/faq-topics/baggage-and-lost-property/faq/what-are-the-rules-and-charges-for-travelling-with-animals/",
    delta_pets="https://pro.delta.com/content/agency/global/en/products-and-services/pet/pet-policies.html",
    united_pets="https://www.united.com/en/us/fly/travel/traveling-with-pets.html",
    petport="https://www.petport.co.za/international-pet-shipping-cost/",
    brakpan_spca="https://www.citizen.co.za/brakpan-herald/news-headlines/local-news/2026/10/15/spca-sterilisation-drive-treats-79-animals/",
    parks_vet="https://theparksanimalcare.co.za/pricing/",
    n400="https://www.uscis.gov/n-400",
    pm12d2="https://www.uscis.gov/policy-manual/volume-12-part-d-chapter-2",
    pm12d4="https://www.uscis.gov/policy-manual/volume-12-part-d-chapter-4",
    pm12d6="https://www.uscis.gov/policy-manual/volume-12-part-d-chapter-6",
    pm12d7="https://www.uscis.gov/policy-manual/volume-12-part-d-chapter-7",
    pm12d9="https://www.uscis.gov/policy-manual/volume-12-part-d-chapter-9",
    pm7l5="https://www.uscis.gov/policy-manual/volume-7-part-l-chapter-5",
    n400five="https://www.uscis.gov/citizenship/learn-about-citizenship/citizenship-and-naturalization/i-am-a-lawful-permanent-resident-of-5-years",
    natex="https://www.uscis.gov/citizenship/exceptions-and-accommodations",
    civics="https://www.uscis.gov/citizenship/find-study-materials-and-resources/check-for-test-updates",
    n400red="https://www.uscis.gov/forms/filing-fees/additional-information-on-filing-a-reduced-fee-request",
    i912="https://www.uscis.gov/i-912",
    feewaive="https://www.uscis.gov/forms/filing-fees/additional-information-on-filing-a-fee-waiver",
    ssswho="https://www.sss.gov/register/who-needs-to-register/",
    ssschart="https://www.sss.gov/wp-content/uploads/2026/07/WhoNeedstoRegister.Final.pdf",
    sssfaq="https://www.sss.gov/faq/",
    sssver="https://www.sss.gov/verify/",
    irs_spt="https://www.irs.gov/individuals/international-taxpayers/substantial-presence-test",
    irs_p519="https://www.irs.gov/publications/p519",
    irs_visa="https://www.irs.gov/individuals/international-taxpayers/taxation-of-aliens-by-visa-type-and-immigration-status",
    irs_fbar="https://www.irs.gov/businesses/small-businesses-self-employed/report-of-foreign-bank-and-financial-accounts-fbar",
    irs_fbarpen="https://www.irs.gov/pub/opr-taxpros/issue-number-2026-25-tax-practice-obligations-and-the-report-of-foreign-bank-and-financial-accounts.pdf",
    fincen_fbar="https://www.fincen.gov/report-foreign-bank-and-financial-accounts",
    irs_8938="https://www.irs.gov/businesses/corporations/do-i-need-to-file-form-8938-statement-of-specified-foreign-financial-assets",
    irs_i8938="https://www.irs.gov/instructions/i8938",
    irs_intpen="https://www.irs.gov/payments/international-information-reporting-penalties",
    irs_ftc="https://www.irs.gov/individuals/international-taxpayers/foreign-tax-credit",
    irs_2555="https://www.irs.gov/instructions/i2555",
    irs_w4="https://www.irs.gov/forms-pubs/about-form-w-4",
    irs_itin="https://www.irs.gov/tin/itin/individual-taxpayer-identification-number-itin",
    irs_tin="https://www.irs.gov/individuals/international-taxpayers/us-taxpayer-identification-number-requirement",
    irs_file="https://www.irs.gov/individual-tax-filing",
    irs_tc301="https://www.irs.gov/taxtopics/tc301",
    irs_drafts="https://www.irs.gov/draft-tax-forms",
    irs_vita="https://www.irs.gov/individuals/free-tax-return-preparation-for-qualifying-taxpayers",
    irs_freefile="https://www.irs.gov/newsroom/free-options-and-resources-for-preparing-and-filing-taxes-in-2026",
    irs_fx="https://www.irs.gov/individuals/international-taxpayers/foreign-currency-and-currency-exchange-rates",
    irs_3520="https://www.irs.gov/individuals/international-taxpayers/us-citizens-and-residents-abroad-filing-requirements",
    irs_5471="https://www.irs.gov/pub/irs-pdf/i5471.pdf",
    irs_8621="https://www.irs.gov/instructions/i8621",
    irs_8992="https://www.irs.gov/forms-pubs/about-form-8992",
    irs_8992dft="https://www.irs.gov/pub/irs-dft/i8992--dft.pdf",
    irs_treaty="https://www.irs.gov/pub/irs-trty/safrica.pdf",
    irs_treatypage="https://www.irs.gov/businesses/international-businesses/south-africa-tax-treaty-documents",
    fl_pit="https://floridarevenue.com/faq/Pages/FAQDetails.aspx?FAQID=1466",
    fl_new="https://www.floridarevenue.com/Forms_library/current/brochure/gt800025.pdf",
    sars_cease="https://www.sars.gov.za/individuals/cease-to-be-an-sa-tax-resident-and-reinstatement-of-sa-tax-resident/",
    sars_nr="https://www.sars.gov.za/individuals/tax-during-all-life-stages-and-events/tax-and-non-residents/",
    sars_cgt="https://www.sars.gov.za/types-of-tax/capital-gains-tax/",
    sars_ait="https://www.sars.gov.za/individuals/manage-your-tax-compliance-status/supporting-documents-for-obtaining-approval-international-transfers/",
    sars_tcs2021="https://www.sars.gov.za/latest-news/tcs-changes-in-respect-of-foreign-investment-allowance-fia-and-emigration/",
    sars_directive="https://www.sars.gov.za/guide-to-tax-directive-for-cease-to-be-resident-and-expiry-of-visa/",
    sars_paye="https://www.sars.gov.za/paye-gen-01-g20-guide-for-employers-iro-employees-tax-for-2026-external-guide/",
    sars_codes="https://www.sars.gov.za/wp-content/uploads/Ops/Guides/PAYE-AE-06-G06-Guide-for-Codes-Applicable-to-Employees-Tax-Certificates-2026-External-Guide.pdf",
    sars_35a="https://www.sars.gov.za/wp-content/uploads/Ops/Guides/IT-PP-02-G01-Amounts-to-be-Withheld-When-a-Non-Resident-Sells-Immovable-Property-in-South-AfricaSA-External-Guide.pdf",
    sars_shares="https://www.sars.gov.za/wp-content/uploads/Ops/Guides/Legal-Pub-Guide-IT11-Tax-guide-for-share-owners.pdf",
    sars_in43="https://www.sars.gov.za/wp-content/uploads/Legal/Notes/LAPD-IntR-IN-2012-43-Circumstances-Disposal-Shares-Capital-Nature-Amounts.pdf",
    sars_brochure="https://www.sars.gov.za/wp-content/uploads/Ops/Guides/LAPD-IT-G13-Tax-Brochure-for-Non-Residents.pdf",
    sarb_circ="https://www.resbank.co.za/content/dam/sarb/what-we-do/financial-surveillance/financial-surveillance-documents/2026/6-2026.pdf",
    sarb_guide="https://www.resbank.co.za/content/dam/sarb/what-we-do/financial-surveillance/financial-surveillance-documents/2026/Currency%20and%20Exchanges%20Guidelines%20for%20Individuals.pdf",
    sarb_faq="https://www.resbank.co.za/en/home/what-we-do/financial-surveillance/FinSurvFAQ",
    sarb_circ12="https://www.resbank.co.za/content/dam/sarb/what-we-do/financial-surveillance/financial-surveillance-documents/2025/12-2025.pdf",
    cipc_foreign="https://www.cipc.co.za/wp-content/uploads/2023/11/Notice_Foreigner-Assurance-verification_version-1.1.pdf",
    cipc_steps="https://www.cipc.co.za/wp-content/uploads/2024/01/Directors-Amendment-Step-by-Step-Automated-Appoint-Foreigner.pdf",
    gov_regs="https://www.gov.za/sites/default/files/gcis_document/202305/48648rg11585gon3444.pdf")
def src(*k): return ' <span class="src">['+', '.join(a(S[x]) for x in k)+']</span>'
# Menu groups are topics. TIMELINE is the previous and next path, in time order.
G=[("Before you arrive",[('eligibility/index.html','Who can be referred'),('online-intake/index.html','The free questionnaire'),('programme-status/index.html','How many people can come'),('avoiding-scams/index.html','Avoiding scams')]),
 ("Arriving",[('first-90-days/index.html','Your first 90 days'),('social-security-card/index.html','Social Security card'),('bringing-pets/index.html','Bringing your pets'),('agency-not-helping/index.html','If your helper is not helping')]),
 ("Work and money",[('jobs/index.html','Work and jobs'),('benefits/index.html','Cash, food and other help'),('tax-first-year/index.html','Tax when you start work'),('sa-tax-residency/index.html','SA tax residency'),('us-tax-treaty/index.html','US tax and the treaty'),('foreign-accounts/index.html','Reporting SA accounts'),('moving-money/index.html','Moving money and pensions'),('sa-company-property/index.html','A company or property')]),
 ("Health",[('health-cover/index.html','Health cover')]),
 ("Documents and travel",[('travel-document/index.html','Leaving the United States'),('sa-passport-citizenship/index.html','South African passport risks')]),
 ("Green card and citizenship",[('green-card/index.html','Green card after one year'),('naturalization/index.html','Citizenship after five years')]),
 ("Using this guide",[('faq/index.html','Common questions'),('find/index.html','All pages'),('glossary/index.html','Word list'),('about/index.html','About this guide'),('disclaimer/index.html','Disclaimer')])]
TIMELINE=[
 ("Before you leave South Africa",['eligibility/index.html','online-intake/index.html','programme-status/index.html','avoiding-scams/index.html']),
 ("First week",['first-90-days/index.html','social-security-card/index.html','jobs/index.html','benefits/index.html','health-cover/index.html','agency-not-helping/index.html']),
 ("First month",['bringing-pets/index.html']),
 ("First year",['tax-first-year/index.html','sa-tax-residency/index.html','us-tax-treaty/index.html','foreign-accounts/index.html','moving-money/index.html','sa-company-property/index.html','travel-document/index.html','sa-passport-citizenship/index.html']),
 ("After 1 year",['green-card/index.html']),
 ("After 5 years",['naturalization/index.html'])]
ORDER=[p for _period,paths in TIMELINE for p in paths]
WHEN={p:period for period,paths in TIMELINE for p in paths}
STAGE={p:g for g,it in G for p,t in it}
FOOT=f'<p>This is an independent, unofficial guide. It is not affiliated with any government or agency, including the U.S. Department of State, the U.S. Embassy in South Africa, ORR/ACF, USCIS, SSA, CBP, any resettlement agency or the South African government. Read more on the <a href="/about/">About page</a> and the <a href="/disclaimer/">disclaimer</a>. Facts link to official pages; always check the linked source.</p>'
GLOSS=[]
def gterm(h,pats,html): GLOSS.append((h,pats,html))
def P(path,title,desc,body,faqs=None,show_faqs=True): s.page(path,title,desc,body,STAGE.get(path),faqs=faqs,show_faqs=show_faqs)
def L(path,text,frm=None): return f'<a href="{href(path)}">{text}</a>'
gterm("A3 and A03",[r'\bA03\b',r'\bA3\b',r'\(a\)\(3\)'],f'The refugee code USCIS prints on an Employment Authorization Document. You may also see it written A3 or A03. SSA accepts an EAD in this category as evidence of status.{src("gc","ssnr","ben")}')
gterm("ACF",[r'\bACF\b'],f'The Administration for Children and Families, the part of the Department of Health and Human Services that includes the Office of Refugee Resettlement.{src("pir")}')
gterm("Advance parole",[r'\badvance parole\b'],f'A different USCIS travel document from the refugee travel document. The Form I-131 instructions say a refugee who is not yet a permanent resident must have a refugee travel document to re-enter unless they have an Advance Parole Document.{src("i131i")}')
gterm("APHIS",[r'\bAPHIS\b'],f'The Animal and Plant Health Inspection Service, part of the U.S. Department of Agriculture. For pet dogs it adds rules when a country is affected by foot-and-mouth disease or screwworm. CDC sets the rabies rules.{src("aphis_dogs")}')
gterm("ASC",[r'\bASC\b',r'\bApplication Support Cent(?:er|re)s?\b'],f'An Application Support Center. USCIS schedules biometrics, such as fingerprints and a photograph, at an ASC after you file for a refugee travel document.{src("guide","i131i")}')
gterm("CBP",[r'\bCBP\b',r'\bCustoms and Border Protection\b'],f'U.S. Customs and Border Protection. ORR says CBP admits refugees at the port of entry. A DHS officer at the port decides whether a person with a refugee travel document may come back in.{src("roles","i131i")}')
gterm("CDC",[r'\bCDC\b'],f'The Centers for Disease Control and Prevention. It sets the U.S. rules for bringing dogs and cats into the country, including rabies rules for dogs.{src("cdc_dogs","cdc_ani")}')
gterm("CDC Dog Import Form",[r'\bCDC Dog Import Forms?\b'],f'The free online form CDC requires for each dog entering the United States. You show the receipt to the airline and to Customs and Border Protection.{src("cdc_form","cdc_fv")}')
gterm("CFR",[r'\bCFR\b',r'\bCode of Federal Regulations\b'],f'The Code of Federal Regulations, where federal rules are published. The Social Security rule cited on this site is 20 CFR 422.103.{src("ssncfr")}')
gterm("DALRRD",[r'\bDALRRD\b',r'\bDepartment of Agriculture\b'],f'Older South African pages say DALRRD or DAFF. Export certification of animals is now on the Department of Agriculture website. A state veterinarian, not a private vet, signs the official export certificate.{src("nda","dalrrd")}')
gterm("DHA",[r'\bDHA\b',r'\bDepartment of Home Affairs\b'],f'The South African Department of Home Affairs. Its website is the official place for civic services such as passports and identity documents.{src("dha")}')
gterm("DHS",[r'\bDHS\b',r'\bDepartment of Homeland Security\b'],f'The U.S. Department of Homeland Security. USCIS and CBP are part of it. When a Social Security number is requested in the immigration process, DHS sends the data to SSA.{src("ssncfr","emb")}')
gterm("EAD",[r'\bEADs?\b',r'\bEmployment Authorization Documents?\b'],f'An Employment Authorization Document, the card that shows you may work. USCIS produces one for principal refugees and family who arrive with them.{src("gc")}')
gterm("Executive Order (EO)",[r'\bExecutive Orders?\b',r'\bEO\b'],f'An order signed by the President. The refugee admission determinations on this site refer to Executive Order 14204.{src("pd26")}')
gterm("Federal Register (FR)",[r'\bFederal Register\b',r'\b\d+ FR \d+\b'],f'The official daily journal of the U.S. government. A citation such as 91 FR 31645 means volume 91, page 31645.{src("pd26")}')
gterm("Fiscal year (FY)",[r'\bFY\d{4}\b',r'\bfiscal years?\b'],f'For these refugee ceilings, the federal fiscal year runs from 1 October to 30 September. FY2026 is 1 October 2025 to 30 September 2026.{src("pd26")}')
gterm("Foot-and-mouth disease (FMD)",[r'\bfoot-and-mouth disease\b',r'\bFMD\b'],f'A livestock disease. APHIS has extra dog-import rules if the country of origin is affected. The disease-status page checked on {D} does not name South Africa.{src("aphis_dogs","aphis_dis")}')
gterm("Green card (LPR)",[r'\bgreen cards?\b',r'\bLPRs?\b',r'\blawful permanent residents?\b'],f'A green card is proof of lawful permanent resident status. Refugees must apply on Form I-485 after one year of physical presence.{src("gc")}')
gterm("I-131",[r'\bI-131\b'],f'USCIS Form I-131, the application for a refugee travel document and for some other travel documents.{src("i131")}')
gterm("I-485",[r'\bI-485\b'],f'USCIS Form I-485, the application refugees use to become permanent residents.{src("gc")}')
gterm("I-571",[r'\bI-571\b'],f'The document number of the refugee travel document itself. USCIS says it can be used in place of a passport and is valid for 1 year, or until refugee or asylee status expires, whichever comes first.{src("guide")}')
gterm("I-9",[r'\bI-9\b'],f'Form I-9, the form an employer uses to check identity and permission to work. A refugee I-94 is acceptable for 90 days after arrival.{src("gc")}')
gterm("I-94",[r'\bI-94s?\b'],f'The arrival and departure record. For a refugee it shows admission under section 207 and is evidence of status and of permission to work.{src("ben","gc")}')
gterm("IATA",[r'\bIATA\b'],f'The International Air Transport Association. Airlines use its Container Requirement 1 to judge the size of a dog or cat crate.{src("iata")}')
gterm("INA",[r'\bINA\b',r'\bImmigration and Nationality Act\b'],f'The Immigration and Nationality Act. Section 207 is the section on refugee admissions.{src("gc")}')
gterm("IOM",[r'\bIOM\b',r'\bInternational Organization for Migration\b'],f'The International Organization for Migration. The linked Foreign Affairs Manual page now says this subchapter is unassigned and does not define this name. The October 2026 Embassy page for this programme does not name IOM as the office that books refugee travel. It names RSC Africa, operated by Church World Service.{src("fam","emb")}')
gterm("Matching Grant",[r'\bMatching Grants?\b'],f'An ORR alternative to TANF or Refugee Cash Assistance. Places are limited and the service period is 240 days.{src("ben")}')
gterm("Medicaid",[r'\bMedicaid\b'],f'A joint federal and state health programme. ORR says refugees may be eligible. Refugee Medical Assistance is for people who are not eligible for Medicaid.{src("ben")}')
gterm("Microchip",[r'\bmicrochips?\b'],f'For a dog that has been in a high-risk rabies country, CDC requires a chip a universal scanner can read, implanted before the rabies vaccine. The number must appear on the forms.{src("cdc_fv")}')
gterm("ORR",[r'\bORR\b'],f'The Office of Refugee Resettlement, inside ACF. It runs initial resettlement and refugee cash and medical assistance.{src("pir")}')
gterm("PIR",[r'\bPIR\b',r'\bProgram of Initial Resettlement\b'],f'The Program of Initial Resettlement. ORR\'s name for support in the first period after arrival, up to 90 days, which it took over on 1 January 2026.{src("pir")}')
gterm("POMS",[r'\bPOMS\b',r'\bProgram Operations Manual System\b'],f'SSA\'s Program Operations Manual System, the staff instructions that say which documents a refugee can use for a Social Security card.{src("ssnr")}')
gterm("PRM",[r'\bPRM\b'],f'The Bureau of Population, Refugees, and Migration at the Department of State. The Embassy FAQ uses this name. The February 2025 Embassy notice used the mailbox PretoriaPRMInfo@state.gov.{src("embfaq","emb2025","fam")}')
gterm("Presidential Determination (PD)",[r'\bPresidential Determinations?\b',r'\bPD\b'],f'A Presidential Determination sets the refugee admissions ceiling for a fiscal year. PD 2026-14 and PD 2026-24 are the ones cited on this site.{src("pd26","pd27")}')
gterm("Rabies serology titer",[r'\brabies serology titers?\b',r'\bserology titers?\b',r'\btiters?\b'],f'A blood test that shows whether a dog responded to the rabies vaccine. For a foreign-vaccinated dog from a high-risk country, a valid result from a CDC-approved laboratory is what lets the dog avoid a 28-day quarantine.{src("cdc_fv","cdc_labs")}')
gterm("RCA",[r'\bRCA\b',r'\bRefugee Cash Assistance\b'],f'Refugee Cash Assistance. Cash help from ORR if you are not eligible for TANF or SSI. For an eligibility date on or after 1 January 2026, ORR\'s current letter says up to 12 months.{src("dcl","ben")}')
gterm("Reception and Placement (R and P)",[r'\bR&amp;P\b',r'\bReception and Placement\b'],f'The older name for the initial support that ORR now calls the Program of Initial Resettlement.{src("pir")}')
gterm("Refugee travel document",[r'\brefugee travel documents?\b',r'\bRTDs?\b'],f'Also called Form I-571. The document USCIS issues so a refugee can travel abroad and ask to return to the United States. You apply on Form I-131.{src("guide","i131")}')
gterm("Resettlement agency",[r'\bresettlement (?:agency|agencies|provider|providers)\b'],f'The local organisation assigned to meet you and help with the first weeks after arrival. ORR also calls this a local resettlement provider.{src("pir")}')
gterm("RMA",[r'\bRMA\b',r'\bRefugee Medical Assistance\b'],f'Refugee Medical Assistance. Health cover from ORR for people who are not eligible for Medicaid. From 1 October 2026 it can last up to 12 months for an eligibility date on or after 1 January 2026.{src("dcl","ben")}')
gterm("Screwworm",[r'\bscrewworm\b'],f'A parasite of warm-blooded animals. If APHIS lists the country as affected, a dog needs a government vet certificate of inspection within 5 days before shipment. The disease-status page checked on {D} does not name South Africa.{src("aphis_dogs","aphis_dis")}')
gterm("SNAP",[r'\bSNAP\b'],f'The Supplemental Nutrition Assistance Program, the federal food assistance programme. ORR says refugees may be eligible.{src("ben","snapu")}')
gterm("SSA",[r'\bSSA\b'],f'The Social Security Administration, the agency that issues Social Security numbers and cards.{src("ssa")}')
gterm("SSI",[r'\bSSI\b'],f'Supplemental Security Income, a federal cash benefit for some older or disabled people. ORR lists it among benefits refugees may qualify for.{src("ben")}')
gterm("SSN",[r'\bSSNs?\b',r'\bSocial Security numbers?\b'],f'A Social Security number. Refugees can be assigned one from the immigration record, or they can apply at an SSA office.{src("ssncfr","ssa")}')
gterm("State veterinarian",[r'\bstate veterinarians?\b'],f'In South Africa, the official government veterinarian who can endorse an export health certificate. A private vet can prepare the animal but cannot give the official certificate.{src("nda","dalrrd","cdc_fv")}')
gterm("TANF",[r'\bTANF\b'],f'Temporary Assistance for Needy Families, the state cash programme for some families with children. ORR says refugees may be eligible.{src("ben")}')
gterm("USCIS",[r'\bUSCIS\b'],f'U.S. Citizenship and Immigration Services, the DHS agency that interviews refugee applicants and decides applications such as Form I-131 and Form I-485.{src("roles","gc")}')
gterm("USDA",[r'\bUSDA\b'],f'The U.S. Department of Agriculture. APHIS is the part of USDA that sets some pet-import rules.{src("aphis_dogs")}')
gterm("USRAP",[r'\bUSRAP\b'],f'The U.S. Refugee Admissions Program, the programme through which refugees are referred, interviewed and resettled.{src("emb")}')
gterm("Visa 93",[r'\bVisa 93\b'],f'A code that can appear on an I-94 for a refugee who followed to join family. ORR lists it as one way to prove refugee status for benefits.{src("ben")}')
gterm("Church World Service (CWS)",[r'\bCWS\b',r'\bChurch World Service\b'],f'The organisation that operates RSC Africa. The Embassy names Church World Service as one of the two USRAP referral partners in South Africa.{src("emb")}')
gterm("Department of Justice (DOJ)",[r'\bDOJ\b'],f'The U.S. Department of Justice. USCIS says immigration legal help should come from an attorney or from an accredited representative of a DOJ-recognised organisation.{src("scam")}')
gterm("Fish and Wildlife Service (FWS)",[r'\bFWS\b',r'\bFish and Wildlife Service\b'],f'The U.S. Fish and Wildlife Service. USDA tells people importing a pet cat to check CDC, this service, and the state they are going to.{src("aphis_cats")}')
gterm("Form N-470",[r'\bN-470\b'],f'Application to Preserve Residence for Naturalization Purposes. For some permanent residents it can keep continuous residence for naturalisation during qualifying work abroad. It is a different form from the refugee travel document.{src("pm12")}')
gterm("OCVI",[r'\bOCVI\b',r'\bofficial certificates? of veterinary inspection\b'],f'An official certificate of veterinary inspection. Florida uses this name for an animal health certificate. The state page gives a 30-day window, with exceptions that include a privately owned pet travelling with its owner.{src("fdacs")}')
gterm("Re-entry permit",[r'\bre-entry permits?\b',r'\breentry permits?\b'],f'A travel document for lawful permanent residents, requested on Form I-131. The instructions say lengthy or frequent absences without one can support a finding that permanent residence was abandoned.{src("i131i")}')
gterm("RSC Africa",[r'\bRSC\b'],f'Resettlement Support Center Africa, operated by Church World Service. The Embassy names it as a USRAP partner for case processing and for booking refugee travel to the United States.{src("emb","embfaq")}')
gterm("UIQ",[r'\bUIQ\b',r'\bUSRAP Intake Questionnaires?\b'],f'The USRAP Intake Questionnaire. The online form the U.S. Embassy in South Africa tells people to complete if they want to be considered for a referral.{src("emb")}')
gterm("Form N-400",[r'\bN-400\b'],f'USCIS Form N-400, Application for Naturalization. A permanent resident uses it to apply for U.S. citizenship. For a refugee, the permanent-residence date for the general 5-year rule is generally the date of entry as a refugee, once adjustment of status is approved.{src("n400","pm12d2","pm7l5")}')
gterm("Good moral character",[r'\bgood moral character\b'],f'A requirement for naturalisation. Under the general rule, the applicant must show it for the 5 years immediately before filing Form N-400 and up to the oath. Conduct from before those 5 years can still matter.{src("n400five","pm12d9")}')
gterm("Selective Service",[r'\bSelective Service\b'],f'The registration system for most men living in the United States from age 18 through 25, including refugees. Registration is not the same as joining the military. A knowing and willful failure to register can affect a later naturalisation application.{src("ssschart","sssfaq","pm12d7")}')
gterm("FBAR (FinCEN Form 114)",[r'\bFBARs?\b',r'\bFinCEN Form 114\b'],f'FinCEN Form 114, the Report of Foreign Bank and Financial Accounts. A United States person files it if foreign financial accounts together went over $10,000 at any time in the calendar year. It is filed with FinCEN, not as part of the income tax return.{src("irs_fbar","fincen_fbar")}')
gterm("FinCEN",[r'\bFinCEN\b'],f'The Financial Crimes Enforcement Network, a bureau of the U.S. Department of the Treasury. It receives the FBAR.{src("fincen_fbar","irs_fbar")}')
gterm("Form 8938",[r'\bForm 8938\b'],f'IRS Form 8938, Statement of Specified Foreign Financial Assets. Some United States taxpayers attach it to the income tax return when specified foreign financial assets are above the threshold for their filing status. It is a different form from the FBAR.{src("irs_8938")}')
gterm("SARS",[r'\bSARS\b'],f'The South African Revenue Service, the South African tax authority.{src("sars_cease")}')
gterm("SARB",[r'\bSARB\b'],f'The South African Reserve Bank. Its Financial Surveillance Department publishes the exchange-control rules for moving money.{src("sarb_guide","sarb_circ")}')
gterm("IRP5",[r'\bIRP5s?\b',r'\bIT3\(a\)\b'],f'An employees\' tax certificate. SARS says an employer who pays remuneration must give the employee an IRP5 or IT3(a) showing pay and employees\' tax deducted.{src("sars_paye")}')
gterm("ITIN",[r'\bITINs?\b'],f'An individual taxpayer identification number. The IRS issues it on Form W-7 to a person who needs a United States taxpayer number and is not eligible for a Social Security number.{src("irs_itin")}')
gterm("Substantial presence test",[r'\bsubstantial presence test\b'],f'The IRS day-count test for tax residence. You meet it if you are physically present in the United States for at least 31 days in the current year and 183 counted days over three years.{src("irs_spt","irs_p519")}')
gterm("Form W-4",[r'\bForm W-4\b',r'\bW-4\b'],f'The Employee\'s Withholding Certificate. You give it to an employer so the employer can withhold federal income tax from your pay.{src("irs_w4")}')
gterm("Foreign tax credit",[r'\bforeign tax credits?\b'],f'A credit that can reduce United States tax when you paid qualifying foreign income tax on the same income. Individuals claim it on Form 1116. You cannot claim it for tax on income you exclude.{src("irs_ftc")}')
gterm("VITA",[r'\bVITA\b'],f'Volunteer Income Tax Assistance. IRS-certified volunteers prepare basic returns for free. The IRS says many sites help people who generally make about $70,244 or less, people with disabilities, and people with limited English. A site can set its own limit.{src("irs_vita")}')
TERMS=[(slug(h),pats) for h,pats,_html in GLOSS]
s=Site(ROOT,BASE,"South African Refugees in the USA: plain-language guide",G,ORDER,FOOT,CSS,terms=TERMS,gsc='u0-9sKvlH1xyV4_DYf2JvQGap_ao0XPEfzPvMaGs_Ts',msvalidate='',related=[(PP,"SA Passport and ID Guide (USA)"),("https://sa-smart-id-bank-finder.vercel.app/","SA Smart ID bank finder")])

# HOME
BLURB={
 'eligibility/index.html':'Who the Embassy says can be considered for a referral.',
 'online-intake/index.html':'The official intake questionnaire: who should submit it, and what happens next.',
 'programme-status/index.html':'Refugee ceilings for fiscal year 2026 and fiscal year 2027.',
 'avoiding-scams/index.html':'The programme is free. Spot fake helpers and pet-travel scams.',
 'bringing-pets/index.html':'Centers for Disease Control and Prevention and Department of Agriculture rules for pets, how long a dog takes, and what the Embassy says about pets.',
 'first-90-days/index.html':'What your local resettlement provider arranges.',
 'social-security-card/index.html':'How refugees get a Social Security number and card.',
 'benefits/index.html':'Cash, medical, food and services to sign up for.',
 'health-cover/index.html':'Refugee Medical Assistance now lasts up to 12 months.',
 'jobs/index.html':'You may work from the day you arrive. The work card and Form I-9.',
 'tax-first-year/index.html':'The checklist if you were an employee in South Africa and you have come to work.',
 'sa-tax-residency/index.html':'How SARS says you cease South African tax residency, and the deemed disposal.',
 'us-tax-treaty/index.html':'When the IRS treats you as a resident, and what the South Africa treaty says.',
 'foreign-accounts/index.html':'FinCEN Form 114 and IRS Form 8938 for South African accounts.',
 'moving-money/index.html':'South African transfer rules, retirement funds, and the pension treaty article.',
 'sa-company-property/index.html':'Forms to consider if you still have a company, property, a directorship, or cash.',
 'agency-not-helping/index.html':'Contact your State Refugee Coordinator.',
 'travel-document/index.html':'Whether you can leave the United States, and how the refugee travel document works.',
 'sa-passport-citizenship/index.html':'Why a South African passport can put refugee status at risk.',
 'green-card/index.html':'You must apply after 1 year of physical presence. Travel can pause that clock.',
 'naturalization/index.html':'Form N-400. For a refugee the 5 years generally run from arrival in the United States.',
 'faq/index.html':'Short answers on applying, arrival, work, benefits, pets and the green card.',
 'about/index.html':'Independent site, sources and method.',
 'glossary/index.html':'Plain-English meanings for the abbreviations on this site.',
 'disclaimer/index.html':'General information only. Not legal advice and not a government site.',
 'find/index.html':'Every page on this guide, listed by topic.'}
ALIAS={
 'eligibility/index.html':'USRAP eligibility referral',
 'online-intake/index.html':'UIQ questionnaire intake form',
 'programme-status/index.html':'FY2026 FY2027 cap ceiling',
 'avoiding-scams/index.html':'fraud scam fee',
 'bringing-pets/index.html':'CDC USDA dog cat rabies pet',
 'first-90-days/index.html':'PIR arrival resettlement 90',
 'social-security-card/index.html':'SSN SSA social security number',
 'benefits/index.html':'RCA SNAP TANF SSI medicaid cash benefits',
 'health-cover/index.html':'RMA medicaid refugee medical assistance health',
 'jobs/index.html':'EAD I-9 work employment authorization job',
 'tax-first-year/index.html':'tax IRP5 W-4 1040 SSN first year employee refugee',
 'sa-tax-residency/index.html':'SARS cease residency exit tax section 9H ordinarily resident',
 'us-tax-treaty/index.html':'substantial presence green card treaty dual status Form 1116 Form 2555',
 'foreign-accounts/index.html':'FBAR FinCEN 114 Form 8938 FATCA foreign account',
 'moving-money/index.html':'SDA AIT retirement annuity pension SARB allowance',
 'sa-company-property/index.html':'Form 5471 CFC PFIC director property section 35A dividends',
 'agency-not-helping/index.html':'grievance coordinator complaint agency',
 'travel-document/index.html':'I-131 I-571 travel document leave USA',
 'sa-passport-citizenship/index.html':'SA passport South Africa citizenship',
 'green-card/index.html':'I-485 green card permanent resident',
 'naturalization/index.html':'N-400 citizenship naturalization naturalisation',
 'faq/index.html':'questions FAQ',
 'glossary/index.html':'abbreviations definitions words glossary',
 'about/index.html':'about sources independent',
 'disclaimer/index.html':'legal advice disclaimer',
 'find/index.html':'search index all pages'}
READ_NEXT={
 'index.html':['first-90-days/index.html','jobs/index.html','health-cover/index.html'],
 'eligibility/index.html':['avoiding-scams/index.html','programme-status/index.html','faq/index.html'],
 'online-intake/index.html':['eligibility/index.html','avoiding-scams/index.html','faq/index.html'],
 'programme-status/index.html':['eligibility/index.html','online-intake/index.html','avoiding-scams/index.html'],
 'avoiding-scams/index.html':['online-intake/index.html','bringing-pets/index.html','first-90-days/index.html'],
 'bringing-pets/index.html':['avoiding-scams/index.html','first-90-days/index.html','agency-not-helping/index.html'],
 'first-90-days/index.html':['tax-first-year/index.html','benefits/index.html','jobs/index.html'],
 'social-security-card/index.html':['benefits/index.html','health-cover/index.html','first-90-days/index.html'],
 'jobs/index.html':['tax-first-year/index.html','social-security-card/index.html','benefits/index.html'],
 'benefits/index.html':['jobs/index.html','social-security-card/index.html','agency-not-helping/index.html'],
 'health-cover/index.html':['benefits/index.html','jobs/index.html','first-90-days/index.html'],
 'agency-not-helping/index.html':['first-90-days/index.html','benefits/index.html','faq/index.html'],
 'travel-document/index.html':['green-card/index.html','naturalization/index.html','first-90-days/index.html'],
 'sa-passport-citizenship/index.html':['travel-document/index.html','naturalization/index.html','disclaimer/index.html'],
 'green-card/index.html':['travel-document/index.html','sa-passport-citizenship/index.html','jobs/index.html'],
 'naturalization/index.html':['green-card/index.html','travel-document/index.html','jobs/index.html'],
 'tax-first-year/index.html':['sa-tax-residency/index.html','us-tax-treaty/index.html','sa-company-property/index.html'],
 'sa-tax-residency/index.html':['tax-first-year/index.html','moving-money/index.html','us-tax-treaty/index.html'],
 'us-tax-treaty/index.html':['tax-first-year/index.html','foreign-accounts/index.html','sa-tax-residency/index.html'],
 'foreign-accounts/index.html':['tax-first-year/index.html','moving-money/index.html','sa-company-property/index.html'],
 'moving-money/index.html':['sa-tax-residency/index.html','foreign-accounts/index.html','sa-company-property/index.html'],
 'sa-company-property/index.html':['tax-first-year/index.html','moving-money/index.html','foreign-accounts/index.html'],
 'faq/index.html':['first-90-days/index.html','eligibility/index.html','glossary/index.html'],
 'find/index.html':['first-90-days/index.html','glossary/index.html','faq/index.html'],
 'glossary/index.html':['faq/index.html','about/index.html','disclaimer/index.html'],
 'about/index.html':['disclaimer/index.html','glossary/index.html','faq/index.html'],
 'disclaimer/index.html':['about/index.html','faq/index.html','glossary/index.html'],
 '404.html':['first-90-days/index.html','faq/index.html','glossary/index.html']}
s.summaries=BLURB
s.when=WHEN
s.read_next=READ_NEXT
s.aliases=ALIAS
_TAX_CHECKED=('27 October 2026','2026-10-27')
s.checked={p:_TAX_CHECKED for p in (
 'tax-first-year/index.html','sa-tax-residency/index.html','us-tax-treaty/index.html',
 'foreign-accounts/index.html','moving-money/index.html','sa-company-property/index.html')}
grouped=[p for _g,it in G for p,_t in it]
assert set(BLURB)==set(grouped)
assert set(ALIAS)==set(grouped)
assert set(p for _per,ps in TIMELINE for p in ps)<=set(grouped)
assert set(READ_NEXT)==set(grouped)|{'index.html','404.html'}
for _src,dests in READ_NEXT.items():
    assert len(dests)==3
    for dest in dests:
        assert dest in grouped
def jump(p, label=None):
    title=label or s.titles[p]
    return f'<a class="jump" href="{href(p)}"><span class="lt">{esc(title)}</span><span class="ls">{esc(BLURB[p])}</span></a>'
timeline=''.join(
    f'<li class="period"><h3 id="{slug(period)}">{esc(period)}</h3><ol class="period-pages">'+''.join(f'<li>{jump(p)}</li>' for p in paths)+'</ol></li>'
    for period,paths in TIMELINE)
tasks=[
 ('tax-first-year/index.html','Tax when you start work'),
 ('jobs/index.html','Work card'),
 ('social-security-card/index.html','Social Security'),
 ('health-cover/index.html','Medicaid and health cover'),
 ('benefits/index.html','Cash, food and other help'),
 ('green-card/index.html','Green card'),
 ('travel-document/index.html','Travel document'),
 ('naturalization/index.html','Citizenship')]
task_html=''.join(f'<li>{jump(p,label)}</li>' for p,label in tasks)
topics=''.join(
    f'<section class="topic"><h3 id="{slug(g)}">{esc(g)}</h3><ul class="link-grid">'+''.join(f'<li>{jump(p)}</li>' for p,_t in it)+'</ul></section>'
    for g,it in G)
body=f'''<h1>South African refugees coming to the USA: where are you in the journey?</h1>
<p class="home-cta">{intake_button()}<a class="guide-link" href="/online-intake/">Read our guide to the questionnaire first</a></p>
<p>A plain-language, factual guide for South Africans being processed through, or recently resettled by, the U.S. Refugee Admissions Program (USRAP). Open Start here for the pages in time order. Words such as USRAP are explained in the {L("glossary/index.html","glossary")}.</p>
<section class="path" aria-labelledby="{slug("Start here")}">
<h2>Start here</h2>
<p>These pages follow the journey in time order. Open the group that matches where you are.</p>
<ol class="timeline">{timeline}</ol>
</section>
<section class="tasks-wrap" aria-labelledby="{slug("Top tasks")}">
<h2>Top tasks</h2>
<p>The pages people need most often. Each link opens one page.</p>
<ul class="tasks">{task_html}</ul>
</section>
<div class="card note"><ul><li>The FY2026 refugee ceiling was raised from 7,500 to 17,500 by Presidential Determination 2026-14{src("pd26")}.</li><li>The FY2027 ceiling is up to 17,500 under Presidential Determination 2026-24{src("pd27")}.</li><li>Since 1 January 2026 the Office of Refugee Resettlement (ORR) runs initial resettlement{src("pir")}.</li></ul></div>
<div class="card warn"><strong>{NOTICE}</strong></div>
<section aria-labelledby="{slug("All topics")}">
<h2>All topics</h2>
<p>Every page on this guide, grouped by subject.</p>
{topics}
</section>'''
s.page('index.html',"South African refugees in the USA: a plain USRAP guide","Plain-language guide for South Africans in the U.S. Refugee Admissions Program: referral, arrival, benefits, health cover, work and the green card.",body,kind='home')

f='eligibility/index.html'
P(f,"USRAP eligibility and referral rules for South Africans","Who the U.S. Embassy in South Africa says can be considered for a USRAP referral, and how the intake questionnaire fits the process.",f'''<h1>Eligibility and referral</h1>
<h2>Who the Embassy says can be considered</h2><div class="card"><p>The U.S. Mission South Africa page (dated 7 October 2026) lists all of these criteria{src("emb")}:</p><ul><li>South African nationality</li><li>Afrikaner ethnicity, or a member of a racial minority in South Africa</li><li>Able to describe past persecution or fear of future persecution on account of race, religion, nationality, membership in a particular social group or political opinion</li><li>At least 18, or referred with a parent</li><li>Living inside South Africa; the programme does not expect out-of-country processing</li></ul></div>
<h2>How to ask for referral</h2><div class="card"><ul><li>If no USRAP partner has contacted you yet, complete the online {L("online-intake/index.html","USRAP Intake Questionnaire",f)}. This applies even if you sent an earlier Statement of Interest{src("emb")}.</li><li>The form the Embassy links is on a state.gov site: {a(S["uiq"],"USRAP Intake Questionnaire")}{src("emb")}.</li><li>Referral partners are RSC Africa (operated by Church World Service) and Amerikaners{src("emb","embfaq")}.</li><li>Not everyone is referred. The authority to grant access rests with the U.S. government, not with RSC Africa/CWS or Amerikaners{src("emb")}.</li><li>If accepted, next steps include a pre-screen interview, security vetting, a USCIS interview and a medical exam{src("embfaq")}.</li><li>There is no standard timeline. Case questions, once you have a case number: SouthAfrica@cwsafrica.org{src("embfaq")}.</li></ul></div>
<h2>Conflicts and gaps</h2><div class="card conf"><ul><li>The Embassy's 13 February 2025 notice says to email PretoriaPRMInfo@state.gov and that access is free{src("emb2025")}. The 7 October 2026 page does not mention that mailbox. It says you must complete the questionnaire, even after a Statement of Interest{src("emb")}. The October page does not say the email was "replaced". Follow the newer page, and read {L("online-intake/index.html","Online intake questionnaire",f)}.</li><li>The Presidential Determinations refer to Afrikaners from South Africa{src("pd26","pd27")}. The Embassy criteria also include a member of a racial minority{src("emb")}.</li><li>Processing time: not stated as one number. The Embassy FAQ says there is no standard timeline{src("embfaq")}.</li></ul></div>
<p>Next: read {L("avoiding-scams/index.html","Avoiding scams",f)} before you share documents or pay anyone.</p>''')

f='online-intake/index.html'
P(f,"USRAP online intake questionnaire for South Africans","What the official USRAP intake questionnaire is, who should submit it, what the Embassy says happens next, and why the form is free.",f'''<h1>Online intake questionnaire</h1>
<p class="home-cta">{intake_button()}</p>
<h2>What it is</h2><div class="card"><p>The U.S. Mission South Africa page (7 October 2026, U.S. Mission South Africa, marked as a 24 minute read) tells people who meet every eligibility rule, and who have not yet been contacted by a USRAP partner, to complete the online USRAP Intake Questionnaire if they want to be considered for referral{src("emb")}.</p>
<p>The Embassy's own link, checked on {D}, is {a(S["uiq"],"https://us-dos.unqorkgov.state.gov/?#/display/68a77f413cdb0fe7ab8817a8")}{src("emb")}. Do not use a look-alike site.</p>
<p>The same page says you must complete this questionnaire even if you already submitted a Statement of Interest on the old link, if you are still interested and a partner has not contacted you to act on that statement{src("emb")}.</p></div>
<h2>Who should submit it</h2><div class="card"><ul><li>People who meet all of the criteria on the {L("eligibility/index.html","eligibility page",f)}{src("emb")}.</li><li>People a USRAP partner has not yet contacted to start a referral or to process the case{src("emb")}.</li><li>A family group of one person still uses the family-group submit button. The Embassy FAQ says that{src("embfaq")}.</li></ul>
<p>Who may submit on behalf of someone else, and every question on the form: not stated by the Embassy pages. The Embassy says it is not necessary to have documents verified{src("emb")}.</p></div>
<h2>What the Embassy says happens after you submit</h2><div class="card"><ul><li>Your application is reviewed by a referring organisation, Church World Service (CWS) or Amerikaners. They may contact you if they need more information{src("embfaq")}.</li><li>The 7 October page says the Department of State's referral partners review submissions and may ask for more information. Because of the volume of interest, you may not get a response for an extended period{src("emb")}.</li><li>If you meet the qualifications for referral, the Bureau of Population, Refugees, and Migration (PRM) evaluates access to USRAP{src("embfaq")}.</li><li>Not everyone is referred. The U.S. government considers eligibility, the persecution claim and background checks. The authority to grant access rests with the U.S. government, not with RSC Africa/CWS or Amerikaners{src("emb","embfaq")}.</li><li>You are told whether you are referred or not{src("emb")}. If you are accepted, RSC Africa/CWS tells you the next steps: a pre-screen interview, security vetting, a USCIS interview and a medical exam{src("embfaq")}.</li><li>There is no standard or guaranteed timeline{src("embfaq")}.</li><li>Keep the email address you used on the form. If your address, email or phone changes after you are granted access, tell RSC Africa immediately{src("embfaq")}.</li><li>Case questions after processing has begun: write to SouthAfrica@cwsafrica.org and include your case number. You can track the case only after you have a case number{src("embfaq")}.</li></ul></div>
<h2>How to know the form went through</h2><div class="card"><p>The Embassy FAQ says to check the dashboard{src("embfaq")}:</p><ul><li>You should see "Information Entry Complete" in the status column next to each family member, after that person's form is finished.</li><li>Then select "Submit Family Group UIQ Application" at the bottom of the dashboard.</li><li>You should then see "Complete" under the Family Group UIQ Status.</li></ul>
<p>If you do not see those statuses, the FAQ says the family group was not submitted. Finish each person and submit the group again. That includes a family of one{src("embfaq")}.</p></div>
<h2>The form is free</h2><div class="card warn"><ul><li>Access to USRAP is free, including the questionnaire. Referral partners do not charge fees{src("emb")}.</li><li>The Embassy FAQ says referrals, applications and related services are free. Do not pay anyone who claims they can expedite the case or guarantee approval{src("embfaq")}.</li><li>The only official referral and USRAP implementers named in South Africa are RSC Africa/CWS and Amerikaners. Report fraud with the USRAP Tip Form on the Embassy page{src("emb","embfaq")}.</li></ul>
<p>Read {L("avoiding-scams/index.html","Avoiding scams",f)} before you pay anyone or hand over identity documents.</p></div>
<h2>February 2025 email and the October 2026 page</h2><div class="card conf"><p>The Embassy notice dated 13 February 2025 says: for more information contact PretoriaPRMInfo@state.gov; if you already wrote, they are reviewing messages; the programme is for consideration for refugee resettlement; access is free; report fraud to that same mailbox{src("emb2025")}.</p>
<p>The 7 October 2026 page does not mention PretoriaPRMInfo@state.gov. It says you must complete the questionnaire even if you already sent a Statement of Interest{src("emb")}. It does not use the word "replaced". Both pages are still on the Embassy site. Follow the newer page for how to ask for a referral.</p></div>''')

f='programme-status/index.html'
P(f,"Refugee programme status and the FY2026 to FY2027 caps","FY2026 and FY2027 refugee admission ceilings from the Federal Register, and which U.S. agencies run referral, interview and arrival.",f'''<h1>Programme status and caps</h1>
<h2>FY2026 (1 October 2025 to 30 September 2026)</h2><div class="card"><ul><li>Presidential Determination 2026-14 of 21 May 2026 raised the FY2026 ceiling from 7,500 (set by Presidential Determination 2025-13) to 17,500{src("pd26")}.</li><li>The additional admissions are allocated among Afrikaners from South Africa, consistent with Executive Order 14204{src("pd26")}.</li><li>Published 27 May 2026, 91 FR 31645{src("pd26")}.</li></ul></div>
<h2>FY2027 determination</h2><div class="card"><ul><li>Yes, there is one. Presidential Determination 2026-24 of 25 September 2026 authorises up to 17,500 refugee admissions in FY2027{src("pd27")}.</li><li>Admissions are "primarily" allocated among Afrikaners from South Africa under Executive Order 14204{src("pd27")}.</li><li>Published 2 October 2026{src("pd27")}.</li></ul></div>
<h2>Who runs what</h2><div class="card"><ul><li>The State Department identifies and refers applicants. USCIS interviews and checks them. CDC-approved doctors do the medical exam. CBP admits refugees at the port of entry. ORR starts services on arrival{src("roles")}.</li><li>ORR took over initial resettlement, now the Program of Initial Resettlement, on 1 January 2026{src("pir")}.</li><li>How to ask for a referral from South Africa is the {L("online-intake/index.html","online intake questionnaire",f)}, not an email to a private helper{src("emb")}.</li></ul></div>
<p class="src">How many places are left in FY2027: not stated by source.</p>''')

f='avoiding-scams/index.html'
P(f,"Avoiding scams in the USRAP refugee programme in 2026","The USRAP intake questionnaire is free. Embassy and USCIS warnings about fees, fake helpers, notarios and how to report fraud.",f'''<h1>Avoiding scams</h1>
<h2>The referral process is free</h2><div class="card warn"><ul><li>Access to USRAP is free, including the {L("online-intake/index.html","questionnaire",f)}. Referral partners do not charge fees{src("emb")}.</li><li>It is not necessary to have documents verified{src("emb")}.</li><li>Do not pay anyone who claims to expedite your case or guarantee approval. Only RSC Africa/CWS and Amerikaners are official referral and USRAP implementers in South Africa. Report fraud with the USRAP Tip Form on the Embassy pages{src("emb","embfaq")}.</li><li>The 13 February 2025 Embassy notice also says access is free and that no one should pay a fee or a favour for access or for a faster case{src("emb2025")}.</li></ul></div>
<h2>Pets are a common hook</h2><div class="card"><p>The Embassy says neither the U.S. government nor USRAP partners fund or arrange pet transport, and Embassy Pretoria is not working with any group to move pets. Beware of anyone who claims they are coordinating with the government to move a pet or to speed up the case{src("emb")}. Details are on {L("bringing-pets/index.html","Bringing your pets",f)}.</p></div>
<h2>After you arrive</h2><div class="card"><ul><li>USCIS will never ask you to send money to a person, or to pay by Western Union, gift cards or similar{src("scam")}.</li><li>Notarios are not authorised to give immigration legal services. Only an attorney or an accredited representative of a DOJ-recognised organisation can{src("scam")}.</li><li>USCIS forms are free to download from uscis.gov{src("scam")}.</li><li>Government email addresses end in .gov{src("scam")}.</li></ul></div>
<h2>Where to report</h2><p>Suspect immigration fraud: the Federal Trade Commission or your state consumer protection office{src("scam")}. Suspicious USCIS-style email: USCIS.Webmaster@uscis.dhs.gov{src("scam")}.</p>''')

f='bringing-pets/index.html'
P(f,"Bringing pets from South Africa to the USA: rules and time","CDC, USDA and South African rules for bringing a dog or cat to the USA, how long it takes, and what the Embassy says about refugee pets.",f'''<h1>Bringing your pets from South Africa to the USA</h1>
<div class="card warn"><p><strong>Refugees: the programme does not move or pay for pets.</strong> The Embassy page of 7 October 2026 says neither the U.S. government nor USRAP implementing partners assist in or fund pet transport. Embassy Pretoria is not working with any entity to move pets. Arrange pet travel yourself after you arrive. The Embassy recommends waiting at least 90 days, because the first housing may not allow pets, and no one in the programme will move the pet inside the United States{src("emb")}.</p>
<p>The Embassy FAQ answers "How do I arrange for my pet to join me?" in the same way: USRAP cannot fund or assist travel for pets or emotional-support animals, and it strongly discourages bringing pets until at least 90 days after the refugees arrive. Pets limit housing. Deposits and monthly pet rent cannot be paid from resettlement support. Later you may use a shipper. Not every animal can be admitted. The process can take a long time and cost a lot{src("embfaq")}.</p>
<p>Beware of anyone who says they are coordinating with the government to move a pet or to speed up your case. Report that on the USRAP Tip Form linked from the Embassy page{src("emb")}. See {L("avoiding-scams/index.html","Avoiding scams",f)}.</p></div>
<h2>How long it takes</h2>
<p>Count back from the <strong>dog's</strong> travel date. These figures are the ones CDC states for a foreign-vaccinated dog that has been in a high-risk rabies country. South Africa is on CDC's high-risk list{src("cdc_hr","cdc_fv")}. Where a page gives no time, this table says so. Do not use European or British export timetables for a trip to the United States. Those rules are not on the CDC or South African pages checked.</p>
<div class="wrap"><table>
<tr><th>When, counted back from the dog's travel date</th><th>What has to be true</th><th>Where it is stated</th></tr>
<tr><td>Before the rabies vaccine</td><td>A microchip that a universal scanner can read must already be in place. A vaccine given before the chip does not count. The chip number goes on the forms.</td><td>{a(S["cdc_fv"],"CDC foreign-vaccinated dogs")}</td></tr>
<tr><td>Dog's age on the day of entry</td><td>At least 6 months old. The dog must also appear healthy.</td><td>{a(S["cdc_fv"],"CDC foreign-vaccinated dogs")}</td></tr>
<tr><td>First valid rabies vaccine</td><td>At or after 12 weeks (84 days) of age. Vaccines before 12 weeks are not accepted for a dog that has been in a high-risk country in the prior 6 months. If it is the first vaccine, it must be given at least 28 days before entry.</td><td>{a(S["cdc_fv"],"CDC foreign-vaccinated dogs")}</td></tr>
<tr><td>At least 30 days after that first valid vaccine, and at least 28 days before entry</td><td>Blood draw for a rabies serology titer at a CDC-approved laboratory. If later valid boosters never lapsed, CDC allows a later draw. If coverage lapsed, wait at least 30 days after the new dose. A passing result stays valid for the life of the dog if coverage does not lapse and the lab stays approved.</td><td>{a(S["cdc_fv"],"CDC foreign-vaccinated dogs")}</td></tr>
<tr><td>Lab turnaround</td><td>Not stated as one number. CDC says the estimated turnaround time varies and tells you to ask the laboratory. CDC recommends talking to the vet about sending the sample at least 60 days or more before travel.</td><td>{a(S["cdc_labs"],"CDC-approved labs")}</td></tr>
<tr><td>60 days or more before travel</td><td>CDC's checklist calls this a recommended start: confirm the chip, make sure the vaccine will not expire, start the airline reservation if you have one, and draw blood if the first valid vaccine was already at least 30 days earlier. CDC does not call 60 days a legal minimum. It does not, by itself, cover a dog that still needs its first valid vaccine.</td><td>{a(S["cdc_fv"],"CDC checklist")}</td></tr>
<tr><td>30 days or more before travel</td><td>Last chance to draw blood, and the draw must still be at least 28 days before travel. Reserve a CDC-registered animal care facility. If you do not have a valid titer, the reservation has to include 28 days of quarantine. The reservation confirmation travels with the dog.</td><td>{a(S["cdc_fv"],"CDC checklist")}</td></tr>
<tr><td>No more than 30 days before travel</td><td>A vet completes the Certification of Foreign Rabies Vaccination and Microchip form. An official government veterinarian of the exporting country endorses it. It is valid for 30 days after the examining vet signs it, for one entry, and it must be printed for the airline and for CBP. CDC does not set one price. Ask the vet.</td><td>{a(S["cdc_fv"],"CDC certification form")}</td></tr>
<tr><td>South African state vet</td><td>How long the state vet takes, and a separate U.S. validity window for a South African certificate: not stated. The Department of Agriculture says that for exports other than its Namibia guide you contact your local state veterinarian. An older department PDF says a private vet cannot give the official certificate and the exporter pays the preparation costs.</td><td>{a(S["nda"],"Department of Agriculture")}, {a(S["dalrrd"],"older export PDF")}</td></tr>
<tr><td>The week of travel, or the day of travel</td><td>CDC says you may complete the CDC Dog Import Form on the day of travel and recommends doing it a few days before. If the date or airport changes, submit a new form. For a foreign-vaccinated dog from a high-risk country, the receipt is for one entry and only for the arrival date on the form. The instructions page says a high-risk receipt is valid for one dog, one time. The six-month receipt is only in the low-risk section. Do not use it for a dog from South Africa.</td><td>{a(S["cdc_fv"],"CDC foreign-vaccinated dogs")}, {a(S["cdc_form"],"CDC Dog Import Form instructions")}</td></tr>
<tr><td>Photo, if the dog is under 1 year</td><td>The instructions say the photo should be taken within 15 days before arrival.</td><td>{a(S["cdc_form"],"CDC Dog Import Form instructions")}</td></tr>
<tr><td>Airline booking</td><td>One book-by deadline for every airline: not stated by the pages checked. Florida says contact the airline as early as you can. Most airlines want a health certificate within 7 to 10 days of travel, and some will not accept one unless the exam was within 10 days. That varies. CDC does not state a general health certificate as its own requirement. States and airlines may ask for one.</td><td>{a(S["fdacs"],"Florida animal movement")}, {a(S["cdc_ani"],"CDC bringing an animal")}</td></tr>
<tr><td>After arrival</td><td>The dog must land at the airport where the CDC-registered facility is, the airport on the form receipt. No domestic onward travel until the exam and a U.S.-licensed rabies revaccination are done. The importer pays the facility. How long that visit takes when the titer is already valid: not stated. If there is no valid titer, quarantine can be 28 days. CDC says quarantine can be shortened if certain criteria are met. Those criteria are on CDC's FAQ. This page does not restate them.</td><td>{a(S["cdc_fv"],"CDC foreign-vaccinated dogs")}</td></tr>
</table></div>
<div class="card note"><p><strong>A realistic total, using only those figures.</strong> If the dog still needs its first valid vaccine, the earliest blood draw is 30 days later, and that draw must also be at least 28 days before entry. That is 58 days after the vaccine, and only if a CDC-approved lab returns a result CDC will accept in time. CDC does not publish one turnaround number{src("cdc_fv","cdc_labs")}. The dog must also be at least 6 months old on the day it enters{src("cdc_fv")}. If there is no valid titer, add 28 days of quarantine after arrival{src("cdc_fv")}.</p>
<p>That CDC clock is separate from the Embassy clock. The Embassy recommends at least 90 days after the person arrives before the pet travels, and the programme does not pay{src("emb","embfaq")}.</p></div>
<h2>Dogs: what CDC requires from a high-risk country</h2>
<div class="card"><ul>
<li>South Africa is on the high-risk countries list{src("cdc_hr")}.</li>
<li>Certification form, filled by a vet and endorsed by an official government veterinarian, completed no more than 30 days before travel{src("cdc_fv")}.</li>
<li>A valid rabies serology titer from a CDC-approved lab, or a reservation that includes 28-day quarantine{src("cdc_fv","cdc_labs")}.</li>
<li>A reservation at a CDC-registered animal care facility, and arrival at that airport{src("cdc_fv")}.</li>
<li>Microchip before the vaccine. The number is on every form{src("cdc_fv")}.</li>
<li>Appear healthy. At least 6 months old{src("cdc_fv")}.</li>
<li>Documents in English, or with a certified English translation{src("cdc_fv")}.</li>
<li>The CDC Dog Import Form is required for each dog. After you confirm the email, the receipt is emailed. The instructions say the verification message comes from 1cdpwebsurvey@cdc.gov and the receipt arrives within 15 minutes of the first submission. Show it to the airline and to CBP{src("cdc_form")}.</li>
<li>The CDC Dog Import Form is free{src("cdc_fv")}. The direct form address is on the CDC instructions page. This guide does not copy a second address{src("cdc_form")}.</li>
</ul></div>
<h2>Cats</h2>
<div class="card"><ul>
<li>CDC says a cat must appear healthy and can be inspected. It can be denied if there is evidence of a disease that spreads from animals to people. If the cat is ill, a vet exam at the owner's expense may be required{src("cdc_ani")}.</li>
<li>CDC does not require proof of rabies vaccination for cats. It recommends the vaccine. The destination state and the airline may require more. Hawaii and Guam have quarantine even for animals that come from the U.S. mainland{src("cdc_ani")}.</li>
<li>A CDC microchip rule or a CDC waiting period for cats: not stated on the cat page checked{src("cdc_ani")}.</li>
<li>USDA APHIS says it has no animal-health requirements for a pet cat. It tells you to check CDC, the Fish and Wildlife Service (FWS), and the destination state{src("aphis_cats")}.</li>
</ul></div>
<h2>USDA APHIS rules for dogs</h2>
<div class="card"><p>APHIS says CDC is the main authority for dog rabies rules. APHIS adds rules if a country is affected by foot-and-mouth disease (FMD) or screwworm{src("aphis_dogs")}.</p>
<ul>
<li>If the country is FMD-affected: fur and bedding free of excessive dirt, hay or straw; bathe the dog on arrival and keep it away from livestock for 5 days. APHIS does not require a document for that step{src("aphis_dogs")}.</li>
<li>If the country is screwworm-affected: a certificate, signed by a full-time salaried veterinary official of the region, that the dog was inspected within 5 days before shipment and is free of screwworm, or was infested, quarantined and treated until free. APHIS does not publish a template{src("aphis_dogs")}.</li>
<li>The disease-status page tells you to follow those rules if a country is "not free". On {D} that page did not name South Africa. This guide does not say South Africa is, or is not, FMD-affected or screwworm-affected. Check the lists{src("aphis_dis")}.</li>
</ul></div>
<h2>South Africa: the export certificate</h2>
<div class="card"><ul>
<li>The Department of Agriculture says that, apart from its Namibia guide, you contact your local state veterinarian about exports{src("nda")}.</li>
<li>A U.S.-specific validity window on that page: not stated{src("nda")}.</li>
<li>An older PDF still on the former department site says the provincial state vet certifies the importing country's health certificate if the requirements are met, a private vet cannot give official certification, and the exporter bears the preparation costs{src("dalrrd")}.</li>
<li>The document the government vet must endorse for CDC is the certification form above. It is a 30-day document. This guide does not invent a second South African expiry date{src("cdc_fv","nda")}.</li>
</ul></div>
<h2>Airline crate</h2>
<div class="card"><p>IATA is the airline industry body, not a government. Its pet page (Container Requirement 1) says only small dogs and cats may travel in the cabin, and some airlines will not allow that and use a heated, ventilated hold{src("iata")}.</p>
<ul>
<li>Measure A from nose to the base of the tail, B from the ground to the elbow, C across the shoulders or the widest point, and D as standing height to the top of the head or the ear tip, whichever is higher{src("iata")}.</li>
<li>Length is A plus half of B. Width is C times 2 (times 3 for two animals, times 4 for three). Height is D plus bedding. Snub-nosed breeds need a container 10 percent larger{src("iata")}.</li>
<li>Weaned puppies or kittens from the same litter, not older than 6 months, up to 14 kg each, up to three in one container. Two compatible adults up to 14 kg each may share. Heavier animals travel alone{src("iata")}.</li>
<li>IATA says to get the animal used to the crate a few weeks or months before the trip. It also says a light meal 2 hours before the animal is handed over is a legal requirement in the United States. That sentence is IATA's{src("iata")}.</li>
</ul></div>
<h2>If you are going to Florida</h2>
<div class="card"><p>These points are only for Florida. Other states differ. APHIS tells you to check the agriculture department of the state you are entering{src("aphis_dogs","fdacs")}.</p>
<ul>
<li>An official certificate of veterinary inspection is normally required within 30 days of issue. Florida lists exceptions, including a privately owned pet travelling with its owner{src("fdacs")}.</li>
<li>Dogs and cats 3 months and older that are brought into Florida, including privately owned pets with their owners, need proof of a current rabies vaccination from a licensed veterinarian{src("fdacs")}.</li>
<li>Inside Florida, dogs and cats 4 months and older need a current USDA-approved rabies vaccination{src("fdacs")}.</li>
</ul>
<p>A separate Florida notice about screwworm and travel between U.S. states is not a South Africa import rule. This page does not mix the two{src("fdacs")}.</p></div>
<h2 id="costs">Approximate costs</h2>
<div class="card warn"><p><strong>These are estimates only.</strong> Prices change often and are for information only. They are not quotes. Always get a written quote before you book. Last checked 24 October 2026. Amounts are shown in the currency each source uses. This guide does not convert rand (ZAR) to US dollars (USD), because the exchange rate changes daily.</p></div>
<p>Abbreviations: CDC is the US Centers for Disease Control and Prevention. A titer test is a rabies blood test that shows the vaccine worked. IATA is the International Air Transport Association, which sets crate rules. IPATA is the International Pet and Animal Transportation Association, a group of pet shipping agents.</p>
<div class="wrap"><table><tr><th>Item</th><th>ZAR</th><th>USD</th><th>Source</th></tr>
<tr><td>Rabies vaccine and microchip at a low-cost clinic (example: Brakpan SPCA)</td><td>Rabies R50, microchip R150, other dog vaccines R250</td><td>Not given</td><td>{a(S["brakpan_spca"],"Brakpan Herald, 15 Oct 2026")}</td></tr>
<tr><td>Private vet (example: The Parks Animal Care, Johannesburg)</td><td>Consult R595, vaccinations R765 (rabies included with core vaccines)</td><td>Not given</td><td>{a(S["parks_vet"],"The Parks Animal Care")}</td></tr>
<tr><td>Rabies titer test (needed for dogs from South Africa, a high-risk country)</td><td>Varies, ask your vet for a quote</td><td>Varies</td><td>{a(S["cdc_labs"],"CDC approved labs")}</td></tr>
<tr><td>Vet filling in the CDC vaccination form</td><td>Varies, ask your vet</td><td>Varies</td><td>{a(S["cdc_fv"],"CDC")}</td></tr>
<tr><td>CDC Dog Import Form</td><td>Free</td><td>Free</td><td>{a(S["cdc_fv"],"CDC")}</td></tr>
<tr><td>South African export health certificate and state vet endorsement</td><td>Varies, ask your local state vet. The exporter pays.</td><td>Not given</td><td>{a(S["nda"],"Department of Agriculture")}, {a(S["dalrrd"],"export PDF")}</td></tr>
<tr><td>CDC-registered animal care facility on arrival (dog, valid titer)</td><td>Not given</td><td>Gateway (Philadelphia) $500 plus airline fees $100 to $350. Pender (Washington Dulles) $996 plus airline fees $275 to $475.</td><td>{a(S["gateway"],"Gateway")}, {a(S["pender"],"Pender")}</td></tr>
<tr><td>Same facility, dog with no valid titer (up to 28 days quarantine)</td><td>Not given</td><td>Gateway $3,500. Pender $4,071.</td><td>{a(S["gateway"],"Gateway")}, {a(S["pender"],"Pender")}</td></tr>
<tr><td>Facility extras</td><td>Not given</td><td>Weekend or after-hours arrival: Gateway $300, Pender $350 to $750</td><td>{a(S["gateway"],"Gateway")}, {a(S["pender"],"Pender")}</td></tr>
<tr><td>Other CDC-registered facilities (Atlanta, Dallas, Los Angeles, Miami, New York JFK, Seattle)</td><td colspan="2">Varies, ask for a quote</td><td>{a(S["cdc_acf"],"CDC facility list")}</td></tr>
<tr><td>Qatar Airways, pet as checked baggage</td><td>Not given</td><td>Up to 32 kg (pet and crate): $350. 32 to 75 kg: $450. Heavier goes as cargo. No pets in the cabin.</td><td>{a(S["qatar_pets"],"Qatar Airways")}</td></tr>
<tr><td>Emirates</td><td colspan="2">From South Africa pets go as cargo (Emirates SkyCargo). Varies, ask for a quote. No pets in the cabin.</td><td>{a(S["emirates_pets"],"Emirates")}</td></tr>
<tr><td>Delta</td><td colspan="2">No pets in the cabin or as checked baggage to or from South Africa (limited exceptions for US military and State Department staff). Cargo only through a known shipper such as an IPATA agent. Varies, ask for a quote.</td><td>{a(S["delta_pets"],"Delta")}</td></tr>
<tr><td>United</td><td colspan="2">Does not carry pets to, from or through South Africa.</td><td>{a(S["united_pets"],"United")}</td></tr>
<tr><td>IATA-approved crate</td><td>Varies by size, ask a pet shop or agent for a quote</td><td>Varies</td><td>{a(S["iata"],"IATA")}</td></tr>
<tr><td>Pet relocation agent, South Africa to USA (door to door estimate)</td><td>Small (up to 10 kg) R55,000 to R85,000. Medium (10 to 25 kg) R70,000 to R100,000. Large (over 25 kg) R85,000 to R130,000.</td><td>Not given</td><td>{a(S["petport"],"PETport")}</td></tr>
</table></div>
<div class="card note"><p><strong>Example total for one dog</strong>, using only the published figures above. Items marked "varies" are not included, so your real total will be higher.</p><ul>
<li><strong>Low (you arrange it yourself, small dog, valid titer):</strong> about R200 (rabies and microchip at the SPCA) plus $350 (Qatar checked baggage) plus $1,271 (Pender with titer, lowest airline fee). That is about R200 plus $1,621, plus the titer test, state vet, crate and vet form, which vary.</li>
<li><strong>High (agent, large dog, no valid titer):</strong> R85,000 to R130,000 (agent estimate) plus up to $4,071 if the dog needs 28 days quarantine at Pender. Ask the agent what their quote already includes.</li></ul>
<p>Check the agent's quote for what is included, such as crate, titer test, state vet, flights and the US facility. Do not pay twice.</p></div>
<h2>Refugee flights</h2>
<div class="card"><ul>
<li>The only official USRAP travel booker the October 2026 Embassy page names is RSC Africa, operated by Church World Service. The Embassy prints {a("https://mycase.rscafrica.org/","https://mycase.rscafrica.org/")} as that partner's site. Travel booked by anyone else is not supported and can put your entry and initial help at risk{src("emb")}.</li>
<li>The same page does not name the International Organization for Migration as the office that books this programme's flights{src("emb")}.</li>
<li>Whether a particular RSC Africa ticket can include a pet: not stated. Ask RSC Africa, and ask your resettlement agency, before you assume the seat or the hold can take an animal{src("emb")}.</li>
<li>The {L("first-90-days/index.html","first 90 days",f)} service list from ORR does not mention pets{src("pir")}.</li>
<li>Costs are the family's. The Embassy says pet transport is not funded. CDC says the importer pays the animal-care facility. The older South African export note says the exporter pays preparation costs{src("emb","cdc_fv","dalrrd")}.</li>
</ul></div>''')

f='first-90-days/index.html'
P(f,"Your first 90 days after you arrive as a USRAP refugee","What the Office of Refugee Resettlement says a local provider arranges in the first period after you arrive, up to 90 days.",f'''<h1>First 90 days</h1>
<h2>Who helps you</h2><div class="card"><p>ORR coordinates placement and initial resettlement services up to 90 days through the Program of Initial Resettlement (PIR). Refugees are typically assigned a local resettlement provider{src("pir")}.</p>
<p>The Embassy FAQ describes that support as typically for 30 to 90 days, with limited help on housing, orientation and basic benefits{src("embfaq")}. ACF's page says up to 90 days and does not state a 30-day minimum{src("pir")}. The two pages use different wording. Read both.</p>
<p>PIR is delivered by eight organisations: Catholic Charities USA, Church World Service, Ethiopian Community Development Council, Global Refuge, HIAS, International Rescue Committee, U.S. Committee for Refugees and Immigrants, and World Relief{src("pir")}.</p></div>
<h2>What the provider helps with</h2><div class="card"><ul><li>Airport welcome</li><li>Temporary or longer-term housing with food, necessities, furnishings and household items (hotels may be used where housing is limited)</li><li>Personal case management and a resettlement plan</li><li>Connections to cash and medical assistance</li><li>Referrals for the domestic medical screening, jobs, social services and school enrolment</li></ul>{src("pir")}
<p>Pets are not on that list. The Embassy says the programme does not move pets and recommends waiting at least 90 days. See {L("bringing-pets/index.html","Bringing your pets",f)}{src("emb")}.</p></div>
<h2>Do these early</h2><ul><li>Sign up for benefits immediately: they are time-limited. See {L("benefits/index.html","Benefits checklist",f)}{src("ben")}.</li><li>Get the ORR-funded domestic medical screening soon after arrival{src("ben")}.</li><li>Check your {L("social-security-card/index.html","Social Security card",f)} arrives.</li><li>Keep your I-94 safe. It proves refugee status and work authorisation{src("ben","gc")}.</li>
<li>When you start a job, read {L("tax-first-year/index.html","Tax when you start work",f)}. That page is general information, not tax advice.</li></ul>''')

f='social-security-card/index.html'
P(f,"How refugees get a Social Security number and card","How refugees get a Social Security number and card, from the immigration record or at an SSA office, using the I-94 or an EAD.",f'''<h1>Social Security card</h1>
<h2>If you asked for an SSN during processing</h2><div class="card"><p>When a Social Security number is requested in the immigration process, DHS sends the data to SSA. SSA assigns the number and mails the card to the address you gave, or to your sponsoring agency if you had no address. The same rule says the card is sent within a reasonable time after the number is assigned. It does not give a number of days. That rule is 20 CFR 422.103, in the Code of Federal Regulations{src("ssncfr","ssnw")}.</p></div>
<h2>If you apply at an SSA office</h2><div class="card"><p>Staff follow the Program Operations Manual System (POMS){src("ssnr")}.</p><ul><li>SSA treats refugees as having permanent work authorisation and issues an unrestricted card (no legend){src("ssnr")}.</li><li>One document can prove age, identity and status, for example the I-94 website printout with the State Department transportation boarding letter carrying the refugee admission stamp{src("ssnr")}.</li><li>An I-94 with the refugee admission stamp, or an EAD with category A3, is also accepted{src("ssnr")}.</li></ul></div>
<h2>Lost card or stolen number</h2><p>Replacement and identity theft options are on {a(S["ssa"],"SSA's Social Security number page")}{src("ssa")}.</p>
<p class="src">A number of days for the card to arrive: not stated. The regulation says only that the card is sent within a reasonable time.</p>''')

f='benefits/index.html'
P(f,"A benefits checklist for refugees in the first year","A checklist of refugee cash, medical, food and job help from ORR, including the 4-month versus 12-month conflict in the sources.",f'''<h1>Benefits checklist</h1>
<h2>Sign up now</h2><div class="card warn">ORR says sign up immediately. Cash and medical help are limited to a period from your ORR eligibility date{src("ben")}.</div>
<h2>Checklist</h2><div class="card"><ul>
<li><strong>Bring proof:</strong> I-94 showing admission under section 207 of the Immigration and Nationality Act (INA), or I-94 code Visa 93, or an EAD with code A03{src("ben")}.</li>
<li><strong>Mainstream benefits:</strong> you may be eligible for TANF, SSI, Medicaid or SNAP{src("ben")}.</li>
<li><strong>Refugee Cash Assistance (RCA):</strong> if you are not eligible for TANF or SSI. Up to 12 months for an ORR eligibility date on or after 1 January 2026{src("dcl","frrma")}.</li>
<li><strong>Matching Grant:</strong> an alternative to TANF or RCA with limited slots, and a 240-day service period{src("ben")}.</li>
<li><strong>Refugee Medical Assistance (RMA):</strong> see {L("health-cover/index.html","Health cover",f)}.</li>
<li><strong>Domestic medical screening</strong> soon after arrival{src("ben")}.</li>
<li><strong>Refugee Support Services:</strong> jobs, English, childcare, transport, interpreting and case management, up to 5 years{src("ben")}.</li></ul></div>
<h2>Where to apply</h2><p>Your state benefits office or nearest resettlement agency. For local providers, contact your {L("agency-not-helping/index.html","State Refugee Coordinator",f)}{src("ben","src")}.</p>
<h2>Conflict between sources</h2><div class="card conf">The ACF benefits fact sheet (page dated 9 October 2026) still says four months of RCA and RMA for an eligibility date on or after 5 May 2025{src("ben")}. ORR's Dear Colleague Letter 26-05 (revised 1 October 2026) and the Federal Register correction say up to 12 months for an eligibility date on or after 1 January 2026{src("dcl","frrma")}. The newer policy letter appears to govern. Confirm with your provider.</div>''')

f='health-cover/index.html'
P(f,"Health cover for refugees in 2026: RMA versus Medicaid","How Refugee Medical Assistance compares with Medicaid in 2026, including ORR's letter that RMA can last up to 12 months.",f'''<h1>Health cover: RMA versus Medicaid</h1>
<h2>Refugee Medical Assistance (RMA)</h2><div class="card"><ul><li>RMA is for people who are not eligible for Medicaid. ORR says it provides the same coverage as Medicaid{src("ben")}.</li><li>From 1 October 2026, ORR provides up to 12 months of RMA for people whose ORR eligibility date is on or after 1 January 2026{src("dcl","frrma")}.</li><li>The letter gives states up to 30 days from 1 October 2026 to put the change into practice{src("dcl")}.</li><li>Conditions include not being eligible for Medicaid and meeting income and resource rules{src("dcl")}.</li></ul></div>
<h2>Medicaid</h2><div class="card"><ul><li>The ACF fact sheet says refugees may be eligible for Medicaid{src("ben")}.</li><li>ORR's letter cites reduced access to other benefits as a reason reliance on ORR assistance is rising{src("dcl")}.</li><li>Exactly how refugee Medicaid eligibility changed on 1 October 2026: not stated by the Administration for Children and Families pages or the Federal Register notice linked on this page. The Embassy FAQ, quoted on the {L("faq/index.html","common questions",f)} page, says Medicaid is typically available once you are a lawful permanent resident. Ask your state Medicaid office or resettlement provider.</li></ul></div>
<h2>What to do</h2><ul><li>Apply for health cover straight away through your resettlement provider or state benefits office{src("ben")}.</li><li>Already enrolled in RMA? Ask how the 12-month period under the 1 October 2026 letter applies to you{src("dcl")}.</li><li>Problems: contact the State Refugee Health Coordinator on {a(S["src"],"ACF's state contacts list")}{src("src")}.</li></ul>
<div class="card conf">Conflict: the ACF fact sheet still lists four months of RMA{src("ben")}, while the October 2026 letter says up to 12 months{src("dcl")}.</div>''')

f='jobs/index.html'
P(f,"Jobs, the EAD and Form I-9 for newly arrived refugees","Refugees may work from the day they arrive. What USCIS says about the EAD, Form I-9 and the I-94, plus free job help from ORR.",f'''<h1>Jobs and employment services</h1>
<h2>Your right to work</h2><div class="card"><ul><li>Refugees may work immediately on arrival{src("gc")}.</li><li>USCIS creates a digital Form I-765 for principal refugees and family who arrive with them. You should receive the Employment Authorization Document (EAD) within a few weeks after you arrive, depending on delivery times{src("gc")}.</li><li>For Form I-9, your I-94 is acceptable for 90 days after arrival. After that, show an unexpired EAD or other documents such as a driver's licence plus an unrestricted Social Security card{src("gc")}.</li><li>There is no fee for an initial or renewal refugee EAD in category (a)(3){src("gc")}.</li></ul></div>
<p>A job also raises tax questions. If you were an employee in South Africa, start with {L("tax-first-year/index.html","Tax when you start work",f)}. That page is general information, not tax advice.</p>
<h2>Free employment help</h2><div class="card"><ul><li>Refugee Support Services include job training, search, placement and retention, English classes, childcare and transport, for up to 5 years{src("ben")}.</li><li>RCA is provided alongside employment services through your provider{src("ben")}. Detailed participation rules: not stated by the pages checked.</li><li>Matching Grant is intensive case management and job help, aiming at self-sufficiency within 240 days{src("ben")}.</li></ul></div>
<h2>Watch for job scams</h2><p>Be wary of overseas or email job offers that ask for money{src("scam")}. See {L("avoiding-scams/index.html","Avoiding scams",f)}.</p>''')

f='agency-not-helping/index.html'
P(f,"What to do when your resettlement agency is not helping","What to do if your resettlement provider is not helping: the grievance process, your State Refugee Coordinator, and ORR's email.",f'''<h1>When your agency is not helping</h1>
<h2>Step 1: use the provider's grievance process</h2><div class="card">ORR requires programmes to have grievance policies so you can raise concerns, and says it reviews complaints with the implementing organisations{src("pir")}. The Embassy FAQ also says each local provider has a grievance policy and should explain it when you arrive{src("embfaq")}.</div>
<h2>Step 2: contact your State Refugee Coordinator</h2><div class="card"><p>ACF publishes a State Refugee Coordinator and a State Refugee Health Coordinator for each state, with email and phone{src("src")}. Find yours on {a(S["src"],"ACF Key State Contacts")}. They can also give a list of providers in your area{src("ben")}.</p></div>
<h2>Step 3: ORR</h2><div class="card">ORR's Program of Initial Resettlement contact is DRSAPrograms@acf.hhs.gov{src("pir")}.</div>
<h2>Gaps</h2><p class="src">Response times for complaints: not stated by source. Contact names change. Check the ACF page (dated 18 September 2026){src("src")}.</p>''')

f='travel-document/index.html'
travel_faqs=[
("Can I leave the USA while I am a refugee?",
 f'<p>USCIS does not say every trip is forbidden. It does say you need a refugee travel document before you leave, and that travel back to the country you fled can put your status at risk. Do not leave on a South African passport. Speak to an immigration attorney or an accredited representative before you buy a ticket. Read the {a(S["i131i"],"Form I-131 instructions")} and the {a(S["td"],"USCIS travel documents page")}.</p>'),
("Can I use my South African passport?",
 f'<p>No. The USCIS guide says refugees cannot get a passport from the country of nationality, and that the refugee travel document is the substitute. The Adjudicator\'s Field Manual says that, unless there is proof to the contrary, a refugee who obtains a national passport or renews one is presumed to have intended to use that country\'s protection again. See the {a(S["guide"],"USCIS refugee and asylee guide")} and the {a(S["afm"],"field manual chapter")}.</p>'),
("Can I go back to South Africa?",
 f'<p>Do not treat a trip to South Africa as safe. The USCIS guide says that if travel suggests you no longer need protection, refugee or asylee status may be terminated, and that going back to the country of past persecution or feared persecution can be used as evidence. A short stay for a compelling reason is described only as a limited possibility, not as a general permission. There is no absolute ban on issuing a travel document for that trip, but the same chapter says the trip may block a green card under section 209 of the Immigration and Nationality Act. Ask a lawyer. Sources: the {a(S["guide"],"USCIS guide")} and the {a(S["afm"],"field manual chapter")}.</p>'),
("When do I apply?",
 f'<p>Before you leave, and before any biometrics appointment USCIS requires. If you leave first, USCIS may, in its discretion, accept Form I-131 within 1 year of the last departure if you explain why you did not apply before you left. That is not a right. See the {a(S["i131i"],"Form I-131 instructions")}.</p>'),
("How long is the document valid?",
 f'<p>The Form I-131 instructions say a refugee travel document is valid for 1 year and that the validity date cannot be extended. The USCIS guide says it is valid for 1 year, or until refugee or asylee status expires, whichever comes first. Both sentences are on official pages. USCIS will not issue a new one while an old one is still valid unless you return it or show it was lost or destroyed. See the {a(S["i131i"],"instructions")} and the {a(S["guide"],"guide")}.</p>'),
("How long does USCIS take?",
 f'<p>A single processing time for a refugee travel document is not stated on the pages checked for this guide. Use the {a(S["ptime"],"USCIS processing times tool")} and select your form and office there. Do not rely on a number quoted from a grouped travel-document table.</p>'),
("What if my Form I-485 is pending?",
 f'<p>The Form I-131 instructions say USCIS generally treats a pending Form I-485 as abandoned if you leave without an advance parole document. The exceptions named there are H-1 and H-4, L-1 and L-2, K-3 and K-4, and V visas, not refugee status. The instructions do not say that a refugee travel document stops that abandonment. Ask a lawyer before you travel with a pending I-485. See the {a(S["i131i"],"Form I-131 instructions")}.</p>'),
("Does a trip pause the one-year green card clock?",
 f'<p>Yes. Time outside the United States does not count. The Policy Manual says the one year is physical presence at the time the green card application is decided, and that a refugee who travels in the first year meets the rule only when the days inside the United States add up to at least one year. See {a(S["pm7"],"USCIS Policy Manual, Volume 7, Part L, Chapter 2")}.</p>'),
("What happens at the airport when I come back?",
 f'<p>The Form I-131 instructions say a DHS officer at the port of entry decides whether you may be admitted when you present the refugee travel document. The USCIS guide says people who arrive without a foreign passport can be sent by U.S. Customs and Border Protection to secondary inspection for a paper I-94. A separate CBP page for refugee re-entry was not found in the sources checked for this guide. See the {a(S["i131i"],"instructions")} and the {a(S["guide"],"guide")}.</p>')]
P(f,"Can refugees leave the USA? The I-131 travel document","A plain answer on leaving the USA as a refugee: the I-131 travel document, the South African passport risk, and the green card clock.",f'''<h1>Can refugees leave the USA? Travel and the refugee travel document (I-131)</h1>
<div class="card warn"><p><strong>Short answer.</strong> Do not leave on your South African passport, and do not go back to South Africa, while you are a refugee. USCIS says you must apply for a refugee travel document, and attend biometrics if they are required, before you leave. Travel that looks as if you no longer need protection can put refugee status at risk. A trip in the first year also pauses the one-year physical-presence clock for the green card.</p>
<p>Speak to an immigration attorney or an accredited representative before any travel, including a trip that seems short. This page is general information, not advice about your case. The {L("disclaimer/index.html","disclaimer",f)} says the same.</p></div>
<h2>Do not use a South African passport or return to South Africa</h2>
<div class="card"><ul>
<li>The USCIS guide says refugees and asylees were given protection because they are fleeing the country of nationality, so they cannot acquire a passport from that country. The refugee travel document, also called Form I-571, is the substitute. It looks similar to a U.S. passport{src("guide")}.</li>
<li>The same guide says: if your travel abroad suggests that you no longer need the protection of the United States, your status as a refugee or asylee may be terminated. Returning to the country of past persecution or of feared future persecution may have to be explained when you come back, and it can be evidence that the fear is not genuine or that protection is no longer needed{src("guide")}.</li>
<li>A short stay for compelling reasons is described only as a limited circumstance, not as permission to go home for a holiday{src("guide")}.</li>
<li>The guide's later answer about losing status after a green card is written about permanent residence based on asylum. It does not say the same sentence about a green card based on refugee status. That point is not stated for refugee green cards{src("guide")}.</li>
<li>The instructions include a warning that cites section 208(c)(2)(D) of the Immigration and Nationality Act for asylees who applied on or after 1 April 1997. That warning is written for asylees. This page does not treat it as the refugee rule{src("i131i")}.</li>
</ul></div>
<div class="card"><p>USCIS still publishes an Adjudicator's Field Manual chapter on refugee travel documents. The current Policy Manual part is linked beside it. Read both, and ask a lawyer if they do not say the same thing{src("afm","pm11")}.</p><ul>
<li>Three things have to be shown before USCIS treats you as having gone back to the old country's protection: you acted voluntarily, you intended to obtain that protection, and you actually obtained it{src("afm")}.</li>
<li>Unless there is proof to the contrary, a refugee who applies for and obtains a national passport, or a renewal, is presumed to have intended to use that country's protection. Getting a birth record or a marriage record is not treated as that{src("afm")}.</li>
<li>Having a valid travel document from the country of nationality can make Form I-131 deniable{src("afm")}.</li>
<li>There is no absolute prohibition on issuing a refugee travel document for travel to the country of nationality or last residence. The same chapter says that travel may stop you establishing eligibility for permanent residence under section 209, and that each case is judged on its facts. Visiting a sick parent is weighed differently from regular holiday or business trips{src("afm")}.</li>
</ul>
<p>Passport logistics, such as how an SA passport is renewed abroad, are a different question. They are on {L("sa-passport-citizenship/index.html","SA passport and citizenship risks",f)}.</p></div>
<h2>Apply before you leave, and attend biometrics</h2>
<div class="card"><ul>
<li>If you are in the United States in valid refugee status, you must apply for the refugee travel document before you leave{src("i131i")}.</li>
<li>If biometrics are required, you must appear for them before you leave. If you do not appear, USCIS may deny the application{src("i131i")}.</li>
<li>Applicants aged 14 to 79 who apply for a refugee travel document may have to give biometrics at an Application Support Center. If you are already abroad, that may be at a U.S. embassy, consulate or USCIS office. USCIS tells you where{src("i131i")}.</li>
<li>Leaving before USCIS decides usually does not affect the decision. Leaving before biometrics are collected may cause a denial{src("i131i")}.</li>
<li>You can ask, when you file, for the document to be sent to a U.S. embassy, consulate or USCIS office abroad for pickup. Not every post can do that{src("i131i")}.</li>
<li>If you are already outside, USCIS may in its discretion allow Form I-131. You must file within 1 year of your last departure and include an explanation of why you did not apply before you left. USCIS decides whether to accept it{src("i131i")}.</li>
<li>Part 6 of the form asks for the country your refugee status is based on, whether you plan to travel there, whether you have returned, and whether you have received a benefit, a travel document, a passport or a re-entry permit since admission. It also asks about a new nationality or refugee status in another country{src("i131i")}.</li>
</ul></div>
<div class="card"><ul>
<li>File Form I-131. The USCIS form page says a refugee travel document (Part 1, box 2 or 3) cannot be filed online. File by mail{src("i131")}.</li>
<li>USCIS changed the I-131 filing location on 7 October 2026, with a grace period for forms postmarked by 9 November 2026. The instructions say to use the filing-addresses page, because a form sent to the wrong place can be rejected or delayed{src("i131","i131i","i131addr")}.</li>
<li>Do not put Form I-131 in the same envelope as Form I-485{src("gc")}.</li>
<li>Form G-1055, the fee schedule, lists a filing fee of $0 for a refugee travel document if you now hold refugee status in the United States, or if you are a lawful permanent resident as a direct result of refugee status. The instructions point you to that schedule{src("g1055","i131i")}.</li>
</ul></div>
<h2>How long USCIS takes</h2>
<div class="card"><p>A processing time for this document is not stated on the USCIS pages this guide quotes. Check the {a(S["ptime"],"USCIS processing times tool")} for Form I-131 at the office that has your case{src("ptime")}.</p>
<p>Do not copy a single number from a historic table that groups every kind of travel document together. That is not a refugee travel document time, and this page does not quote one.</p></div>
<h2>How long the document is valid</h2>
<div class="card conf"><ul>
<li>The Form I-131 instructions, dated 13 May 2026 in the file, say a refugee travel document is valid for 1 year and that the validity date cannot be extended{src("i131i")}.</li>
<li>The USCIS guide says it is valid for 1 year, or until refugee or asylee status expires, whichever comes first{src("guide")}.</li>
<li>Both are official. They do not use the same sentence. Show both to a lawyer before you plan a trip near the end of the year.</li>
<li>USCIS will not issue another one while the current one is still valid, unless the old one is returned or you show it was lost or destroyed{src("i131i")}.</li>
<li>USCIS will not issue one for travel to an area if a Federal Register notice bars that document for that area{src("i131i")}.</li>
</ul></div>
<h2>Before the green card, and while Form I-485 is pending</h2>
<div class="card warn"><ul>
<li>If you have refugee or asylee status and you are not a lawful permanent resident, you must have a refugee travel document to re-enter, unless you have an advance parole document{src("i131i")}.</li>
<li>The USCIS travel documents page says the same for a derivative refugee, and says that leaving without the document may mean you cannot re-enter or that you are placed in removal proceedings{src("td")}.</li>
<li>If you have filed Form I-485 and you leave without an advance parole document, USCIS generally treats the I-485 as abandoned. The exceptions in the instructions are only H-1 and H-4, L-1 and L-2, K-3 and K-4, and V visas. Refugee status is not in that list{src("i131i")}.</li>
<li>The instructions do not say that a refugee travel document stops an I-485 being treated as abandoned. Do not assume it does. Ask a lawyer before you travel with a pending I-485{src("i131i")}.</li>
</ul>
<p>The green card steps themselves are on {L("green-card/index.html","Green card after 1 year",f)}.</p></div>
<h2>The one-year green card clock and naturalisation</h2>
<div class="card"><p><strong>Green card.</strong> Refugees must have 1 year of physical presence in the United States when the adjustment application is decided, not merely one year after the admission date on paper. Only days inside the United States count. If you travel during that first year, you meet the rule only when the time inside adds up to at least 1 year{src("pm7")}.</p>
<ul>
<li>A principal refugee, and a derivative refugee admitted from abroad, starts counting on the date of admission as a refugee{src("pm7")}.</li>
<li>A derivative who was already in the United States and who gained status through an approved Form I-730 starts on the date that petition was approved{src("pm7")}.</li>
</ul>
<p>The public green card page also says you must be physically present for at least 1 year after admission when you file{src("gc")}. The Policy Manual stresses the date of the decision and the days you were actually here{src("pm7")}. Read both before you travel in year one.</p></div>
<div class="card"><p><strong>Naturalisation is a later clock, and for a refugee it reaches back to admission.</strong> Continuous residence under the general rule is at least 5 years as a lawful permanent resident before you file, and you must also have lived in the state or service district for 3 months before you file{src("pm12")}.</p>
<p>A refugee is generally a lawful permanent resident as of the date of entry into the United States, once adjustment is approved. That date is earlier than the day USCIS approves the green card. A derivative who was already in the United States when the relative petition was approved uses the petition approval date instead{src("pm12d2","pm7l5")}. A trip in that period can fall inside the 5-year count. The full rules, including physical presence, are on {L("naturalization/index.html","Naturalisation after 5 years",f)}.</p>
<ul>
<li>Continuous residence and physical presence are separate requirements. The continuous-residence chapter does not state how many months of physical presence are required{src("pm12")}. The physical-presence chapter requires at least 30 months, which it also states as at least 913 days, before filing under the general provision{src("pm12d4")}.</li>
<li>An absence of 6 months or less does not, by itself, break continuous residence. Several shorter trips can still be reviewed{src("pm12")}.</li>
<li>More than 6 months but less than 1 year is presumed to break it. You can try to rebut that, for example if U.S. employment was not ended and you did not take a job abroad, if immediate family stayed, and if you still owned or leased a home{src("pm12")}.</li>
<li>One year or more breaks continuous residence unless Form N-470 is approved for qualifying employment abroad{src("pm12")}.</li>
<li>An approved N-470 does not remove the physical-presence requirement, except for certain U.S. government work or religious duties described in that chapter{src("pm12")}.</li>
</ul>
<p>Once you have a green card, the Form I-131 instructions give a separate warning: if a permanent resident who obtained that status because of refugee or asylee status does not get a re-entry permit, lengthy or frequent absences can support a finding that permanent residence was abandoned{src("i131i")}. A re-entry permit and Form N-470 are different forms. The pages checked do not say one replaces the other.</p></div>
<h2>Coming back through a port of entry</h2>
<div class="card"><ul>
<li>The refugee travel document lets you seek admission. It does not guarantee it. A DHS officer at the port of entry decides admissibility when you present it{src("i131i")}.</li>
<li>The USCIS guide says people without a foreign passport are sent by U.S. Customs and Border Protection (CBP) to secondary inspection, where a paper I-94 is issued{src("guide")}. The guide is describing arrival without a foreign passport. It does not say that presenting a refugee travel document skips inspection.</li>
<li>A separate page on cbp.gov for this return was not found in the sources checked. This guide does not invent a CBP link. The sentences above are USCIS sentences that name CBP and the port-of-entry officer{src("guide","i131i")}.</li>
<li>The document is invalid if it was obtained by a material false representation or concealment, if you are ordered removed, or if the 1951 Refugee Convention ceases to apply to you under Articles 1C, D, E or F{src("i131i")}.</li>
</ul></div>
<h2>Typical traps</h2>
<div class="card"><ul>
<li>Travelling on a South African passport, or renewing one, and treating that as harmless{src("guide","afm")}.</li>
<li>Going back to South Africa for a holiday, a funeral or business without legal advice{src("guide","afm")}.</li>
<li>Leaving before the biometrics appointment{src("i131i")}.</li>
<li>Leaving with a pending I-485 because you hold, or expect, a refugee travel document{src("i131i")}.</li>
<li>Taking a trip in the first year and still filing the green card on the one-year anniversary of arrival{src("pm7")}.</li>
<li>Assuming the document can be extended. The instructions say the validity date cannot be extended{src("i131i")}.</li>
<li>Filing online, or putting the I-131 in the I-485 envelope, or using an old filing address after 7 October 2026{src("i131","gc")}.</li>
<li>Applying from abroad and expecting approval. That path is discretionary, and only within 1 year of the last departure{src("i131i")}.</li>
<li>Asking a U.S. post abroad to hold the document when that post does not offer the service{src("i131i")}.</li>
</ul></div>''',travel_faqs)

f='sa-passport-citizenship/index.html'
P(f,"SA passport and citizenship risks for refugees in the USA","Why USCIS says using a South African passport or returning to South Africa can put refugee status at risk, and where to read SA rules.",f'''<h1>SA passport and citizenship risks for refugees</h1>
<div class="card warn"><p>Using a South African passport, or travelling to South Africa, can put U.S. refugee status at risk. The detail, including the green card effect, is on {L("travel-document/index.html","Can I leave the USA?",f)}. Speak to an immigration attorney or an accredited representative before you renew a passport or book a trip.</p></div>
<h2>What U.S. official sources say</h2><div class="card"><ul>
<li>The USCIS guide says refugees and asylees cannot acquire a passport from the country of nationality. The refugee travel document is the substitute{src("guide")}.</li>
<li>The same guide says travel that suggests you no longer need protection may lead to termination of refugee or asylee status, and that a return to the country you fled can be evidence that protection is no longer needed{src("guide")}.</li>
<li>The Adjudicator's Field Manual says that, unless there is proof to the contrary, obtaining a national passport or renewing one is presumed to mean you intended to use that country's protection. Birth and marriage records are not treated that way. Travel to that country may also block permanent residence under section 209 of the Immigration and Nationality Act{src("afm","pm11")}.</li>
<li>A refugee who is not yet a permanent resident needs a refugee travel document to return, unless they have an advance parole document{src("i131i","td")}.</li>
<li>Your refugee status must not have been terminated when you apply for a green card{src("gc")}.</li>
</ul></div>
<h2>The effect is not "unknown"</h2>
<div class="card"><p>An earlier version of this page said the effect of an SA passport, or of travel to South Africa, was not stated. That is no longer correct. USCIS states the risk in the guide and in the field manual chapter linked above. What those pages do not do is decide your own facts. That is why you need a lawyer before you act.</p></div>
<h2>South African passports and citizenship</h2>
<div class="card"><p>For how an SA passport or identity document is renewed from the USA, see the separate {a(PP,"SA Passport and ID Guide (USA)")}. For questions about keeping South African citizenship, see its {a(PPC,"citizenship page")}. Those are independent guides about South African logistics. They are not U.S. immigration advice, and they are not official sources.</p>
<p>The South African Department of Home Affairs publishes civic services, including passports, on its own site{src("dha")}.</p></div>''')

f='green-card/index.html'
P(f,"Refugee green card after 1 year: Form I-485 steps for 2026","USCIS steps for a refugee green card on Form I-485 after one year of physical presence, including fees, family and travel.",f'''<h1>Green card after 1 year (I-485)</h1>
<h2>You must apply</h2><div class="card"><p>U.S. law requires refugees to apply for a green card, which is lawful permanent resident status, after at least 1 year of physical presence{src("gc")}.</p>
<p>Travel outside the United States during that year does not count as presence. The Policy Manual says the year is measured when USCIS decides the application, and that only days in the United States count. Read {L("travel-document/index.html","Can I leave the USA?",f)} before you travel{src("pm7")}.</p></div>
<h2>Eligibility</h2><div class="card"><ul>
<li>Admitted as a refugee under section 207 of the Immigration and Nationality Act{src("gc")}.</li>
<li>Physically present in the United States when you file, and for at least 1 year after admission, on the public green card page{src("gc")}.</li>
<li>The Policy Manual requires 1 year of physical presence at the time of the decision, not only one calendar year from admission. A trip means you wait until the days inside add up to a year{src("pm7")}. The two USCIS pages do not use the same sentence. Show both to your lawyer or accredited representative.</li>
<li>Refugee status not terminated, and you are not already a permanent resident{src("gc")}.</li>
<li>Admissible, or eligible for a waiver on Form I-602{src("gc")}.</li>
</ul></div>
<h2>What to send (principal applicant)</h2><div class="card"><ul>
<li>Form I-485. Principal refugees pay no filing fee and no biometrics fee{src("gc")}.</li>
<li>Proof of refugee admission, such as the I-94, evidence of 1 year of presence, two passport-style photos, photo identification, and a birth certificate if you have one{src("gc")}.</li>
<li>The vaccination record part of Form I-693{src("gc")}.</li>
<li>Form I-602, if you need a waiver{src("gc")}.</li>
</ul></div>
<h2>Family members</h2><div class="card"><p>Derivative spouses and children follow similar rules. The green card page tells a derivative to use the fee schedule and does not print a dollar amount for that person{src("gc")}.</p><p>Form G-1055, the USCIS fee schedule, lists a filing fee of $0 if you are a refugee or you were paroled as a refugee. That row does not split a principal from a family member. The schedule is in the <a href="/about/#src-g1055">source list</a>.</p></div>
<h2>If you need to travel</h2>
<div class="card warn"><p>Do not leave while the I-485 is pending until a lawyer has told you which document, if any, keeps the application alive. The Form I-131 instructions say leaving without advance parole generally abandons a pending I-485, and they do not say a refugee travel document prevents that{src("i131i")}.</p>
<p>Do not put Form I-131 in the same envelope as Form I-485{src("gc")}. The travel page is {L("travel-document/index.html","Can I leave the USA?",f)}.</p></div>
<h2>After the green card</h2>
<div class="card"><p>Naturalisation uses a different form, Form N-400. Once adjustment is approved, a refugee is generally a lawful permanent resident as of the date of entry into the United States, so the general 5-year count uses that earlier date{src("pm12d2","pm7l5")}. You generally must already be a permanent resident when you file{src("pm12d2")}. The steps are on {L("naturalization/index.html","Naturalisation after 5 years",f)}.</p></div>''')

f='naturalization/index.html'
n400_faqs=[
("When does the 5-year clock start for a refugee?",
 f'<p>Once USCIS approves adjustment, a refugee is generally a lawful permanent resident as of the date of entry into the United States, not as of the approval date. A derivative who was already in the United States when the relative petition was approved uses that approval date instead.{src("pm12d2","pm7l5")}</p><p>You generally must already be a permanent resident on the day you file Form N-400.{src("pm12d2")}</p>'),
("Can I file 90 days early?",
 f'<p>Yes, for the continuous-residence part of the general 5-year rule. USCIS counts 90 days back from the day before you would first meet the 5 years. You are not eligible to be naturalised until those 5 years are complete.{src("pm12d6","n400")}</p><p>The early-filing chapter does not say those 90 days reduce the physical-presence requirement. The public page asks for at least 30 months of physical presence in the 5 years immediately before the date you file.{src("n400five","pm12d4")}</p>'),
("What if the date on the green card looks wrong?",
 f'<p>The card shows the date of lawful permanent resident status and the class of admission. For an approved refugee adjustment, the policy manual sets that date as the date of first admission as a refugee, with the derivative exception above.{src("pm12d2","pm7l5")}</p><p>How to correct a card that prints a different date: not stated by the pages checked. Ask an immigration attorney or an accredited representative before you file.</p>'),
("Do men have to register for Selective Service?",
 f'<p>The Selective Service chart says yes for refugee, parolee and asylee immigrants, in the group of male immigrants ages 18 through 25. Registration is not enlistment in the military.{src("ssschart","sssfaq")}</p><p>As of 30 June 2026, Selective Service no longer issues the status information letter that the USCIS form page and Policy Manual still name. Read the conflict on this page before you assume a letter is available.{src("sssfaq","n400","pm12d7")}</p>'),
]
P(f,"Refugee naturalisation on Form N-400: the 5-year clock","When a refugee may file Form N-400, how the 5-year clock uses the U.S. arrival date, the 30-month presence rule, fees, the test and Selective Service.",f'''<h1>Naturalisation after 5 years (Form N-400)</h1>
<div class="card"><p>Naturalisation is the way a person born outside the United States becomes a U.S. citizen. The usual application is Form N-400, Application for Naturalization, after at least 5 years as a lawful permanent resident{src("n400","n400five")}.</p>
<p>For a refugee, those 5 years are not counted from the day U.S. Citizenship and Immigration Services (USCIS) approves the green card. USCIS rolls the permanent-residence date back to an earlier day, set out below. You still file Form N-400 only after you are a permanent resident{src("pm12d2","pm7l5")}.</p>
<p>The green card application itself is on {L("green-card/index.html","Green card after 1 year",f)}. Rules for leaving the United States are on {L("travel-document/index.html","Can I leave the USA?",f)}.</p></div>
<h2>When the 5 years start</h2>
<div class="card"><p>Most people become lawful permanent residents on the day USCIS approves the adjustment application, or on the day they are admitted with an immigrant visa. For some classes the effective date is earlier. The Policy Manual calls that earlier date a rollback date. A refugee is generally considered a lawful permanent resident as of the date of entry into the United States. The manual cites section 209(a)(2) of the Immigration and Nationality Act{src("pm12d2")}.</p>
<p>The refugee adjustment chapter states the same rule at approval: if the application is approved, the effective date of permanent residence is the date the person was first admitted to the United States as a refugee{src("pm7l5")}.</p>
<p>There is one stated exception. A derivative refugee who gained status through an approved relative petition, and who was already in the United States when that petition was approved, has an effective date of the day the petition was approved, not the day of entry{src("pm7l5")}. The physical-presence chapter for adjustment calls that petition Form I-730{src("pm7")}.</p>
<p><strong>Example of the counting rule, not a promise about a real case.</strong> A principal refugee admitted on 1 March 2026, whose adjustment USCIS later approves, has an effective permanent-residence date of 1 March 2026. The general 5-year period runs from that date.</p>
<p>The permanent resident card shows the date of the status and the class of admission. After approval, a principal refugee is adjusted as RE-6. A spouse admitted as the spouse of a refugee is RE-7. A child admitted as the child of a refugee is RE-8{src("pm7l5","pm12d2")}.</p>
<p>If the date printed on the card does not match the rule above, how to correct the card is not stated by the pages checked. Ask an immigration attorney or an accredited representative before you file.</p></div>
<h2>You file only after the green card</h2>
<div class="card"><p>You generally must show lawful admission for permanent residence at the time you file Form N-400. The card is evidence of the status. The card alone does not prove the admission was lawful, and it does not by itself prove continuous residence or physical presence{src("pm12d2","pm12","pm12d4")}.</p>
<p>If Form I-485 is still pending on the anniversary of arrival, these pages do not say you may file Form N-400. Get the green card approved first.</p>
<p>One narrow point goes the other way. If USCIS approved a refugee adjustment even though 1 year of physical presence had not yet accrued on the day the adjustment was filed, USCIS does not deny naturalisation on that ground alone, as long as the admission was otherwise lawful and the year had accrued by the time adjustment was approved{src("pm12d2")}.</p></div>
<h2>Continuous residence and trips abroad</h2>
<div class="card"><p>Under the general rule you must have resided continuously in the United States after lawful permanent resident admission for at least 5 years before you file, and up to the time of naturalisation. USCIS looks at the whole period from that admission to the present{src("pm12")}.</p>
<p>Because a refugee admission date rolls back, time in the United States before the green card is approved can sit inside those 5 years. A trip taken while you were still waiting for the card can be an absence during the statutory period. Read that together with the travel page before you leave the country.</p>
<ul>
<li>An absence of 6 months or less does not, by itself, break continuous residence. Several shorter trips can still be reviewed{src("pm12")}.</li>
<li>More than 6 months but less than 1 year is presumed to break it. You can try to rebut that presumption. Examples in the chapter include U.S. employment that was not ended, no job taken abroad, immediate family who stayed, and a home you still owned or leased{src("pm12")}.</li>
<li>One year or more breaks continuous residence unless Form N-470 is approved for qualifying employment abroad{src("pm12")}.</li>
<li>An approved Form N-470 does not remove the physical-presence requirement, except for certain U.S. government work or religious duties described in that chapter{src("pm12")}.</li>
</ul>
<p>If any trip lasted more than 6 months but less than 1 year, the Form N-400 page asks for evidence that you kept your residence. The examples it lists include rent or mortgage statements, pay statements, bank or credit-card statements, proof of car registration and insurance, passport stamps, and IRS tax transcripts{src("n400")}.</p>
<p>Possession of the card for 5 years does not, by itself, prove continuous residence{src("pm12")}.</p>
<p>A re-entry permit, requested on Form I-131 after you have a green card, is a different document from Form N-470. The pages checked do not say one replaces the other. See {L("travel-document/index.html","Can I leave the USA?",f)}.</p></div>
<h2>Physical presence: 30 months</h2>
<div class="card"><p>Continuous residence and physical presence are separate. For the general provision, you must have been physically present in the United States for at least 30 months, which the manual also states as at least 913 days, before you file{src("pm12d4","n400five")}.</p>
<p>USCIS counts the day you depart and the day you return as days of physical presence{src("pm12d4")}.</p>
<p>The public eligibility page measures those 30 months out of the 5 years immediately before the date you file Form N-400{src("n400five")}.</p>
<p>Possession of the card does not, by itself, prove physical presence. USCIS reviews the records and can consider your testimony{src("pm12d4")}.</p></div>
<h2>Age, address, and filing 90 days early</h2>
<div class="card"><ul>
<li>Be at least 18 years old when you submit Form N-400{src("n400five")}.</li>
<li>Have lived for at least 3 months in the state or USCIS district with jurisdiction over your place of residence. The manual measures that time from the moment you first establish residence there. Residence means the principal, actual dwelling place, without regard to intent{src("n400five","pm12d6")}.</li>
<li>A student who is financially dependent on parents may apply where the school is, or where the family lives{src("n400five")}.</li>
<li>If you move after you file, you must report the change of address so USCIS can send the file to the office for the new address{src("pm12d6")}.</li>
</ul>
<p>You may file Form N-400 up to 90 days before you would first meet the 5-year continuous-residence period. You are not eligible for naturalisation until that 5-year period is complete. USCIS counts the 90 days back from the day before the day you would first meet the requirement{src("n400","pm12d6")}.</p>
<p>The manual gives this example. If the 5 years would first be complete on 10 June 2010, USCIS starts the count from 9 June 2010, and the earliest filing date in the example is 12 March 2010{src("pm12d6")}.</p>
<p>If you file early, and the 3-month state or district period falls inside the 5 years, the manual bases jurisdiction on the 3 months immediately before the examination on the application{src("pm12d6")}.</p>
<p>The Form N-400 page also allows the 90-day filing window when eligibility is based on 3 years as a permanent resident married to a U.S. citizen. This page does not set out that marriage basis. Read the form page if that is your situation{src("n400")}.</p>
<p>The early-filing chapter does not say the 90 days reduce the 30 months of physical presence. The public page ties those 30 months to the date you file. Read together, the 90-day window is not extra time in which to accumulate days inside the United States{src("pm12d6","n400five","pm12d4")}.</p></div>
<h2>English, civics, character and the oath</h2>
<div class="card"><p>The public 5-year page also requires all of the following{src("n400five")}:</p>
<ul>
<li>Good moral character for at least 5 years immediately before the date you file.</li>
<li>Attachment to the principles and ideals of the U.S. Constitution.</li>
<li>Ability to read, write and speak basic English.</li>
<li>Knowledge of U.S. history and of the principles and form of government (civics).</li>
<li>The Oath of Allegiance to the United States.</li>
</ul>
<p>The good-moral-character chapter says you must show that character during the 5 years immediately before the application and up to the oath, and that conduct from before those 5 years can still matter{src("pm12d9")}.</p>
<p>The oath is taken at a public ceremony. The exceptions page says the law allows certain modifications and points to section 337 of the Immigration and Nationality Act and to title 8 of the Code of Federal Regulations, at 8 CFR 337.1(b). What those modifications are, in practice, is on those citations, which this page does not restate{src("natex")}.</p></div>
<div class="card"><p><strong>English language exceptions.</strong> You are exempt from the English requirement, and you still take the civics test, if either of these is true at filing{src("natex")}:</p>
<ul>
<li>Age 50 or older, and you have lived as a permanent resident for 20 years (often called 50/20).</li>
<li>Age 55 or older, and you have lived as a permanent resident for 15 years (often called 55/15).</li>
</ul>
<p>You may take the civics test in your native language. You must bring an interpreter who is fluent in English and in that language{src("natex")}.</p>
<p>If you are 65 or older and have been a permanent resident for at least 20 years at filing, the exceptions page says you receive special consideration on civics. The test-updates page is more specific: USCIS gives 10 questions from a bank of 20, drawn from the 2008 test or the 2025 test according to when you filed, and you may take the test in the language of your choice{src("natex","civics")}.</p>
<p>Those year-counts are years as a permanent resident. For a refugee, the Policy Manual treats permanent residence as beginning on the rollback date once adjustment is approved. The exceptions page does not repeat the refugee sentence. If you are close to 50, 55 or 65, show both pages to a lawyer before you rely on an exception{src("natex","pm12d2")}.</p>
<p>A separate medical exception uses Form N-648, Medical Certification for Disability Exceptions, if a physical or developmental disability or a mental impairment prevents you from meeting the English or civics requirement. A licensed medical or osteopathic doctor, or a licensed clinical psychologist, completes it{src("natex","n400")}.</p>
<p>For a disability accommodation at an appointment, the exceptions page tells you to use the request page it names, uscis.gov/accommodations, or to ask the USCIS Contact Center, and to do it when the appointment notice arrives{src("natex")}.</p></div>
<div class="card"><p><strong>Which civics test.</strong> File Form N-400 before 20 October 2025 and USCIS uses the 2008 civics test. File on or after 20 October 2025 and USCIS uses the 2025 civics test. Some answers change after elections, appointments or changes in law. You answer with the name of the official who is serving at your interview. The updates page lists the answers that were current when that page was reviewed, and it is the page to re-check before you study{src("civics")}.</p>
<p>A single processing time for Form N-400 is not stated on the pages this guide quotes. Use the {a(S["ptime"],"USCIS processing times tool")} and select the form and office there{src("ptime")}.</p></div>
<h2>The fee</h2>
<div class="card"><p>The Form N-400 page and Form G-1055, the fee schedule, list these filing amounts{src("n400","g1055")}:</p>
<ul>
<li>Full fee by paper: $760.</li>
<li>Full fee online: $710.</li>
<li>Reduced paper fee: $380, if you submit the supporting documents the schedule describes.</li>
<li>$0 if you meet the military-service requirements in section 328 or 329 of the Immigration and Nationality Act. This page does not set out that path.</li>
<li>$0 if you qualify for a fee waiver. The schedule points to Form I-912, Request for Fee Waiver.</li>
</ul>
<p>You cannot file online if you request the reduced fee or a fee waiver. File a paper Form N-400. Do not file both a reduced-fee request and a fee waiver{src("n400","n400red")}.</p>
<p>On the form, the filing tips say to select No in Part 10 and skip to Part 11 if you pay the full fee, and to select Yes and complete Part 10 if you request the reduced fee. For a fee waiver, the tips say you are not required to complete Part 10, Item 1, and you submit Form I-912 or a written request instead of a fee{src("n400")}.</p></div>
<div class="card conf"><p><strong>The income line is not written the same way on every page.</strong></p>
<ul>
<li>Form G-1055 gives the $380 paper fee if documented annual household income is not more than 400 percent of the Federal Poverty Guidelines{src("g1055")}.</li>
<li>The reduced-fee page says USCIS approves a reduced fee only if documented annual household income is less than 400 percent of those guidelines. It also says: if income is at or below 150 percent, do not request the reduced fee. Request a fee waiver instead{src("n400red")}.</li>
<li>The $380 row on the schedule does not repeat the 150 percent instruction. At exactly 400 percent, "not more than" and "less than" are not the same test. Show both pages to the person who helps you file, and follow the page that applies to the request you actually submit.</li>
</ul></div>
<div class="card"><p>A fee waiver is available when the form is eligible and you document one of these{src("feewaive","g1055")}:</p>
<ul>
<li>You, your spouse, your child, or your parent (if you are under 21 or disabled) currently receive a means-tested benefit.</li>
<li>Household income is at or below 150 percent of the Federal Poverty Guidelines when you file.</li>
<li>You are experiencing extreme financial hardship that prevents you from paying the fee, including unexpected medical bills or emergencies.</li>
</ul>
<p>Send Form I-912, or a written request, with the paper Form N-400. The I-912 page says you cannot send the waiver request after USCIS has already received the N-400{src("i912","feewaive")}.</p>
<p>Examples of means-tested benefits on the waiver page include Medicaid, the Supplemental Nutrition Assistance Program (SNAP), Temporary Assistance for Needy Families (TANF) and Supplemental Security Income (SSI). The same page says it does not treat Medicare, unemployment benefits or Social Security benefits as means-tested benefits for this request. Whether Refugee Cash Assistance is on that list: not stated. A benefit card by itself is not acceptable evidence unless it shows the details that page requires{src("feewaive")}.</p>
<p>The N-400 rows on the fee schedule do not add a separate Public Law 119-21 amount. The chart of non-waivable Public Law 119-21 fees on the fee-waiver page does not name Form N-400{src("g1055","feewaive")}.</p></div>
<h2>What to send and how to file</h2>
<div class="card"><p>The Form N-400 page checked for this edition lists edition date 01/20/25. Use the edition that page lists on the day you file. Every page must come from that edition, and the edition date and page numbers must be visible, or USCIS may reject the form{src("n400")}.</p>
<p>You generally file online, through a USCIS online account, or by mail. The form page links the direct filing addresses. Mail sent to the wrong address can take longer. Reduced-fee and fee-waiver cases are paper filings only{src("n400")}.</p>
<p>Sign the form. USCIS rejects an unsigned form{src("n400")}.</p>
<p>Send copies unless the instructions ask for an original. Any document in a foreign language needs a full English translation and a certification that the translation is complete and accurate and that the translator is competent{src("n400")}.</p>
<p>The form page checklist, which you do not submit, says every applicant provides the following if they apply to the case{src("n400")}:</p>
<ul>
<li>A copy of both sides of the permanent resident card.</li>
<li>Form N-648, if you request a disability exception to English or civics.</li>
<li>The current marriage certificate, and proof that each prior marriage ended, if that applies.</li>
<li>Arrest, charge, conviction and sentencing records. This includes an arrest or detention where no charges were filed.</li>
<li>Traffic records only if the incident involved alcohol or drugs, led to an arrest, or seriously injured another person.</li>
<li>If taxes are owed, a signed agreement from the Internal Revenue Service (IRS) or the state or local tax office showing a return was filed and payment was arranged.</li>
<li>Child-support evidence, if that applies.</li>
<li>Evidence for any trip of more than 6 months but less than 1 year, as listed earlier.</li>
<li>Selective Service evidence in the situation described in the next section.</li>
</ul>
<p>The checklist says it does not replace the form instructions. Read the instructions before you send the packet{src("n400")}.</p></div>
<div class="card"><p><strong>Biometrics and the card while the case is pending.</strong> Applicants generally must attend biometrics unless USCIS waives them. The appointment notice gives the time and place. The photograph taken there may be used on the Certificate of Naturalization, so the form page recommends clothing that is acceptable for display on that certificate. USCIS may later ask for physical passport-style photographs{src("n400")}.</p>
<p>For a Form N-400 properly filed on or after 12 December 2022, the receipt notice extends the green card for 24 months from the "Card Expires" date on the card. Present the receipt together with the card. If you lose the card, you generally must still file Form I-90, Application to Replace Permanent Resident Card, even though naturalisation is pending. If you lose the receipt and the date on the card has passed, you generally must file Form I-90{src("n400")}.</p>
<p>You may be represented, at no expense to the U.S. government, by an attorney or an accredited representative. The representative submits Form G-28, Notice of Entry of Appearance as Attorney or Accredited Representative{src("n400")}.</p></div>
<h2>Selective Service for men aged 18 to 25</h2>
<div class="card"><p>The Selective Service chart says the registration requirement applies, with few exceptions, to male U.S. citizens and male immigrants living in the United States who are 18 through 25. On that chart, the row for refugee, parolee and asylee immigrants is Yes. The row for lawful nonimmigrants on a current nonimmigrant visa is No{src("ssschart","ssswho")}.</p>
<p>The Selective Service FAQ says that if you were born a male, you are likely required to register, and it points you to that chart. The same FAQ says the Military Selective Service Act, as written, only authorizes registration of male persons{src("sssfaq")}.</p>
<p>Registering does not mean you are joining the military{src("sssfaq")}.</p>
<ul>
<li>The Policy Manual says males must register within 30 days of the 18th birthday, and not after reaching age 26. It names a local post office, a registration card received by mail, and online registration{src("pm12d7")}.</li>
<li>The FAQ says men 18 through 25 can register online with a valid Social Security number, and that a valid number already in the Selective Service database is required for online registration. A number issued recently may not be in that database yet. If you have a Social Security number, you are required to provide it{src("sssfaq")}.</li>
<li>If more than 30 days have passed since the 18th birthday, the FAQ says to register immediately. Late registration is accepted until the man turns 26. After that, it is too late to register{src("sssfaq")}.</li>
</ul>
<p>A method for a man who has no Social Security number yet: not stated on the FAQ page checked. The Policy Manual names a post office and a card received by mail, and it does not say those two paths require a number. Read both pages, and read {L("social-security-card/index.html","Social Security card",f)} for how the number itself is issued.</p>
<p>When a male applicant aged 18 to 26 files for adjustment of status, USCIS says it transmits the data to Selective Service. Selective Service then sends an acknowledgement, which is the proof of registration. If USCIS or Selective Service does not finish that process, the manual says that failure is not a willful failure by the applicant. Do not treat the Form I-485 receipt, by itself, as proof that you registered. Keep the acknowledgement. You can check registration on the {a(S["sssver"],"Selective Service verify page")}. The manual also lists telephone confirmation at (847) 688-6888{src("pm12d7","sssfaq")}.</p></div>
<div class="card warn"><p><strong>Failure to register can block naturalisation for a time, and the letter USCIS asks for is no longer issued.</strong></p>
<ul>
<li>USCIS will deny naturalisation if the applicant refuses to register, or knowingly and willfully failed to register, during the period when registration was required{src("pm12d7")}.</li>
<li>Under 26: generally ineligible. From 26 to 31: may be ineligible, with a chance to show the failure was not knowing or willful, or that registration was not required. Over 31: eligible even if the failure was knowing and willful, because the manual treats it as outside the statutory period{src("pm12d7")}.</li>
<li>The Form N-400 evidence list asks for a status information letter and a statement of reasons if you had to register, did not do so before 26, and you are now over 26 but under 31. If you are filing because you are married to a U.S. citizen, that list uses under 29 instead of under 31{src("n400")}.</li>
<li>As of 30 June 2026, the Selective Service FAQ says the agency no longer issues status information letters. It tells men to check registration on the verify page, and it says Selective Service does not decide whether another agency grants a benefit{src("sssfaq")}.</li>
</ul>
<p>Chapter 7 of the Policy Manual does not mention age 29. The form page does. And both USCIS pages still name a status information letter that Selective Service says it stopped issuing on 30 June 2026. If you are between these ages, or you did not register, show all three pages to an immigration attorney or an accredited representative. This guide does not invent a letter to stand in for the one Selective Service no longer issues.</p>
<p>Separately, the FAQ says failure to register is a violation of the Military Selective Service Act, and that a conviction may result in imprisonment for up to 5 years, a fine of not more than $250,000, or both. That criminal sentence is not the same thing as the naturalisation rule above{src("sssfaq")}.</p></div>
<h2>Where the official pages do not match</h2>
<div class="card conf"><ul>
<li>Reduced fee at the 400 percent line, and the 150 percent cross-over to a waiver: Form G-1055 says "not more than 400 percent". The reduced-fee page says "less than 400 percent", and it tells a person at or below 150 percent to request a waiver instead of the $380 fee. The schedule row does not repeat that 150 percent sentence{src("g1055","n400red")}.</li>
<li>Selective Service evidence ages: the Form N-400 page uses under 31, or under 29 for a spouse of a U.S. citizen. Policy Manual Chapter 7 uses under 26, between 26 and 31, and over 31, and does not mention 29{src("n400","pm12d7")}.</li>
<li>Status information letter: the Form N-400 page and Chapter 7 still ask for one. The Selective Service FAQ, as of 30 June 2026, says the agency no longer issues that letter{src("n400","pm12d7","sssfaq")}.</li>
</ul>
<p>The dollar amounts for the ordinary filing fee do match: $760 on paper and $710 online on both the form page and Form G-1055{src("n400","g1055")}.</p></div>''',n400_faqs)

faq_groups=[
("Money and tax",[
("I was an employee in South Africa. What happens to my tax when I start work?",
 f'<p>Being a refugee is an immigration status. It is not, by itself, a tax status. The IRS says you are a resident alien for tax if you meet the green card test or the substantial presence test.{src("irs_p519","irs_visa")}</p><p>SARS says a change in South African tax residence must be declared. Leaving the country does not, on its own, complete that declaration.{src("sars_cease")}</p><p>The checklist is {L("tax-first-year/index.html","Tax when you start work")}. It is general information, not tax advice. Speak to a qualified tax practitioner.</p>'),
]),
("Applying",[
("Who can be considered for this programme?",
 f'<p>The U.S. Embassy page dated 7 October 2026 says you must be a South African national, of Afrikaner ethnicity or a member of a racial minority, able to describe persecution or a fear of persecution, at least 18 or referred with a parent, and living in South Africa.{src("emb")}</p><p>Not everyone who meets that list is referred. The U.S. government decides access, not RSC Africa or Amerikaners. Read {L("eligibility/index.html","Eligibility and referral")}.{src("emb")}</p>'),
("Is the programme only for Afrikaners?",
 f'<p>The Embassy criteria include Afrikaner ethnicity or a member of a racial minority in South Africa.{src("emb")}</p><p>Presidential Determination 2026-14 allocates the extra fiscal year 2026 admissions among Afrikaners from South Africa, and Presidential Determination 2026-24 says fiscal year 2027 admissions are primarily allocated among Afrikaners.{src("pd26","pd27")}</p><p>The pages do not use the same words, so read {L("eligibility/index.html","Eligibility and referral")} and {L("programme-status/index.html","Programme status and caps")}.</p>'),
("How do I apply?",
 f'<p>If no USRAP partner has contacted you yet, complete the online USRAP Intake Questionnaire on the Department of State website the Embassy links.{src("emb")} {a(S["uiq"],"Open the official questionnaire")}</p><p>The referral partners the Embassy names are RSC Africa, operated by Church World Service, and Amerikaners.{src("emb","embfaq")}</p><p>Read {L("online-intake/index.html","Online intake questionnaire")}.</p>'),
("I already sent a Statement of Interest. Do I still need the questionnaire?",
 f'<p>Yes, if you are still interested and a partner has not contacted you: the 7 October 2026 Embassy page says you must complete the questionnaire.{src("emb")}</p><p>A 13 February 2025 notice told people to email PretoriaPRMInfo@state.gov, but the October page does not mention that mailbox and does not say the email was replaced.{src("emb2025","emb")}</p><p>Follow the newer page, explained on {L("online-intake/index.html","Online intake questionnaire")}.</p>'),
("Does it cost anything to apply?",
 f'<p>No. The Embassy FAQ says referrals, applications and related services are free, and it names only RSC Africa (Church World Service) and Amerikaners as official implementers in South Africa.{src("embfaq","emb")}</p><p>Do not pay anyone who says they can speed the case up or guarantee approval.{src("embfaq")}</p><p>Read {L("avoiding-scams/index.html","Avoiding scams")}.</p>'),
("How long does the process take?",
 f'<p>There is no standard or guaranteed timeline. Every case is different, and times vary widely.{src("embfaq")}</p><p>When the case is ready for a pre-screen interview you receive a case number for the RSC Africa MyCase site, and later questions go to SouthAfrica@cwsafrica.org with that number.{src("embfaq")}</p><p>Read {L("online-intake/index.html","Online intake questionnaire")} and {L("programme-status/index.html","Programme status and caps")}.</p>'),
("I submitted the form and no one has contacted me. Was I accepted?",
 f'<p>Check the dashboard first: each person should show "Information Entry Complete", and you must select "Submit Family Group UIQ Application" until the family group status says "Complete", even if you are applying alone.{src("embfaq")}</p><p>If that is done and you still have no case number, wait. You can track the case only after RSC Africa gives you one.{src("embfaq")}</p><p>Read {L("online-intake/index.html","Online intake questionnaire")}.</p>'),
("Can I apply if I am outside South Africa?",
 f'<p>No. Every person on the case, including children, must be living and physically present in South Africa, so a temporary work visa or a holiday abroad does not qualify.{src("embfaq")}</p><p>Processing includes in-person appointments.{src("embfaq")}</p><p>Read {L("eligibility/index.html","Eligibility and referral")}.</p>'),
("What civil documents will I need?",
 f'<p>The Embassy FAQ says cases use civil documents such as birth, marriage, death and divorce records, and that the set depends on the case.{src("embfaq")}</p><p>Some start with a short form, and others are later asked for the full record. An unabridged birth certificate is almost always required for a child who will resettle with a parent, and RSC Africa tells you what your case needs.{src("embfaq")}</p><p>Read {L("online-intake/index.html","Online intake questionnaire")}.</p>'),
]),
("Interview and medicals",[
("What happens after I am accepted for processing?",
 f'<p>RSC Africa contacts you with the next steps: a pre-screen interview, security vetting, a USCIS interview and a medical exam.{src("embfaq")}</p><p>USCIS, in the Department of Homeland Security, decides refugee status. The State Department, the U.S. Mission in South Africa and RSC Africa do not.{src("embfaq")}</p><p>Read {L("online-intake/index.html","Online intake questionnaire")} and {L("programme-status/index.html","Programme status and caps")}.</p>'),
("How do I get an interview and a medical exam?",
 f'<p>After you are granted access, RSC Africa contacts you to schedule the pre-screen interview, the USCIS interview and the medical exam.{src("embfaq")}</p><p>The medical exam is arranged with panel physicians in Cape Town, Johannesburg or Pretoria, as close to where you live as they can.{src("embfaq")}</p><p>You do not book those appointments from a public website. Read {L("online-intake/index.html","Online intake questionnaire")}.</p>'),
("What security checks do I have to complete?",
 f'<p>USRAP implementers run the security and background checks while the case is processed.{src("embfaq")}</p><p>The Embassy FAQ says the step it asks of you, when contacted, is fingerprinting with Managed Integrity Evaluation (MIE).{src("embfaq")}</p><p>If your address, email or phone changes after you have access, tell RSC Africa immediately. Read {L("online-intake/index.html","Online intake questionnaire")}.{src("embfaq")}</p>'),
("Who decides my case, and can it change at the last minute?",
 f'<p>USCIS decides each case, and vetting continues until arrival, so status can change even shortly before travel.{src("embfaq")}</p><p>USCIS has found some South African cases ineligible for continued processing: there is no appeal, no one on that case may apply again, and MyCase is deactivated within five days of the email notice.{src("embfaq")}</p><p>Read {L("eligibility/index.html","Eligibility and referral")}.</p>'),
]),
("Travel and arrival",[
("Who books the flight to the United States?",
 f'<p>The October 2026 Embassy page names one official booker: RSC Africa, operated by Church World Service.{src("emb")}</p><p>Travel booked by anyone else is not supported and can put your entry, and your initial help, at risk.{src("emb")}</p><p>That page does not name the International Organization for Migration as the office that books these flights. Read <a href="/bringing-pets/#refugee-flights">who books a refugee flight</a>.{src("emb")}</p>'),
("Can I choose which city I go to?",
 f'<p>Not as a free choice. Tell RSC Africa early about a friend, family member or employer in the United States, called a U.S. tie.{src("embfaq")}</p><p>They try to place you nearby, but they cannot always do it, and other location wishes are not considered.{src("embfaq")}</p><p>Once you support yourself you may move, as explained on {L("first-90-days/index.html","First 90 days")}.</p>'),
("Who meets me, and will I have housing?",
 f'<p>A local resettlement provider case manager meets you at the airport, or arranges for your U.S. tie to meet you, and then gives basic support.{src("embfaq")}</p><p>The provider typically finds the first housing. The Embassy FAQ says it should be safe and adequate, but it may be an apartment rather than a house, and some people need a roommate.{src("embfaq")}</p><p>Read {L("first-90-days/index.html","First 90 days")}.</p>'),
("Should I contact the U.S. agency before I fly?",
 f'<p>No. Ask RSC Africa before you travel, because local providers are not able to answer pre-arrival email, phone or WhatsApp.{src("embfaq")}</p><p>After you arrive, the provider contacts you, and if you leave the place you were sent you may lose the initial resettlement services.{src("embfaq")}</p><p>Read {L("first-90-days/index.html","First 90 days")} and {L("agency-not-helping/index.html","When your agency is not helping")}.</p>'),
("What help do I get in the first weeks?",
 f'<p>The Embassy FAQ describes limited help through the Program of Initial Resettlement, typically for 30 to 90 days, including some housing, orientation and basic benefits.{src("embfaq")}</p><p>The Office of Refugee Resettlement says services run up to 90 days and does not state a 30-day minimum, so the two pages use different wording.{src("pir","embfaq")}</p><p>The stated goal is early self-sufficiency through work. See {L("first-90-days/index.html","First 90 days")}.</p>'),
]),
("First months",[
("Can I work as soon as I arrive?",
 f'<p>Yes, refugees may work immediately on arrival, and USCIS creates an Employment Authorization Document for a principal refugee and family who arrive with them. You should receive it within a few weeks after you arrive, depending on delivery times.{src("gc")}</p><p>There is no fee for the initial or renewal refugee work card in category (a)(3), and for Form I-9 the Form I-94 arrival record is acceptable for 90 days.{src("gc")}</p><p>Read {L("jobs/index.html","Jobs and employment services")}.</p>'),
("How do I get a Social Security card?",
 f'<p>If you asked for a Social Security number during processing, the Department of Homeland Security sends the data to the Social Security Administration, which mails the card to the address you gave or to your sponsoring agency.{src("ssncfr")}</p><p>You can also apply at an office with your arrival record or a work card in category A3, and refugees receive an unrestricted card.{src("ssnr")}</p><p>How long delivery takes is not stated, so ask your resettlement agency if it does not arrive, and read {L("social-security-card/index.html","Social Security card")}.</p>'),
("What benefits can I get, and for how long?",
 f'<p>Sign up immediately. Cash and medical help are time-limited from your eligibility date, and you may qualify for Temporary Assistance for Needy Families (TANF), Supplemental Security Income (SSI), Medicaid or the Supplemental Nutrition Assistance Program (SNAP).{src("ben")}</p><p>Refugee Cash Assistance (RCA), if you are not eligible for TANF or SSI, is up to 12 months in the October 2026 letter for an eligibility date on or after 1 January 2026, while an older fact sheet still says four months.{src("dcl","frrma","ben")}</p><p>Confirm with your provider, and read {L("benefits/index.html","Benefits checklist")}.</p>'),
("Will I have health cover?",
 f'<p>The Embassy FAQ says the United States does not have a national public health care system. It says you could be eligible for Refugee Medical Assistance (RMA) for up to 12 months when you first arrive. The October 2026 letter says up to 12 months of RMA for an eligibility date on or after 1 January 2026. An older fact sheet still says four months.{src("embfaq","dcl","ben")}</p><p>The Embassy FAQ says that after RMA ends there can be a gap until a job includes health insurance, or until you are eligible for Medicaid. It says Medicaid is typically available once you are a lawful permanent resident, which you may apply for after one year, and that not everyone qualifies. In most states it depends on household income, family size, age, and health. You may also buy private insurance, including on the Health Insurance Marketplace or a state exchange. What those plans cost is not stated as one figure.{src("embfaq")}</p><p>Exactly how refugee Medicaid eligibility changed on 1 October 2026 is not stated on these pages. Ask your resettlement agency which cover you can get, and read {L("health-cover/index.html","Health cover")}.</p>'),
("What is expected of me after I arrive?",
 f'<p>The Embassy FAQ says you are expected to look for work soon and to take the first job offered, even if it is not the one you want, and that refusing may put support at risk.{src("embfaq")}</p><p>Many foreign qualifications are not automatically recognised, so that job may be outside your old field or at a lower level.{src("embfaq")}</p><p>Ask your resettlement agency how this applies to you, and read {L("jobs/index.html","Jobs and employment services")}.</p>'),
("What if my resettlement agency is not helping?",
 f'<p>Start with your case manager and the provider grievance process, which should be explained when you arrive.{src("embfaq","pir")}</p><p>You can also contact the State Refugee Coordinator on the federal contact list, or the initial-resettlement mailbox named on the guide page below.{src("src","pir")}</p><p>Read {L("agency-not-helping/index.html","When your agency is not helping")}.</p>'),
]),
("Green card after 1 year",[
("When can a refugee apply for U.S. citizenship?",
 f'<p>After you are a lawful permanent resident, on Form N-400. For a refugee, the general 5-year period runs from the date of entry into the United States once adjustment is approved, not from the approval date. A derivative already in the United States when the relative petition was approved uses that approval date.{src("pm12d2","pm7l5","n400")}</p><p>You also need at least 30 months of physical presence before you file, and you may file up to 90 days before the 5 years of continuous residence are complete.{src("pm12d4","pm12d6")}</p><p>Read {L("naturalization/index.html","Naturalisation after 5 years")}.</p>'),
("When do I apply for permanent residence, and is there a fee?",
 f'<p>USCIS requires an application after at least one year of physical presence, while the Embassy FAQ says to apply exactly one year after arrival.{src("gc","embfaq")}</p><p>The Policy Manual counts only days inside the United States when the application is decided, so a trip means you wait until those days add up to a year.{src("pm7")}</p><p>A principal pays no filing fee and no biometrics fee. For a family member, the green card page does not print a dollar amount and points to the fee schedule. Form G-1055 lists a filing fee of $0 if you are a refugee or you were paroled as a refugee. That row does not split a principal from a family member. Ask your resettlement agency how this applies to you, and read {L("green-card/index.html","Green card after 1 year")}. The schedule is in the <a href="/about/#src-g1055">source list</a>.{src("gc")}</p>'),
]),
("Travel abroad",[
("Can I leave on my South African passport?",
 f'<p>Do not leave on a South African passport, and do not treat a trip back as safe. USCIS says refugees cannot get a passport from the country of nationality, and that going back can be evidence you no longer need protection.{src("guide")}</p><p>You need a refugee travel document before you leave, unless you already have advance parole.{src("i131i","td")}</p><p>Speak to an immigration attorney or an accredited representative before you book, and read {L("travel-document/index.html","Can I leave the USA?")}.</p>'),
("Does a trip abroad count toward the one-year residence rule?",
 f'<p>No. Days outside the United States do not count, and the Policy Manual measures the year when the application is decided.{src("pm7")}</p><p>The public page also says you must be physically present for at least one year after admission when you file.{src("gc")}</p><p>Read both before you travel in the first year, on {L("green-card/index.html","Green card after 1 year")} and {L("travel-document/index.html","Can I leave the USA?")}.</p>'),
]),
("Pets",[
("Will the programme bring my pet?",
 f'<p>No. Neither the U.S. government nor programme partners fund or arrange pet travel, including for an emotional-support animal.{src("emb","embfaq")}</p><p>Wait at least 90 days, because the first housing may not allow pets and pet deposits cannot be paid from resettlement funds.{src("emb","embfaq")}</p><p>You arrange any later shipping yourself, not every animal can enter, and the detail is on {L("bringing-pets/index.html","Bringing your pets")}.</p>'),
("What are the import rules for a dog from South Africa?",
 f'<p>South Africa is on the high-risk dog list. A dog needs a microchip before the rabies vaccine, must be at least 6 months old on entry, and needs a valid rabies blood test from an approved lab or a booking that includes 28 days of quarantine.{src("cdc_hr","cdc_fv")}</p><p>The import form is free, and the Embassy wait of at least 90 days is a separate rule.{src("cdc_fv","emb")}</p><p>Read {L("bringing-pets/index.html","Bringing your pets")}.</p>'),
]),
("Family",[
("Can I live near family or friends who are already in the United States?",
 f'<p>Tell RSC Africa as early as you can. A friend, family member or employer in the United States is called a U.S. tie, including someone who arrived as a refugee before you.{src("embfaq")}</p><p>An effort is made to place you nearby, but it is not guaranteed, and a wish that is not a U.S. tie is not used to pick a city.{src("embfaq")}</p><p>Read {L("first-90-days/index.html","First 90 days")}.</p>'),
("My partner has an H-2A or H-2B visa. Can we still apply?",
 f'<p>An H-2A or H-2B visa does not by itself stop you applying. You still have to be living and physically present in South Africa.{src("embfaq")}</p><p>If you hold, or plan to seek, another U.S. status at the same time, the Embassy FAQ says to consult an immigration attorney, because the two applications can affect each other.{src("embfaq")}</p><p>Read {L("eligibility/index.html","Eligibility and referral")}.</p>'),
]),
]
faq_flat=[(q,a) for _g,items in faq_groups for q,a in items]
faq_body=f'''<h1>Common questions</h1>
<div class="card note"><p><strong>These answers are general.</strong> They are not legal advice and they are not about any individual case. Confirm your own facts with your resettlement agency, RSC Africa, an accredited representative or an immigration attorney. Read the {L("disclaimer/index.html","disclaimer")} and the {L("glossary/index.html","glossary")}. Last checked {D}.</p></div>
<p>The questions below are ones people ask about the U.S. Refugee Admissions Program (USRAP) for South Africans: on the U.S. Embassy FAQ, in news about the 2025 and 2026 programme, and in public posts about how to apply, how long it takes, work, pets and family. Each answer uses an official page or a page on this guide that already cites one. If a point is not on those pages, the answer says so instead of guessing.</p>'''
for g,items in faq_groups:
    faq_body+=f'<h2>{g}</h2>'+''.join(f'<details class="card"><summary>{q}</summary><div>{a}</div></details>' for q,a in items)
P('faq/index.html',"Frequently asked questions for South African refugees","Plain answers to common questions South Africans ask about the U.S. Refugee Admissions Program, from the form and interviews to work, pets and the green card.",faq_body,faq_flat,show_faqs=False)

f='about/index.html'
P(f,"About this independent guide for South African refugees","How this independent guide is built: official sources only, a link beside every fact, and no affiliation with any government.",f'''<h1>About this site</h1>
<div class="card warn"><strong>{NOTICE}</strong> The full notice is on the {L("disclaimer/index.html","disclaimer",f)}.</div>
<h2>Independent</h2><div class="card"><p>This site is independent. It is not affiliated with, endorsed by or run for any government or agency. That includes the U.S. Department of State, the U.S. Embassy and Consulates in South Africa, the Department of Health and Human Services, ACF, ORR, USCIS, CBP, SSA, CDC, USDA, any resettlement agency or referral partner, and the South African government.</p></div>
<h2>Method</h2><div class="card"><ul>
<li>Facts are tied to official pages that were opened and checked. A link sits beside every fact. The money and tax pages were checked on 27 October 2026. The other pages were checked on {D}.</li>
<li>Where a source is silent, the page says "not stated by source". Where two official pages disagree, both are shown.</li>
<li>IATA is included only for airline crate size. It is an airline industry body, not a government. The two related guides in the footer are independent sites about South African passports and smart ID cards. They are not official sources.</li>
<li>The site is factual and does not take a political position. Abbreviations are listed on the {L("glossary/index.html","glossary",f)}.</li>
</ul></div>
<h2>Sources used</h2><ul>{"".join(f'<li id="src-{k}">{a(u,esc(u))}</li>' for k,u in S.items())}</ul>''')

f='glossary/index.html'
gloss_body='<h1>Words and abbreviations explained</h1><p>Short meanings for words used on this site. If a short line and the official page do not match, follow the official page. The first time a word appears on another page, it links here.</p>'
for h,_pats,html in sorted(GLOSS, key=lambda row: row[0].lower()):
    gloss_body+=f'<h2>{esc(h)}</h2><div class="card"><p>{html}</p></div>'
P(f,"Words and abbreviations explained in plain English","Plain-English meanings for USRAP, USCIS, ORR, the refugee travel document and the other abbreviations used on this guide.",gloss_body)

f='disclaimer/index.html'
P(f,"Disclaimer: this guide is general information only","This guide is general information only. It is not legal advice, it has no warranty, and it is not affiliated with any government.",f'''<h1>Disclaimer</h1>
<h2>General information only</h2><div class="card"><p>The pages on this site are general information about public rules for South Africans in the U.S. refugee programme. They are not legal advice, not tax advice, and not advice about your own case. Refugee status, travel, a green card and citizenship can turn on facts this site does not know.</p></div>
<h2>Not legal advice</h2><div class="card"><p>Nothing here creates a lawyer-client relationship. Before you travel, file a form, pay anyone, or rely on a deadline, speak to an immigration attorney or an accredited representative, and confirm the point on the official page linked beside it. Your resettlement agency can explain the services it actually provides. It is not your lawyer.</p></div>
<h2>No warranty</h2><div class="card"><p>The pages are provided as general reading. There is no warranty, express or implied, that a page is complete, current or fit for a particular decision. Official pages change. The "Last checked" date is the date the cited pages were read for this edition. It is not a promise that the rule is the same today.</p></div>
<h2>Limitation of liability</h2><div class="card"><p>To the extent the law allows, the people who publish this guide are not liable for loss or damage that results from using it, from being unable to use it, or from acting on it without checking the official source and getting advice about your own case. Some jurisdictions do not allow certain limits. In those places, the limit applies only as far as the law allows.</p></div>
<h2>External links</h2><div class="card"><p>Links to government sites, and the two related guides in the footer, are there so you can read the source. A link is not an endorsement of that site, of every page on that site, or of any organisation. Those sites have their own terms.</p></div>
<h2>Not affiliated</h2><div class="card"><p>This guide is not affiliated with any government or agency, including the U.S. Department of State, the U.S. Embassy in South Africa, USCIS, CBP, ORR, SSA, CDC, USDA, any resettlement agency, or the South African government. Flags in the header identify the two countries the guide is about. They are not a seal and they are not a sign of official status.</p></div>
<h2>Check the official source</h2><div class="card"><p>Every factual claim is meant to sit next to the official page it came from. If this guide and that page disagree, follow the official page. If two official pages disagree, the conflict is shown on purpose. Do not pick the sentence you prefer.</p></div>
<h2>Corrections</h2><div class="card"><p>This site has no contact email address and no corrections desk. A correction is made by re-reading the official page and changing the guide. If you think a line is wrong, compare it with the link beside it and with the {L("about/index.html","about page",f)}, which lists the sources.</p></div>''')

f='find/index.html'
find_body='<h1>All pages</h1><p>Type in the search box at the top of this page. The list below stays complete if search is not available.</p><p id="index-status" class="index-status" aria-live="polite">Showing every page.</p><div id="page-index">'
for g,it in G:
    find_body+=f'<section><h2>{esc(g)}</h2><ul class="index-list">'+''.join(
        f'<li data-keywords="{esc(ALIAS.get(p,""))}"><a class="jump" href="{href(p)}"><span class="lt">{esc(t)}</span><span class="ls">{esc(BLURB[p])}</span></a></li>'
        for p,t in it)+'</ul></section>'
find_body+='</div>'
P(f,"Find a page in this guide for South African refugees","Search or browse every page in this independent guide, from arrival and work to health, documents, the green card and citizenship.",find_body)

from moneytax import add_pages
add_pages(P, L, a, src, S)

s.page('404.html',"Page not found: South African refugees in the USA guide","That page is not on this guide. Use the menu or the links below to reach eligibility, arrival, benefits and the green card.",f'''<h1>Page not found</h1>
<p>That address is not on this guide. Use the menu, or start from one of these pages:</p>
<ul>
<li>{L("eligibility/index.html","Who can be referred")}</li>
<li>{L("online-intake/index.html","The free questionnaire")}</li>
<li>{L("bringing-pets/index.html","Bringing your pets")}</li>
<li>{L("first-90-days/index.html","Your first 90 days")}</li>
<li>{L("benefits/index.html","Cash, food and other help")}</li>
<li>{L("health-cover/index.html","Health cover")}</li>
<li>{L("jobs/index.html","Work and jobs")}</li>
<li>{L("travel-document/index.html","Leaving the United States")}</li>
<li>{L("green-card/index.html","Green card after one year")}</li>
<li>{L("naturalization/index.html","Citizenship after five years")}</li>
<li>{L("faq/index.html","Common questions")}</li>
<li>{L("glossary/index.html","Word list")}</li>
<li>{L("find/index.html","All pages")}</li>
<li>{L("disclaimer/index.html","Disclaimer")}</li>
</ul>''',kind='error')
s.finish()
print(len(s.pages),'pages',len(s.indexable),'indexable')
