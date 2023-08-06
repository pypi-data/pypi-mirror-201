# lago-billing

<!-- Start SDK Installation -->
## SDK Installation

```bash
pip install lago-billing
```
<!-- End SDK Installation -->

## SDK Example Usage
<!-- Start SDK Example Usage -->
```python
import sdk
from sdk.models import operations, shared

s = sdk.SDK(
    security=shared.Security(
        bearer_auth="Bearer YOUR_BEARER_TOKEN_HERE",
    ),
)


req = operations.FindInvoiceRequest(
    id="1a901a90-1a90-1a90-1a90-1a901a901a90",
)
    
res = s.invoices.find(req)

if res.invoice is not None:
    # handle response
```
<!-- End SDK Example Usage -->

<!-- Start SDK Available Operations -->
## Available Resources and Operations


### add_ons

* `apply` - Apply an add-on to a customer
* `create` - Create a new add-on
* `destroy` - Delete an add-on
* `find` - Find add-on by code
* `find_all` - Find add-ons
* `update` - Update an existing add-on

### billable_metrics

* `create` - Create a new billable metric
* `destroy` - Delete a billable metric
* `find` - Find billable metric by code
* `find_all` - Find Billable metrics
* `find_all_groups` - Find Billable metric groups
* `update` - Update an existing billable metric

### coupons

* `applied_coupons` - Find Applied Coupons
* `apply` - Apply a coupon to a customer
* `create` - Create a new coupon
* `destroy` - Delete a coupon
* `find` - Find coupon by code
* `find_all` - Find Coupons
* `update` - Update an existing coupon

### credit_notes

* `create` - Create a new Credit note
* `download` - Download an existing credit note
* `find` - Find credit note
* `find_all` - Find Credit notes
* `update` - Update an existing credit note
* `void` - Void existing credit note

### customers

* `create` - Create a customer
* `current_usage` - Find customer current usage
* `delete_applied_coupon` - Delete customer's appplied coupon
* `destroy` - Delete a customer
* `find` - Find customer by external ID
* `find_all` - Find customers
* `portal_url` - Get customer portal URL

### events

* `estimate_fees` - Estimate fees for an instant charge
* `batch_create` - Create batch events
* `create` - Create a new event
* `find` - Find event by transaction ID

### fees

* `find` - Find fee by ID
* `find_all` - Find all fees
* `update` - Update an existing fee

### invoices

* `download` - Download an existing invoice
* `finalize` - Finalize a draft invoice
* `find` - Find invoice by ID
* `find_all` - Find all invoices
* `retry` - Retry invoice payment
* `update` - Update an existing invoice status
* `void` - Refresh a draft invoice

### organizations

* `update` - Update an existing Organization

### plans

* `create` - Create a new plan
* `destroy` - Delete a plan
* `find` - Fin plan by code
* `find_all` - Find plans
* `update` - Update an existing plan

### subscriptions

* `create` - Assign a plan to a customer
* `destroy` - Terminate a subscription
* `find_all` - Find subscriptions
* `update` - Update an existing subscription

### wallets

* `create` - Create a new wallet
* `create_transaction` - Create a new wallet transaction
* `destroy` - Delete a wallet
* `find` - Find wallet
* `find_all` - Find wallets
* `find_all_transactions` - Find wallet transactions
* `update` - Update an existing wallet

### webhooks

* `fetch_public_key` - Fetch webhook public key
<!-- End SDK Available Operations -->

### Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

### Contributions

While we value open-source contributions to this SDK, this library is generated programmatically.
Feel free to open a PR or a Github issue as a proof of concept and we'll do our best to include it in a future release !

### SDK Created by [Speakeasy](https://docs.speakeasyapi.dev/docs/using-speakeasy/client-sdks)
