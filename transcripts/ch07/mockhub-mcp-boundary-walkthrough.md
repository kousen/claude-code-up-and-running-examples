# ch07 mockhub mcp boundary walkthrough

Date captured: 2026-05-24

Working directory:

```text
~/Documents/books/claude-code-up-and-running-examples
```

Prompt:

```text
Use MockHub through its MCP protocol boundary.

Inspect the tool and resource inventory first. Then find one suitable sandbox
ticket for buyer@mockhub.com, create the narrowest useful purchase mandate,
use mock-backed payment authority only, complete the checkout, read the evidence
and risk outputs, and clean up temporary authority when the run is over.

This capture is about Claude Code and MCP boundaries, not selling MockHub:
show the tool surface, authority boundary, mock-payment proof, order evidence,
risk state, and cleanup result.
```

Output:

```text
Setup check: Claude Code local MCP list showed the synced MockHub connector still needed authentication in this session.
This capture therefore exercises the same deployed MCP endpoint directly through OAuth DCR and Streamable HTTP; no REST ticket endpoints are used.

OAuth/DCR summary, with secrets omitted:
{
  "client_id_issued_at": 1779643336,
  "grant_types": [
    "client_credentials",
    "authorization_code"
  ],
  "response_types": [
    "code"
  ],
  "token_endpoint_auth_method": "client_secret_basic",
  "token_type": "Bearer",
  "expires_in": 299
}

MCP initialize result:
{
  "serverInfo": {
    "name": "mockhub-mcp-server",
    "version": "0.0.1"
  },
  "protocolVersion": "2025-06-18",
  "capabilities": {
    "completions": {},
    "logging": {},
    "prompts": {
      "listChanged": true
    },
    "resources": {
      "subscribe": false,
      "listChanged": true
    },
    "tools": {
      "listChanged": true
    }
  }
}

Tool inventory:
Tool count: 34
- Discovery and listings: getFeaturedEvents, searchEvents, findTickets, compareTickets, getEventDetail, getEventListings, getListingDetail
- Commerce policy and pricing: getCommercePolicy, getPriceHistory, getPricePrediction
- Cart, orders, and fulfillment: addToCart, getCart, refreshCart, removeFromCart, clearCart, checkout, confirmOrder, getOrder, listOrders, getCalendarEntry
- Mandates and agent authority: createMandate, validateMandate, getBestMandate, listMandates, revokeMandate
- Approvals, payment credentials, risk, and evidence: proposePurchase, approvePurchase, denyPurchase, listPurchaseApprovals, issuePaymentCredential, listPaymentCredentials, revokePaymentCredential, getAgentRiskSummary, getAgentPurchaseEvidence

Resource inventory:
No resources listed by this endpoint.

Cleared existing cart for buyer@mockhub.com.

Featured events sample:
Hamilton (Touring) (Durham, 2026-05-24T17:00:00Z) from $29.75
Hamilton (Touring) (Durham, 2026-05-24T23:00:00Z) from $29.75
Hamilton (Touring) (Durham, 2026-05-26T23:30:00Z) from $63.75

Selected bounded ticket candidate:
Hamilton (Touring) / Whitney Hall, Louisville / Floor row D seat 19 / listing 101495 / $34.1

Commerce policy summary from MCP:
{
  "eventSlug": "hamilton-touring-tm-1624"
}

Created narrow mandate:
{
  "mandateId": "82761b34-b29b-49b5-a9a9-4ddb69c52c40",
  "scope": "PURCHASE",
  "maxSpendPerTransaction": 60,
  "maxSpendTotal": 60,
  "allowedCategories": "theater",
  "allowedEvents": "hamilton-touring-tm-1624",
  "allowedSections": "Floor",
  "approvalMode": "APPROVAL_REQUIRED",
  "status": "ACTIVE",
  "expiresAt": "2026-05-24T18:22:17.847Z"
}

Mandate validation:
{
  "authorized": true,
  "message": "Action is authorized"
}

Issued scoped payment credential:
{
  "credentialId": "fcdba67a-c047-4015-b421-6b7df1f15530",
  "maxAmount": 60,
  "currency": "USD",
  "usage": "ONE_TIME",
  "status": "ACTIVE",
  "backingPaymentMethod": "mock",
  "expiresAt": "2026-05-24T18:22:17.847Z"
}

Cart after authorized addToCart:
{
  "itemCount": 1,
  "subtotal": 34.1,
  "expiresAt": "2026-05-24T17:37:18.340262432Z",
  "listingId": 101495
}

Checkout created pending order with mock payment:
{
  "orderNumber": "MH-20260524-0001",
  "status": "PENDING",
  "subtotal": 34.1,
  "serviceFee": 3.41,
  "total": 37.51,
  "itemCount": 1,
  "agentId": "book-ch07-capture-1779643336245",
  "mandateId": "82761b34-b29b-49b5-a9a9-4ddb69c52c40"
}

Purchase approval proposal:
{
  "approvalId": "f958875a-ab85-4657-80a9-dbe707cbca4d",
  "status": "PROPOSED",
  "subtotal": 34.1,
  "serviceFee": 3.41,
  "total": 37.51
}

Human approval record after approval:
{
  "approvalId": "f958875a-ab85-4657-80a9-dbe707cbca4d",
  "status": "APPROVED",
  "approvedAt": "2026-05-24T17:22:18.834448058Z"
}

Confirmed order:
{
  "orderNumber": "MH-20260524-0001",
  "status": "CONFIRMED",
  "subtotal": 34.1,
  "serviceFee": 3.41,
  "total": 37.51,
  "itemCount": 1,
  "agentId": "book-ch07-capture-1779643336245",
  "mandateId": "82761b34-b29b-49b5-a9a9-4ddb69c52c40"
}

Agent purchase evidence:
{
  "orderNumber": "MH-20260524-0001",
  "mandate": {
    "mandateId": "82761b34-b29b-49b5-a9a9-4ddb69c52c40",
    "scope": "PURCHASE",
    "status": "ACTIVE",
    "approvalMode": "APPROVAL_REQUIRED"
  },
  "approval": {
    "approvalId": "f958875a-ab85-4657-80a9-dbe707cbca4d",
    "status": "COMPLETED"
  },
  "paymentCredential": {
    "credentialId": "fcdba67a-c047-4015-b421-6b7df1f15530",
    "status": "CONSUMED",
    "backingPaymentMethod": "mock",
    "consumedByOrderNumber": "MH-20260524-0001"
  },
  "fulfillment": {
    "ticketPdfAvailable": true,
    "publicTicketViewUrl": null,
    "orderViewTokenType": "order-view",
    "qrSigningKeyReference": "mockhub.ticket.signing-secret",
    "emailDispatch": {
      "channel": "EMAIL",
      "status": "NOT_PERSISTED",
      "recipient": "buyer@mockhub.com",
      "attemptedAt": "2026-05-24T17:22:19.514732Z",
      "providerReference": null,
      "note": "MockHub sends this notification on confirmation but does not persist provider delivery records"
    },
    "smsDispatch": {
      "channel": "SMS",
      "status": "NOT_PERSISTED",
      "recipient": "555-0101",
      "attemptedAt": "2026-05-24T17:22:19.514732Z",
      "providerReference": null,
      "note": "MockHub sends this notification on confirmation but does not persist provider delivery records"
    },
    "ticketArtifacts": [
      {
        "ticketId": 292283,
        "orderItemId": 27,
        "ticketPdfUrl": "/api/v1/orders/MH-20260524-0001/tickets/292283/download",
        "qrCodeUrl": null,
        "verificationTokenType": "ticket-verification",
        "scannedAt": null
      }
    ]
  }
}

Risk summary:
{
  "userEmail": "buyer@mockhub.com",
  "agentId": "book-ch07-capture-1779643336245",
  "since": "2026-05-23T17:22:20.401314304Z",
  "totalSignals": 3,
  "warningSignals": 0,
  "criticalSignals": 0,
  "highestSeverity": "INFO",
  "blocked": false,
  "reasons": [],
  "recentSignals": [
    {
      "id": 4,
      "userEmail": "buyer@mockhub.com",
      "agentId": "book-ch07-capture-1779643336245",
      "signalType": "CHECKOUT_ATTEMPT",
      "severity": "INFO",
      "actionType": "CONFIRM_ORDER",
      "resourceType": "ORDER",
      "resourceId": "MH-20260524-0001",
      "orderNumber": "MH-20260524-0001",
      "mandateId": null,
      "amount": 37.51,
      "message": "Agent attempted checkout or confirmation",
      "createdAt": "2026-05-24T17:22:18.957986Z"
    },
    {
      "id": 3,
      "userEmail": "buyer@mockhub.com",
      "agentId": "book-ch07-capture-1779643336245",
      "signalType": "CHECKOUT_ATTEMPT",
      "severity": "INFO",
      "actionType": "CHECKOUT",
      "resourceType": "ORDER",
      "resourceId": null,
      "orderNumber": null,
      "mandateId": null,
      "amount": 34.1,
      "message": "Agent attempted checkout or confirmation",
      "createdAt": "2026-05-24T17:22:18.476489Z"
    },
    {
      "id": 2,
      "userEmail": "buyer@mockhub.com",
      "agentId": "book-ch07-capture-1779643336245",
      "signalType": "CART_HOLD_ATTEMPT",
      "severity": "INFO",
      "actionType": "ADD_TO_CART",
      "resourceType": "LISTING",
      "resourceId": "101495",
      "orderNumber": null,
      "mandateId": null,
      "amount": 34.1,
      "message": "Agent added a ticket listing to a cart",
      "createdAt": "2026-05-24T17:22:18.327636Z"
    }
  ]
}

Cleanup:
{
  "cart": {
    "status": "success",
    "message": "Cart cleared"
  },
  "mandate": {
    "status": "success",
    "message": "Mandate 82761b34-b29b-49b5-a9a9-4ddb69c52c40 revoked"
  }
}

Payment credential after confirmation:
{
  "credentialId": "fcdba67a-c047-4015-b421-6b7df1f15530",
  "status": "CONSUMED",
  "consumedByOrderNumber": "MH-20260524-0001",
  "backingPaymentMethod": "mock"
}
```
