# Pickup ordering

Customers add products to a pickup order on naturesnook.co and send their name and mobile number.
Each order lands as a row in a Google Sheet and an email to the store. Staff confirm and text the customer from GoTo.
Payment happens in the store. The feature is **dormant** (nothing shows on the site) until go-live.

## Files
- `pickup.css`, `pickup.js` - the front end that is already inside `index.html` (kept here as the readable source)
- `Code.gs` - the Google Apps Script that receives orders
- `golive.py` - sets the endpoint and updates the privacy, cookie and terms pages in one step

## Go-live checklist (owner steps 1-4, then Claude)
1. Create a new Google Sheet named "Pickup Orders" (in the store's Google account).
2. In the sheet: Extensions > Apps Script. Delete the sample code, paste all of `Code.gs`, save.
3. Project Settings > Script Properties > add `STORE_EMAIL` = the address that should get each order.
4. Deploy > New deployment > type "Web app": Execute as **Me**, Who has access **Anyone**. Authorize when asked.
   Copy the Web app URL (ends in `/exec`) and send it to Claude. Optional: Triggers > add `purgeOld`, time-driven, daily (deletes orders after 90 days, which the privacy page promises).
5. Claude runs `python3 tools/pickup/golive.py <URL>`, tests with a real order, then commits and pushes.
6. Decide in store: who watches the sheet/email, how fast orders get answered (and say so in a post), and the pickup hours if different from store hours.

## Texting
Phase 1 (this build): staff text the customer from the GoTo app, as the store already does.
The customer ticks a consent box ("text me about this order only, rates may apply, reply STOP"), which is stored with the order.
Phase 2 (optional later): automatic confirmation texts through the GoTo messaging API. That needs the GoTo OAuth client ID and secret
and the texting number. **These go in Apps Script Script Properties, never in this public repo or in `index.html`.**
Check that the number is registered for business texting (carrier 10DLC rules) before turning on automatic messages.

## Rules (see CLAUDE.md)
- Policy pages must say what the form collects before it is live; `golive.py` does that edit together with the switch.
- Keep the order list in page memory only (no cookies, no localStorage).
- Never add payments here without updating the policies and terms first.
