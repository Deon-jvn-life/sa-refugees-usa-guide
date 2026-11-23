"""Sending money between South Africa and the United States.

Visitor-facing provider links live in PROVIDER_LINKS only.
Replace a url there when an affiliate link exists. Do not point the
source citations at an affiliate url. The links below are ordinary
provider pages. No affiliate programme is connected.
"""

PROVIDER_LINKS={
    "bank":"https://www.standardbank.co.za/southafrica/personal/products-and-services/bank-with-us/foreign-exchange/international-payments",
    "wise":"https://wise.com/",
    "worldremit":"https://www.worldremit.com/",
    "remitly":"https://www.remitly.com/",
    "westernunion":"https://www.westernunion.com/",
    "xe":"https://www.xe.com/",
    "mukuru":"https://www.mukuru.com/sa/send-money/united-states-of-america/",
}

EXTRA_SOURCES={
    "sarb_circ7":"https://www.resbank.co.za/content/dam/sarb/what-we-do/financial-surveillance/financial-surveillance-documents/2026/7-2026.pdf",
    "wise_zar":"https://wise.com/help/articles/2932359/guide-to-zar-transfers",
    "wise_fees":"https://wise.com/help/articles/2522717/fees-for-sending-money",
    "wr_fromza":"https://www.worldremit.com/en/faq/send-from/africa/south-africa",
    "wr_toza":"https://www.worldremit.com/en-us/south-africa",
    "remitly_toza":"https://www.remitly.com/us/en/money-transfer/send-money-to-south-africa",
    "wu_toza":"https://www.westernunion.com/us/en/send-money-to-south-africa.html",
    "wu_fromza":"https://www.westernunion.com/za/en/send-money.html",
    "xe_toza":"https://www.xe.com/en-us/send-money/send-money-to-south-africa/from-united-states/",
    "xe_zar":"https://help.xe.com/hc/en-gb/articles/360019906957-Sending-South-African-Rand-ZAR",
    "mukuru_usa":"https://www.mukuru.com/sa/send-money/united-states-of-america/",
    "sb_pay":"https://www.standardbank.co.za/southafrica/personal/products-and-services/bank-with-us/foreign-exchange/international-payments",
    "sb_brochure":"https://www.standardbank.co.za/static_file/South%20Africa/PDF/SB_International_Payments_Brochure_interactive_final.pdf",
}

CHECKED="23 November 2026"

