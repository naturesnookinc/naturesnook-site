"""Turn pickup ordering on.  Usage:  python3 tools/pickup/golive.py https://script.google.com/macros/s/.../exec
Sets the order endpoint in index.html and updates the privacy, cookie and terms pages to match.
Run it only after the Apps Script web app is deployed and a test order has landed in the sheet.
Then run the smoke test, commit and push (policy pages and the feature go out together)."""
import sys, re, datetime, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
url = sys.argv[1] if len(sys.argv) > 1 else ''
assert re.match(r'^https://script\.google\.com/macros/s/[\w-]+/exec$', url), 'pass the full Apps Script web app URL (ends in /exec)'
today = datetime.date.today().strftime('%B %-d, %Y')

def edit(path, pairs):
    s = open(ROOT + path, encoding='utf-8').read()
    for old, new in pairs:
        assert old in s, f'{path}: text not found: {old[:60]}'
        s = s.replace(old, new, 1)
    s = re.sub(r'Last updated [A-Z][a-z]+ \d+, \d{4}', 'Last updated ' + today, s, count=1)
    open(ROOT + path, 'w', encoding='utf-8').write(s)

edit('index.html', [('endpoint:""', f'endpoint:"{url}"')])

edit('privacy/index.html', [
 ("The site has no accounts, forms, analytics or advertising trackers.", "The site has no accounts, analytics or advertising trackers. Its only form is the optional pickup order form."),
 ("<li>This website is a catalog and store information page. It has no accounts, no sign-up or contact forms, no online ordering and no payments.</li>",
  "<li>This website is a catalog and store information page with an optional pickup order form. It has no accounts and takes no online payments.</li>"),
 ("<li>We do not ask for or collect your name, email, phone number or address through this website.</li>",
  "<li>We collect your name, mobile number and order only if you send us a pickup order. We do not otherwise ask for or collect your name, email, phone number or address through this website.</li>"),
 ("<li>We do not sell or share personal information from this website, because we don't collect any.</li>",
  "<li>We do not sell personal information. A pickup order is shared only with the Google tools that store it for us, as described below.</li>"),
 ("<p>None. The search box filters", """<p>Only if you send a pickup order. Then we collect the name and mobile number you type, the products you chose, and any note you add. We use them to prepare your order and to text or call you about it. If you check the box, we may text the number you gave about that order only, never for advertising. Message and data rates may apply, and you can reply STOP to opt out.</p>
<p>The order is saved in a Google Sheet that belongs to Nature's Nook (using Google Apps Script) and emailed to the store, so Google processes it for us under its own <a href="https://policies.google.com/privacy">privacy policy</a>. Only store staff can open the sheet. We delete pickup orders after 90 days. To see, correct or delete an order sooner, call us at (208) 356-5284.</p>
<p>The search box filters"""),
])

edit('cookies/index.html', [
 ("<h2>Outside services the site loads</h2>", "<p>The pickup order form does not use cookies or browser storage. Your order list is kept in the page's memory only, until you send the order, close the page or reload it.</p>\n<h2>Outside services the site loads</h2>"),
 ("<p>If you click a link to Google Maps", "<p>When you send a pickup order, your browser sends it to Google (Google Apps Script), which stores it for us. See the <a href=\"/privacy/\">privacy policy</a>.</p>\n<p>If you click a link to Google Maps"),
])

edit('terms/index.html', [
 ("You can't buy anything through the site. All sales happen in the store.", "You can send us a pickup order through the site, but you don't pay online. All sales happen in the store."),
 ("<h2>Member deals, coupons and sales</h2>", """<h2>Pickup orders</h2>
<p>A pickup order is a request, not a sale. We confirm what is in stock by text or phone, and you pay in the store at pickup. Prices shown on the site may differ from the price at the register, and the register price applies. We may change or cancel a request if a product is not available. Our <a href="/returns/">return policy</a> applies to pickup purchases.</p>
<h2>Member deals, coupons and sales</h2>"""),
])
print('Pickup ordering is ON. Next: smoke test, commit, push.')
