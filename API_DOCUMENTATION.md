# Backend-AI API Documentation

## Overview
This is a Flask-based REST API for a cryptocurrency wallet application built on **Scroll Sepolia Testnet**. The API provides comprehensive functionality for user management, wallet operations, blockchain transactions, AI-powered chat assistance, and real-time cryptocurrency pricing through Pyth Network integration.

**Base URL:** `http://127.0.0.1:5000`  
**Network:** Scroll Sepolia Testnet (Chain ID: 534351)  
**RPC Endpoint:** `https://sepolia-rpc.scroll.io`  
**Block Explorer:** `https://sepolia.scrollscan.com`

---

## Table of Contents
1. [User Management Endpoints](#user-management-endpoints)
2. [Contact Management Endpoints](#contact-management-endpoints)
3. [Contact Wallets Endpoints](#contact-wallets-endpoints)
4. [Transaction Endpoints](#transaction-endpoints)
5. [Balance Endpoints](#balance-endpoints)
6. [Pyth Network Pricing Endpoints](#pyth-network-pricing-endpoints)
7. [AI Chat Endpoint](#ai-chat-endpoint)
8. [Error Handling](#error-handling)

---

## User Management Endpoints

### 1. Create User
**Endpoint:** `POST /users`  
**Description:** Registers a new user with their wallet address and encrypted private key.

**Request Body:**
```json
{
  "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "nombre_usuario": "John Doe",
  "clave_privada_encriptada": "encrypted_private_key_string"
}
```

**Response (201 Created):**
```json
{
  "message": "Usuario creado exitosamente",
  "user": {
    "id": 123,
    "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "nombre_usuario": "John Doe",
    "created_at": "2025-11-23T10:30:00Z"
  }
}
```

**Use Case:** Initial user registration when creating a new wallet or importing an existing one.

---

### 2. Get User by Wallet Address
**Endpoint:** `GET /users/wallet/<wallet_address>`  
**Description:** Retrieves user information by their Ethereum wallet address.

**URL Parameters:**
- `wallet_address` (string, required): Ethereum wallet address (0x format)

**Example Request:**
```
GET /users/wallet/0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

**Response (200 OK):**
```json
{
  "id": 123,
  "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "nombre_usuario": "John Doe",
  "clave_privada_encriptada": "encrypted_private_key_string",
  "created_at": "2025-11-23T10:30:00Z"
}
```

**Use Case:** User login, profile retrieval, wallet verification.

---

### 3. Update User
**Endpoint:** `PUT /users/<wallet_address>`  
**Description:** Updates user information (username or encrypted private key).

**URL Parameters:**
- `wallet_address` (string, required): Ethereum wallet address

**Request Body (partial updates allowed):**
```json
{
  "nombre_usuario": "John Smith",
  "clave_privada_encriptada": "new_encrypted_key"
}
```

**Response (200 OK):**
```json
{
  "message": "Usuario actualizado exitosamente",
  "user": {
    "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "nombre_usuario": "John Smith"
  }
}
```

**Use Case:** Profile updates, key rotation, username changes.

---

### 4. Delete User
**Endpoint:** `DELETE /users/<wallet_address>`  
**Description:** Permanently deletes a user account and all associated data.

**Response (200 OK):**
```json
{
  "message": "Usuario eliminado exitosamente"
}
```

**Warning:** This action is irreversible and deletes all user data including contacts and transaction history.

---

## Contact Management Endpoints

### 5. Add Contact
**Endpoint:** `POST /users/wallet/<wallet_address>/contacts`  
**Description:** Adds a new contact to a user's contact list.

**URL Parameters:**
- `wallet_address` (string, required): User's wallet address

**Request Body:**
```json
{
  "contact_wallet": "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
  "nombre_contacto": "Alice Smith"
}
```

**Response (201 Created):**
```json
{
  "message": "Contacto agregado exitosamente",
  "contact": {
    "id": 456,
    "contact_wallet": "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
    "nombre_contacto": "Alice Smith"
  }
}
```

**Use Case:** Building a contact list for quick transfers, address book functionality.

---

### 6. Get User Contacts
**Endpoint:** `GET /users/wallet/<wallet_address>/contacts`  
**Description:** Retrieves all contacts associated with a user's wallet.

**Response (200 OK):**
```json
{
  "contacts": [
    {
      "id": 456,
      "contact_wallet": "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
      "nombre_contacto": "Alice Smith",
      "created_at": "2025-11-20T15:00:00Z"
    },
    {
      "id": 457,
      "contact_wallet": "0x1234567890abcdef1234567890abcdef12345678",
      "nombre_contacto": "Bob Johnson",
      "created_at": "2025-11-21T10:30:00Z"
    }
  ]
}
```

**Use Case:** Displaying contact list, populating recipient dropdowns.

---

### 7. Delete Contact
**Endpoint:** `DELETE /users/wallet/<wallet_address>/contacts/<contact_id>`  
**Description:** Removes a specific contact from user's contact list.

**Response (200 OK):**
```json
{
  "message": "Contacto eliminado exitosamente"
}
```

---

## Contact Wallets Endpoints

### 8. Add Contact Wallet
**Endpoint:** `POST /contact-wallets`  
**Description:** Creates a labeled wallet entry. This is separate from the main contacts table and allows users to save wallet addresses with custom names.

**Request Body:**
```json
{
  "nombre_wallet_agregada": "My Savings Wallet",
  "wallet_agregada": "0xabcdef1234567890abcdef1234567890abcdef12",
  "wallet_quien_agrego": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
}
```

**Response (201 Created):**
```json
{
  "message": "Contact wallet agregado exitosamente",
  "contact_wallet": {
    "id": 789,
    "nombre_wallet_agregada": "My Savings Wallet",
    "wallet_agregada": "0xabcdef1234567890abcdef1234567890abcdef12",
    "wallet_quien_agrego": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
  }
}
```

**Use Case:** Multi-wallet management, organizing different wallet addresses with custom labels.

---

### 9. Get Contact Wallets
**Endpoint:** `GET /contact-wallets/<wallet_address>`  
**Description:** Retrieves all contact wallets created by a specific user.

**Response (200 OK):**
```json
{
  "contact_wallets": [
    {
      "id": 789,
      "nombre_wallet_agregada": "My Savings Wallet",
      "wallet_agregada": "0xabcdef1234567890abcdef1234567890abcdef12",
      "created_at": "2025-11-22T08:00:00Z"
    }
  ]
}
```

---

## Transaction Endpoints

### 10. Create Transaction
**Endpoint:** `POST /transactions`  
**Description:** Executes a cryptocurrency transaction on Scroll Sepolia network using Web3.py.

**Request Body:**
```json
{
  "wallet_origen": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "wallet_destino": "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
  "monto": "0.1",
  "clave_privada": "0xprivate_key_here"
}
```

**Response (201 Created):**
```json
{
  "message": "Transacción creada y enviada exitosamente",
  "transaction": {
    "id": 1001,
    "wallet_origen": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "wallet_destino": "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
    "monto": "0.1",
    "hash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    "estado": "pending",
    "created_at": "2025-11-23T12:00:00Z"
  }
}
```

**Technical Details:**
- Uses Web3.py to sign and broadcast transactions
- Automatically calculates gas price and gas limit
- Returns transaction hash for blockchain verification
- Transaction can be tracked on Scroll Sepolia block explorer

**Use Case:** Sending ETH between wallets on Scroll Sepolia testnet.

---

### 11. Get User Transactions
**Endpoint:** `GET /transactions/wallet/<wallet_address>`  
**Description:** Retrieves transaction history for a specific wallet (both sent and received).

**Response (200 OK):**
```json
{
  "transactions": [
    {
      "id": 1001,
      "wallet_origen": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
      "wallet_destino": "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
      "monto": "0.1",
      "hash": "0x1234567890abcdef...",
      "estado": "confirmed",
      "created_at": "2025-11-23T12:00:00Z"
    }
  ]
}
```

---

## Balance Endpoints

### 12. Get Wallet Balance
**Endpoint:** `GET /balance/<wallet_address>`  
**Description:** Retrieves the current ETH balance for a wallet address on Scroll Sepolia network.

**Response (200 OK):**
```json
{
  "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "balance": "1.5",
  "balance_wei": "1500000000000000000",
  "network": "Scroll Sepolia",
  "chain_id": 534351
}
```

**Technical Details:**
- Queries Scroll Sepolia RPC directly using Web3.py
- Returns balance in both ETH (human-readable) and Wei (smallest unit)
- Real-time balance updates

**Use Case:** Displaying wallet balance, checking if user has sufficient funds before transactions.

---

## Pyth Network Pricing Endpoints

### 13. Get Single Cryptocurrency Price
**Endpoint:** `GET /pyth/price/<symbol>`  
**Description:** Fetches real-time price data for a specific cryptocurrency from Pyth Network Hermes API.

**URL Parameters:**
- `symbol` (string, required): Cryptocurrency symbol (eth, btc, usdc, usdt, bnb, sol, matic, avax, ada, doge)

**Example Request:**
```
GET /pyth/price/eth
```

**Response (200 OK):**
```json
{
  "symbol": "ETH",
  "price": 2045.67,
  "price_usd": "$2,045.67",
  "confidence": 0.15,
  "confidence_usd": "±$0.1500",
  "confidence_percentage": "0.007%",
  "volatility": "Very Low",
  "publish_time": 1700736754,
  "publish_timestamp": "2025-11-23 12:05:54 UTC",
  "expo": -8,
  "price_feed_id": "0xff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace"
}
```

**Supported Cryptocurrencies (10 total):**
- ETH (Ethereum)
- BTC (Bitcoin)
- USDC (USD Coin)
- USDT (Tether)
- BNB (Binance Coin)
- SOL (Solana)
- MATIC (Polygon)
- AVAX (Avalanche)
- ADA (Cardano)
- DOGE (Dogecoin)

**Field Descriptions:**
- `price`: Raw price value
- `price_usd`: Formatted USD price with commas
- `confidence`: Price confidence interval (absolute value)
- `confidence_usd`: Confidence interval in dollars (±$X.XX format)
- `confidence_percentage`: Confidence as percentage of price
- `volatility`: Classification based on confidence (Very Low/Low/Moderate/High/Very High)
- `publish_time`: Unix timestamp
- `publish_timestamp`: Human-readable UTC timestamp
- `expo`: Exponent for price calculation (price = raw_price × 10^expo)
- `price_feed_id`: Unique Pyth Network price feed identifier

**Volatility Classification:**
- Very Low: < 0.01%
- Low: 0.01% - 0.1%
- Moderate: 0.1% - 0.5%
- High: 0.5% - 1%
- Very High: > 1%

**Use Case:** Real-time price displays, market data dashboards, price alerts.

---

### 14. Get Multiple Cryptocurrency Prices
**Endpoint:** `GET /pyth/prices`  
**Description:** Fetches prices for multiple cryptocurrencies in a single request.

**Query Parameters:**
- `symbols` (string, optional): Comma-separated list of symbols. If omitted, returns all 10 supported cryptocurrencies.

**Example Requests:**
```
GET /pyth/prices
GET /pyth/prices?symbols=eth,btc,sol
```

**Response (200 OK):**
```json
{
  "prices": [
    {
      "symbol": "ETH",
      "price": 2045.67,
      "price_usd": "$2,045.67",
      "confidence": 0.15,
      "confidence_usd": "±$0.1500",
      "volatility": "Very Low",
      "publish_time": 1700736754
    },
    {
      "symbol": "BTC",
      "price": 37234.89,
      "price_usd": "$37,234.89",
      "confidence": 2.50,
      "confidence_usd": "±$2.5000",
      "volatility": "Low",
      "publish_time": 1700736755
    }
  ],
  "count": 2,
  "timestamp": "2025-11-23T12:05:54Z"
}
```

**Use Case:** Portfolio overview, multi-asset price tracking, market comparison.

---

## AI Chat Endpoint

### 15. AI-Powered Chat Assistant
**Endpoint:** `POST /pyth/chat`  
**Description:** Intelligent chatbot powered by DeepSeek AI that provides cryptocurrency price information, transfer advice, and portfolio analysis. The AI can execute 4 different actions based on natural language queries.

**Request Body:**
```json
{
  "message": "What's the current price of Bitcoin?",
  "portfolio": [
    {
      "symbol": "ETH",
      "amount": 1.5
    },
    {
      "symbol": "BTC",
      "amount": 0.05
    }
  ]
}
```

**Parameters:**
- `message` (string, required): Natural language query
- `portfolio` (array, optional): User's cryptocurrency holdings for portfolio-related queries

---

### AI Action 1: Get Single Price
**Trigger:** Questions about a specific cryptocurrency price

**Example Queries:**
- "What's the price of Ethereum?"
- "How much is BTC right now?"
- "Current SOL price?"

**Response:**
```json
{
  "response": "The current price of Ethereum (ETH) is $2,045.67 USD with a confidence interval of ±$0.15 (0.007%). The volatility is classified as Very Low, indicating stable pricing. This data was published at 2025-11-23 12:05:54 UTC. The price feed is highly reliable with minimal deviation.",
  "action": "get_price",
  "data": {
    "symbol": "ETH",
    "price": 2045.67,
    "price_usd": "$2,045.67",
    "confidence": 0.15,
    "confidence_usd": "±$0.1500",
    "confidence_percentage": "0.007%",
    "volatility": "Very Low",
    "publish_timestamp": "2025-11-23 12:05:54 UTC",
    "expo": -8,
    "price_feed_id": "0xff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace"
  }
}
```

---

### AI Action 2: Get Multiple Prices
**Trigger:** Questions about multiple cryptocurrencies

**Example Queries:**
- "Compare ETH and BTC prices"
- "Show me prices for Ethereum, Bitcoin, and Solana"
- "What are the top 3 crypto prices?"

**Response:**
```json
{
  "response": "Here are the current cryptocurrency prices:\n\nEthereum (ETH): $2,045.67 with ±$0.15 confidence (Very Low volatility)\nBitcoin (BTC): $37,234.89 with ±$2.50 confidence (Low volatility)\nSolana (SOL): $58.23 with ±$0.08 confidence (Low volatility)\n\nAll prices are real-time from Pyth Network oracles with high reliability.",
  "action": "get_multiple_prices",
  "data": {
    "prices": [
      {
        "symbol": "ETH",
        "price": 2045.67,
        "price_usd": "$2,045.67",
        "confidence": 0.15,
        "confidence_usd": "±$0.1500",
        "volatility": "Very Low",
        "publish_time": 1700736754
      },
      {
        "symbol": "BTC",
        "price": 37234.89,
        "price_usd": "$37,234.89",
        "confidence": 2.50,
        "confidence_usd": "±$2.5000",
        "volatility": "Low",
        "publish_time": 1700736755
      },
      {
        "symbol": "SOL",
        "price": 58.23,
        "price_usd": "$58.23",
        "confidence": 0.08,
        "confidence_usd": "±$0.0800",
        "volatility": "Low",
        "publish_time": 1700736756
      }
    ]
  }
}
```

---

### AI Action 3: Transfer Advice
**Trigger:** Questions about making transfers or best time to send crypto

**Example Queries:**
- "Should I transfer ETH now?"
- "Is it a good time to send Bitcoin?"
- "Advise me on transferring 0.5 ETH"

**Response:**
```json
{
  "response": "Based on current market conditions:\n\n📊 Ethereum (ETH): $2,045.67\n🎯 Volatility: Very Low (0.007% confidence)\n⏰ Data freshness: 2025-11-23 12:05:54 UTC\n\n✅ RECOMMENDATION: This is a GOOD time to transfer ETH. The volatility is very low, indicating stable pricing with minimal price fluctuation risk. The tight confidence interval (±$0.15) means the price is reliable and unlikely to change significantly during transaction confirmation.\n\n💡 Additional advice:\n- Gas fees on Scroll Sepolia are typically low\n- Consider transferring during this stable period\n- Monitor for 5-10 minutes to ensure continued stability\n\n⚠️ Note: Always verify recipient address before sending.",
  "action": "transfer_advice",
  "data": {
    "symbol": "ETH",
    "price": 2045.67,
    "price_usd": "$2,045.67",
    "confidence": 0.15,
    "confidence_usd": "±$0.1500",
    "confidence_percentage": "0.007%",
    "volatility": "Very Low",
    "publish_timestamp": "2025-11-23 12:05:54 UTC"
  }
}
```

---

### AI Action 4: Portfolio Calculator
**Trigger:** Questions about portfolio value or analysis (requires portfolio parameter)

**Example Queries:**
- "What's my portfolio worth?"
- "Calculate my holdings value"
- "Analyze my portfolio"

**Request Body:**
```json
{
  "message": "What's my portfolio worth?",
  "portfolio": [
    {
      "symbol": "ETH",
      "amount": 1.5
    },
    {
      "symbol": "BTC",
      "amount": 0.05
    },
    {
      "symbol": "SOL",
      "amount": 10
    }
  ]
}
```

**Response:**
```json
{
  "response": "📊 PORTFOLIO ANALYSIS\n\nTotal Portfolio Value: $6,011.48 USD\n\n💎 Asset Breakdown:\n1. Ethereum (ETH): 1.5 tokens = $3,068.51 (51.04%)\n2. Bitcoin (BTC): 0.05 tokens = $1,861.74 (30.97%)\n3. Solana (SOL): 10 tokens = $582.30 (9.69%)\n\n📈 AI Investment Advice:\nYour portfolio shows a well-balanced distribution with strong exposure to top-tier assets. The 51% ETH allocation provides solid DeFi exposure, while 31% BTC offers stability. Consider the following:\n\n✅ Strengths:\n- Good diversification across major networks\n- Balanced risk profile with large-cap dominance\n- SOL provides growth potential\n\n💡 Recommendations:\n- Current volatility levels are Very Low to Low across all assets\n- This is an optimal period for rebalancing if needed\n- Consider taking profits on ETH if it represents >50% of portfolio\n- Monitor BTC dominance trends\n\n⚠️ Risk Assessment: LOW to MODERATE\nConfidence intervals are tight across all holdings, indicating stable pricing.",
  "action": "calculate_portfolio",
  "data": {
    "portfolio_items": [
      {
        "symbol": "ETH",
        "amount": 1.5,
        "price": 2045.67,
        "value_usd": 3068.51,
        "percentage": 51.04,
        "volatility": "Very Low"
      },
      {
        "symbol": "BTC",
        "amount": 0.05,
        "price": 37234.89,
        "value_usd": 1861.74,
        "percentage": 30.97,
        "volatility": "Low"
      },
      {
        "symbol": "SOL",
        "amount": 10,
        "price": 58.23,
        "value_usd": 582.30,
        "percentage": 9.69,
        "volatility": "Low"
      }
    ],
    "total_value_usd": 6011.48,
    "timestamp": "2025-11-23T12:05:54Z"
  }
}
```

**Portfolio Calculation Details:**
- Fetches real-time prices for all holdings
- Calculates USD value for each position
- Computes percentage allocation
- Generates AI-powered investment advice considering:
  - Diversification score
  - Volatility levels
  - Market conditions
  - Risk assessment
  - Rebalancing recommendations

---

## Error Handling

### Standard Error Response Format
```json
{
  "error": "Error message describing what went wrong",
  "details": "Additional technical details (optional)"
}
```

### Common HTTP Status Codes

**400 Bad Request**
- Missing required fields
- Invalid data format
- Malformed wallet addresses

**404 Not Found**
- User not found
- Contact not found
- Transaction not found
- Invalid cryptocurrency symbol

**500 Internal Server Error**
- Database connection failures
- Web3 provider errors
- Pyth Network API unavailable
- AI service errors

**Example Error Responses:**

```json
{
  "error": "Usuario no encontrado"
}
```

```json
{
  "error": "Símbolo no soportado. Símbolos válidos: eth, btc, usdc, usdt, bnb, sol, matic, avax, ada, doge"
}
```

```json
{
  "error": "Error al obtener precio de Pyth Network",
  "details": "Connection timeout to Hermes API"
}
```

---

## Technical Architecture

### Blockchain Integration
- **Network:** Scroll Sepolia Testnet
- **Library:** Web3.py v6.x
- **RPC Provider:** `https://sepolia-rpc.scroll.io`
- **Transaction Signing:** Local signing with private keys
- **Gas Management:** Automatic gas price estimation

### Database
- **Type:** Supabase (PostgreSQL)
- **Tables:**
  - `users`: User accounts and encrypted keys
  - `contacts`: User contact lists
  - `contact_wallets`: Labeled wallet addresses
  - `transacciones`: Transaction history

### External APIs
- **Pyth Network Hermes:** Real-time cryptocurrency oracle data
  - Base URL: `https://hermes.pyth.network`
  - Endpoint: `/v2/updates/price/latest`
  - 10 supported price feeds
- **DeepSeek AI:** Natural language processing for chatbot
  - Model: `deepseek-chat`
  - Function calling support for tool integration

### Security Considerations
- Private keys are never stored in plaintext
- All keys must be encrypted client-side before sending
- CORS enabled for cross-origin requests
- Input validation on all endpoints
- SQL injection prevention through Supabase client

---

## Usage Examples

### Complete User Flow Example

**Step 1: Create User**
```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "nombre_usuario": "Alice",
    "clave_privada_encriptada": "encrypted_key_123"
  }'
```

**Step 2: Check Balance**
```bash
curl http://127.0.0.1:5000/balance/0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

**Step 3: Get ETH Price**
```bash
curl http://127.0.0.1:5000/pyth/price/eth
```

**Step 4: Ask AI for Transfer Advice**
```bash
curl -X POST http://127.0.0.1:5000/pyth/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Should I transfer 0.5 ETH now?"
  }'
```

**Step 5: Execute Transfer**
```bash
curl -X POST http://127.0.0.1:5000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "wallet_origen": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "wallet_destino": "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
    "monto": "0.5",
    "clave_privada": "0xprivate_key_here"
  }'
```

---

## Rate Limits & Performance

- **Pyth Network API:** No strict rate limits, but recommended < 100 requests/minute
- **Database Queries:** Optimized with indexes on wallet addresses
- **Blockchain RPC:** Scroll Sepolia public RPC has no strict limits but may throttle heavy usage
- **AI Chat:** Depends on DeepSeek API key tier

---

## Development & Deployment

### Local Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SUPABASE_URL="your_supabase_url"
export SUPABASE_KEY="your_supabase_key"
export DEEPSEEK_API_KEY="your_deepseek_key"

# Run server
python app.py
```

### Environment Variables Required
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase anonymous/service key
- `DEEPSEEK_API_KEY`: DeepSeek AI API key

### Dependencies
- Flask
- Flask-CORS
- Web3.py
- Supabase-py
- Requests
- Python-dotenv

---

## Support & Resources

- **Scroll Sepolia Faucet:** Get test ETH for development
- **Pyth Network Docs:** https://docs.pyth.network
- **Scroll Documentation:** https://docs.scroll.io
- **Supabase Docs:** https://supabase.com/docs

---

## Version History

**Version 1.0** (Current)
- Initial release with Scroll Sepolia integration
- 15 REST endpoints
- Pyth Network oracle integration (10 cryptocurrencies)
- AI chatbot with 4 action types
- Full CRUD for users, contacts, and transactions
- Real-time balance checking
- Portfolio analysis capabilities

**Migration from sBTC:**
- Originally built for Stacks sBTC
- Migrated to Scroll Sepolia for faster transactions and lower fees
- All smart contract interactions replaced with direct Web3.py calls
- Maintained same API structure for frontend compatibility

---

**Last Updated:** November 23, 2025  
**API Version:** 1.0  
**Blockchain Network:** Scroll Sepolia Testnet