def add_page(P, L, a, src, S):
    def go(key, label):
        return a(PROVIDER_LINKS[key], label)
    f='sending-money/index.html'
    rows=[
        ("bank","Standard Bank",
         "The brochure gives US dollars as an example of an outward payment to an account outside South Africa. The payment is a telegraphic transfer on SWIFT. The United States is not named.",
         "Not stated as a country. The same pages describe an inward international payment into a Standard Bank account. They do not say Standard Bank sends money from the United States.",
         "The app shows the exchange rate and the transaction costs before you pay. Commission is described as a small percentage. A SWIFT fee is charged. The percentage, and the SWIFT fee in rand, are not stated. The receiving bank's fee varies, and Standard Bank says that amount is not known to it.",
         "An outward payment is processed within 2 business days. How long an inward payment takes to reach the bank is not stated. After the funds arrive, you have 30 calendar days to process the receipt.",
         ("sb_brochure","sb_pay")),
        ("wise","Wise",
         "No. Wise says you can't currently send from rand.",
         "Yes, to a bank account in South Africa. The guide does not name the United States as the country you pay from. The limit on that guide is the equivalent of 1 million British pounds.",
         "Wise says the fee is a percentage of the amount. The percentage changes by currency. A small transfer has a minimum fee instead. How you pay can change the cost. You get the mid-market rate, and Wise says it does not mark that rate up. The rand percentage is not stated on the rand guide. You see the cost when you set the transfer up. A same-currency transfer between Wise accounts is free.",
         "To a rand account: usually 0 to 1 working day after Wise has the money and has converted it. Conversion can take up to 2 working days. Wise shows an estimate when you set the transfer up. A time for sending from rand is not stated, because that guide says you can't currently send from rand.",
         ("wise_zar","wise_fees")),
        ("mukuru","Mukuru",
         "Yes. The South Africa page says you can send to any bank account in the United States. A new customer who registered with a South African identity document can send up to R1 000 000. That figure is Mukuru's own limit. It is not the Reserve Bank allowance.",
         "Not stated.",
         "The page says the pricing is transparent, with no hidden charges, and that the exchange rates are competitive. A fee amount, and how the rate is set, are not stated.",
         "The page says transfers are sent in minutes to a bank account in the United States.",
         ("mukuru_usa",)),
        ("remitly","Remitly",
         "Not stated. The page checked is for sending from the United States to South Africa.",
         "Yes. Delivery on that page can be a bank deposit, cash pickup, or a debit card deposit.",
         "The page says the cost varies with the amount, the way you pay, and the delivery option, and that there are no hidden fees. You see the total when you enter the transfer. A new customer can be offered no fee, and a promotional rate, on the first 1,000 US dollars. This guide does not copy that rate. It changes.",
         "Not stated as one time. The page says many transfers arrive quickly, and that Express with a debit or credit card is the fastest where that option is offered. The exact speed is shown when you enter the transfer.",
         ("remitly_toza",)),
        ("westernunion","Western Union",
         "Not stated. The South Africa send page says a receiver can collect at a participating agent worldwide, generally within minutes. It does not name the United States. On that page the maximum principal is R30 000, and also 8,000 US dollars per person per day.",
         "Yes, including cash pickup. The US page's maximum for cash pickup to South Africa is 677.07 US dollars. You can pay from a bank account, a credit card, or a debit card.",
         "The US page says to check the price estimator for any transfer fees and for the latest dollar to rand rate. It also says Western Union makes money from the currency exchange. A fixed fee is not stated on the page.",
         "Cash pickup from the United States: within minutes, subject to agent hours and time zones. A time for other delivery methods is not stated. From South Africa, the page says money is generally available for pickup within minutes. It does not tie that sentence to the United States.",
         ("wu_fromza","wu_toza")),
        ("worldremit","WorldRemit",
         "Not stated. The send-from-South-Africa page says you can send to 130 or more destinations. It does not name the United States. The maximum on that page is 4,999 rand per transfer and 24,999 rand per month, whether you pay by card or from a bank account.",
         "Yes. You pay in US dollars and the receiver gets rand. Receive methods on the page include a bank transfer, cash pickup, and mobile money.",
         "The US-to-South-Africa page says you see the fees and the exchange rate up front. The transfer fee depends on the receive method and does not vary with the amount. A fee in rand or dollars is not stated.",
         "Cash pickup: the page says funds are sent to local partners in South Africa within minutes, and are then ready to collect. Paying by card is described as faster. A time for a bank deposit is not stated. The page says the actual time can differ.",
         ("wr_fromza","wr_toza")),
        ("xe","Xe",
         "Not stated. The Xe help page on sending rand says South African users are directed to Ria Money Transfers. It does not describe a transfer from South Africa to the United States.",
         "Yes. The page is for sending from the United States to a bank account in South Africa. Online, the page says you can send up to 535,000 US dollars.",
         "The page says there are no hidden fees and it shows the day's rate. A bank transfer may have 0.00 in additional transfer fees. This guide does not copy the rate. It changes. A full fee formula is not stated.",
         "The same page gives more than one time. It says a bank deposit can arrive in minutes, that the transfer can take from minutes up to 3 business days, and, in a later answer, that you should allow 1 to 4 working days. It says you see a closer estimate before you confirm.",
         ("xe_toza","xe_zar")),
    ]
    def cell(text, keys):
        return text+src(*keys)
    body=['<tr><th scope="col">Service</th><th scope="col">South Africa to the US</th>'
          '<th scope="col">US to South Africa</th><th scope="col">Fees and exchange rate</th><th scope="col">Speed</th></tr>']
    for key,label,sa,us,fees,speed,keys in rows:
        body.append('<tr><th scope="row">'+go(key,label)+'</th><td>'+cell(sa,keys)+'</td><td>'+cell(us,keys)+'</td><td>'+cell(fees,keys)+'</td><td>'+cell(speed,keys)+'</td></tr>')
    table=''.join(body)
    P(f,"Sending money from South Africa to the USA and back",
      "Plain-language SARB and SARS rules for sending money abroad, and what each company's page says about South Africa and the United States.",
      f'''<p class="disclose">Some links on this page may earn us a fee. It does not change what you pay or what we recommend.</p>
<h1>Sending money between South Africa and the United States</h1>
<p>This page is the short version: the allowance rules, then what each service's own page says about the two directions. Retirement funds, and the year you stop being a South African tax resident, are on {L("moving-money/index.html","Moving money and pensions",f)}. Reports of foreign accounts are on {L("foreign-accounts/index.html","Reporting SA accounts",f)}.</p>
<p>This is general information for information purposes only. It is not legal advice and it is not tax advice. A bank and a practitioner apply the rules to your own transfer.</p>
<h2>Which way each service sends</h2>
<div class="card"><p>The table uses only the pages linked in each row. They were read on {CHECKED}. Where a page does not say, the cell says not stated. A fee or a rate that the page does not print is left out. Compare the quote the service shows you on the day you send.</p>
<p>The order is not a ranking and it is not a commission. Standard Bank and Wise come first because their pages say something about both directions. The other names are alphabetical.</p>
<p>The bank row is Standard Bank's own international-payments page, as one worked example. Another bank publishes its own fees and times. The name of each service is the link a reader follows. Those addresses are kept in one list so a tracking link can be swapped in later. The small source links stay on the page that was read.</p></div>
<div class="wrap"><table class="compare"><caption>What each service's own page said on {CHECKED}. Swipe sideways on a small screen.</caption>{table}</table></div>
<h2>The allowance rules, in plain language</h2>
<div class="card"><p>Two limits matter for a South African resident who wants to send money out. The Reserve Bank's public pages do not all print the same rand amount for the first one. Read the conflict box before you use either number at a bank{src("sarb_circ","sarb_circ7","sarb_guide","sarb_faq")}.</p>
<h3>Single discretionary allowance</h3>
<p>This is the amount a resident adult can send abroad in a calendar year for any legal purpose, including an investment. Gifts of cash are included. Gold and jewellery are not. You do the sending through an authorised dealer, which is a bank allowed to deal in foreign exchange{src("sarb_faq","sarb_guide","sarb_circ")}.</p>
<p>You show the bank a valid green bar-coded South African identity document or a smart identity card. The questions page says you do not have to give the bank documentary evidence for this allowance, except when you use it for travel outside the Common Monetary Area (South Africa, eSwatini, Lesotho and Namibia). For travel, you produce a ticket. The same page says this allowance does not need a SARS tax compliance status{src("sarb_faq","sarb_guide")}.</p>
<p>The rand amount is the part the documents do not agree on. It is in the box below. Do not pick a number from memory{src("sarb_circ","sarb_guide","sarb_faq")}.</p>
<h3>Foreign capital allowance, and the SARS PIN</h3>
<p>A separate allowance is for investment abroad. The Reserve Bank calls it a foreign capital allowance of up to R10 million per calendar year. Circular 12/2025 says an authorised dealer may transfer that amount, for a person of 18 or older who is a taxpayer in good standing, via an AIT. The circular defines AIT as "Approval International Transfer"{src("sarb_circ12","sarb_guide","sarb_faq")}.</p>
<p>The circular says SARS issues a tax compliance status PIN letter. It shows the tax number and the PIN. The bank uses the PIN on SARS eFiling to check that you are tax compliant before it sends the money. The bank must not send more than the amount SARS approved. The PIN can expire. If it has expired, the bank must ask for a new one. If the status says you are not compliant, the bank should not transfer the money{src("sarb_circ12")}.</p>
<p>SARS's own page for this step is titled Approval of International Transfers (AIT). The section you need is "Supporting documents for TCS for foreign investment allowance". SARS uses the words "foreign investment allowance". The Reserve Bank uses "foreign capital allowance". The SARS page lists the papers: something that shows where the money came from, a statement of assets and liabilities for the previous three tax years, and a power of attorney if someone else submits the application. The page does not, in that section, print the R10 million cap. The cap above is from the Reserve Bank{src("sars_ait","sarb_circ12")}.</p>
<p>More than R10 million in a calendar year is a further application. The bank sends it to the Reserve Bank's Financial Surveillance Department, with the tax compliance result. Circular 12/2025 says that application is also via an AIT, and that SARS does a stricter check{src("sarb_faq","sarb_circ12")}.</p>
<p>Stopping South African tax residence, retirement-fund withdrawals, and what a non-resident may send are a different set of rules. They are on {L("moving-money/index.html","Moving money and pensions",f)} and {L("sa-tax-residency/index.html","SA tax residency",f)}{src("sarb_guide","sars_ait")}.</p></div>
<h2>Where the rand amounts disagree</h2>
<div class="card conf"><ul>
<li><strong>Single discretionary allowance: R1 million or R2 million.</strong> Exchange Control Circular No. 6/2026, dated 8 April 2026, says the allowance for a resident of 18 or older was R1 million and is increased to R2 million from the date of the circular. Circular No. 7/2026, the same day, raises the same limit in the manual for authorised dealers with limited authority (the bureaux and money-transfer dealers). The Currency and Exchanges Guidelines for Individuals, dated 7 January 2026 on the PDF in the 2026 folder, still print R1 million. The Financial Surveillance questions page still said R1 million when it was read on {CHECKED}. This guide does not pick a winner. Show the bank all four Reserve Bank documents{src("sarb_circ","sarb_circ7","sarb_guide","sarb_faq")}.</li>
<li><strong>Travel allowance under 18.</strong> The questions page still says a resident under 18 may have a travel allowance of up to R200 000 per calendar year, and may not use the adult single discretionary allowance. Circulars 6/2026 and 7/2026 raise that travel allowance to R400 000 in the dealer manuals. The January guidelines were not reissued with the new figure. Same conflict. Do not pick a number{src("sarb_faq","sarb_circ","sarb_circ7","sarb_guide")}.</li>
<li><strong>A bank page prints R2 million.</strong> Standard Bank's international payments page tells customers the single discretionary allowance on that page is up to R2 million per calendar year. That is a bank page, not a Reserve Bank page. It matches the April circulars and not the questions page or the January guidelines. It does not settle the conflict{src("sb_pay","sarb_circ","sarb_faq","sarb_guide")}.</li>
<li><strong>The name of the approval.</strong> Circular 12/2025 writes "Approval International Transfer". The SARS page title writes "Approval of International Transfers". Both use the short name AIT{src("sarb_circ12","sars_ait")}.</li>
</ul></div>
<h2>What to watch</h2>
<div class="card warn"><p>The allowance is yours. The questions page says you may not use another person's single discretionary allowance or foreign capital allowance by calling it a loan, or by a similar agreement. The Reserve Bank calls that a simulated transaction and an illegal one{src("sarb_faq")}.</p>
<p>Use the company's own site, not a message from a stranger. Read the quote before you pay. This page does not list a fee that was not on the company's page on {CHECKED}.</p></div>
<h2>Sources</h2>
<div class="card"><p>Read on {CHECKED}.</p>
<ul>
<li>Reserve Bank, Exchange Control Circular No. 6/2026 (8 April 2026): {a(S["sarb_circ"],"PDF")}</li>
<li>Reserve Bank, Exchange Control Circular No. 7/2026 (8 April 2026): {a(S["sarb_circ7"],"PDF")}</li>
<li>Reserve Bank, Currency and Exchanges Guidelines for Individuals (PDF dated 7 January 2026): {a(S["sarb_guide"],"PDF")}</li>
<li>Reserve Bank, Financial Surveillance questions: {a(S["sarb_faq"],"questions page")}</li>
<li>Reserve Bank, Exchange Control Circular No. 12/2025 (19 June 2025): {a(S["sarb_circ12"],"PDF")}</li>
<li>SARS, supporting documents for Approval of International Transfers: {a(S["sars_ait"],"AIT page")}</li>
<li>Standard Bank, international payments, and the international payments brochure: {a(S["sb_pay"],"payments page")}, {a(S["sb_brochure"],"brochure PDF")}</li>
<li>Wise, guide to rand transfers, and fees for sending money: {a(S["wise_zar"],"rand guide")}, {a(S["wise_fees"],"fees")}</li>
<li>Mukuru, send money to the United States from South Africa: {a(S["mukuru_usa"],"Mukuru page")}</li>
<li>Remitly, send money to South Africa from the United States: {a(S["remitly_toza"],"Remitly page")}</li>
<li>Western Union, send from South Africa, and send to South Africa from the US: {a(S["wu_fromza"],"South Africa page")}, {a(S["wu_toza"],"US page")}</li>
<li>WorldRemit, sending from South Africa, and sending to South Africa from the US: {a(S["wr_fromza"],"from South Africa")}, {a(S["wr_toza"],"to South Africa")}</li>
<li>Xe, send to South Africa from the United States, and the rand help page: {a(S["xe_toza"],"US to South Africa")}, {a(S["xe_zar"],"rand help")}</li>
</ul></div>''')
