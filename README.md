# 🚀 Backend-AI - Crypto Wallet API with AI Intelligence

A Flask-based REST API for cryptocurrency wallet management on **Scroll Sepolia Testnet**, featuring AI-powered chat assistance, real-time price feeds from Pyth Network, and blockchain transaction capabilities with Web3.py.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Web3.py](https://img.shields.io/badge/Web3.py-6.0+-orange.svg)](https://web3py.readthedocs.io/)
[![Scroll](https://img.shields.io/badge/Scroll-Sepolia-purple.svg)](https://scroll.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Endpoints](#-api-endpoints)
  - [User Management](#1-user-management-4-endpoints)
  - [Contact Management](#2-contact-management-3-endpoints)
  - [Contact Wallets](#3-contact-wallets-2-endpoints)
  - [Transactions](#4-transactions-2-endpoints)
  - [Balance](#5-balance-1-endpoint)
  - [Pyth Network Pricing](#6-pyth-network-pricing-2-endpoints)
  - [AI Chat Assistant](#7-ai-chat-assistant-1-endpoint)
- [Usage Examples](#-usage-examples)
- [Supported Cryptocurrencies](#-supported-cryptocurrencies)
- [Technologies](#-technologies)
- [Error Handling](#-error-handling)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Functionality
- 🔗 **Scroll Sepolia Integration**: Native Web3.py integration with Scroll L2 testnet
- 💸 **ETH Transfers**: Complete transaction system with automatic gas estimation
- 👥 **User Management**: Full CRUD operations for users, contacts, and wallets
- 📊 **Real-time Balance**: Query wallet balances directly from blockchain
- 📝 **Transaction History**: Track and monitor all transactions

### AI-Powered Intelligence
- 🤖 **DeepSeek AI Chat**: Natural language processing for crypto operations
- 💡 **Transfer Advice**: AI-powered recommendations based on market conditions
- 📈 **Portfolio Analysis**: Automated portfolio valuation and diversification insights
- 🎯 **4 AI Actions**: Price queries, multi-price comparisons, transfer advice, portfolio calculation

### Market Data (Pyth Network)
- 📡 **Real-time Oracle Prices**: Direct integration with Pyth Network Hermes API
- 💰 **10 Cryptocurrencies**: ETH, BTC, USDC, USDT, BNB, SOL, MATIC, AVAX, ADA, DOGE
- 📊 **Detailed Metrics**: Price, confidence intervals, volatility classification, timestamps
- 🔍 **Price Feed IDs**: Full Pyth Network oracle metadata included

### Database & Security
- 🗄️ **Supabase PostgreSQL**: Scalable cloud database for users and transactions
- 🔒 **Encrypted Keys**: Client-side encryption for private key storage
- 🌐 **CORS Enabled**: Ready for cross-origin requests from web frontends
- ✅ **Input Validation**: Protection against malformed requests and SQL injection

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (React/Vue)   │
└────────┬────────┘
         │ HTTP REST
         ▼
┌─────────────────────────────────────────┐
│         Flask Backend (app.py)          │
│  ┌──────────┬──────────┬─────────────┐ │
│  │ User API │ Pyth API │ AI Chat API │ │
│  └──────────┴──────────┴─────────────┘ │
└───┬──────────┬──────────┬──────────────┘
    │          │          │
    ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│ Supabase │ │ Web3.py  │ │ DeepSeek AI  │
│PostgreSQL│ │ Scroll   │ │ (Chat Model) │
└──────────┘ │ Sepolia  │ └──────────────┘
             └──────────┘
                  │
                  ▼
             ┌──────────┐
             │  Pyth    │
             │ Network  │
             │ Hermes   │
             └──────────┘
```

**Network Details:**
- **Blockchain:** Scroll Sepolia Testnet (Chain ID: 534351)
- **RPC:** `https://sepolia-rpc.scroll.io`
- **Explorer:** `https://sepolia.scrollscan.com`
- **Oracle:** Pyth Network Hermes API (`https://hermes.pyth.network`)

## 🔧 Prerequisites

Before starting, ensure you have:

- **Python 3.8+** installed
- **pip** (Python package manager)
- **Scroll Sepolia testnet ETH** (get from faucet)
- **DeepSeek API Key** - [Get it here](https://platform.deepseek.com/)
- **Supabase Account** - [Sign up here](https://supabase.com/)
- **Git** for version control

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/HappyHODLers/Backend.git
cd Backend-AI
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

1. **Create a `.env` file in the project root** with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# DeepSeek AI Configuration
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Scroll Network Configuration (Optional - defaults provided)
SCROLL_SEPOLIA_RPC=https://sepolia-rpc.scroll.io
CHAIN_ID=534351
```

2. **Supabase Database Setup**

Create the following tables in your Supabase project:

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    wallet VARCHAR(42) UNIQUE NOT NULL,
    nombre_usuario VARCHAR(255),
    clave_privada_encriptada TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Contacts table
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    user_wallet VARCHAR(42) REFERENCES users(wallet) ON DELETE CASCADE,
    contact_wallet VARCHAR(42) NOT NULL,
    nombre_contacto VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Contact wallets table
CREATE TABLE contact_wallets (
    id SERIAL PRIMARY KEY,
    nombre_wallet_agregada VARCHAR(255),
    wallet_agregada VARCHAR(42) NOT NULL,
    wallet_quien_agrego VARCHAR(42) REFERENCES users(wallet) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Transactions table
CREATE TABLE transacciones (
    id SERIAL PRIMARY KEY,
    wallet_origen VARCHAR(42) NOT NULL,
    wallet_destino VARCHAR(42) NOT NULL,
    monto DECIMAL(20, 8) NOT NULL,
    hash VARCHAR(66) UNIQUE,
    estado VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
```

3. **Start the server**

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

---

## 📡 API Endpoints

### Base URL
```
http://127.0.0.1:5000
```

---

## 1️⃣ User Management (4 Endpoints)

### 1.1 Create User
**Create a new user account with encrypted wallet credentials.**

- **Method:** `POST`
- **Endpoint:** `/users`
- **Request Body:**
```json
{
  "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "nombre_usuario": "John Doe",
  "clave_privada_encriptada": "encrypted_private_key_string"
}
```
- **Response (201 Created):**
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
- **Use Case:** Initial wallet registration, user onboarding
- **Technical Details:** Stores encrypted private key (never plaintext), validates Ethereum address format

---

### 1.2 Get User by Wallet
**Retrieve user information by wallet address.**

- **Method:** `GET`
- **Endpoint:** `/users/wallet/<wallet_address>`
- **Example:**
```bash
curl http://127.0.0.1:5000/users/wallet/0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```
- **Response (200 OK):**
```json
{
  "id": 123,
  "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "nombre_usuario": "John Doe",
  "clave_privada_encriptada": "encrypted_key",
  "created_at": "2025-11-23T10:30:00Z"
}
```
- **Use Case:** User login, profile loading, authentication
- **Technical Details:** Case-insensitive wallet lookup, returns 404 if not found

---

### 1.3 Update User
**Update user information (username or encrypted key).**

- **Method:** `PUT`
- **Endpoint:** `/users/<wallet_address>`
- **Request Body (partial updates allowed):**
```json
{
  "nombre_usuario": "John Smith"
}
```
- **Response (200 OK):**
```json
{
  "message": "Usuario actualizado exitosamente",
  "user": {
    "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "nombre_usuario": "John Smith"
  }
}
```
- **Use Case:** Profile updates, key rotation
- **Technical Details:** Supports partial updates, validates fields before updating

---

### 1.4 Delete User
**Permanently delete user account and all associated data.**

- **Method:** `DELETE`
- **Endpoint:** `/users/<wallet_address>`
- **Response (200 OK):**
```json
{
  "message": "Usuario eliminado exitosamente"
}
```
- **Use Case:** Account deletion, GDPR compliance
- **Technical Details:** Cascades to delete contacts and transaction history

---

## 2️⃣ Contact Management (3 Endpoints)

### 2.1 Add Contact
**Add a new contact to user's address book.**

- **Method:** `POST`
- **Endpoint:** `/users/wallet/<wallet_address>/contacts`
- **Request Body:**
```json
{
  "contact_wallet": "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
  "nombre_contacto": "Alice Smith"
}
```
- **Response (201 Created):**
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
- **Use Case:** Building contact list for quick transfers
- **Technical Details:** Prevents duplicate contacts, validates Ethereum addresses

---

### 2.2 Get User Contacts
**Retrieve all contacts for a specific user.**

- **Method:** `GET`
- **Endpoint:** `/users/wallet/<wallet_address>/contacts`
- **Response (200 OK):**
```json
{
  "contacts": [
    {
      "id": 456,
      "contact_wallet": "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
      "nombre_contacto": "Alice Smith",
      "created_at": "2025-11-20T15:00:00Z"
    }
  ]
}
```
- **Use Case:** Populating recipient dropdowns, displaying address book
- **Technical Details:** Returns empty array if no contacts found

---

### 2.3 Delete Contact
**Remove a contact from user's address book.**

- **Method:** `DELETE`
- **Endpoint:** `/users/wallet/<wallet_address>/contacts/<contact_id>`
- **Response (200 OK):**
```json
{
  "message": "Contacto eliminado exitosamente"
}
```
- **Use Case:** Contact list management
- **Technical Details:** Validates ownership before deletion

---

## 3️⃣ Contact Wallets (2 Endpoints)

### 3.1 Add Contact Wallet
**Create a labeled wallet entry (separate from main contacts).**

- **Method:** `POST`
- **Endpoint:** `/contact-wallets`
- **Request Body:**
```json
{
  "nombre_wallet_agregada": "My Savings Wallet",
  "wallet_agregada": "0xabcdef1234567890abcdef1234567890abcdef12",
  "wallet_quien_agrego": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
}
```
- **Response (201 Created):**
```json
{
  "message": "Contact wallet agregado exitosamente",
  "contact_wallet": {
    "id": 789,
    "nombre_wallet_agregada": "My Savings Wallet",
    "wallet_agregada": "0xabcdef1234567890abcdef1234567890abcdef12"
  }
}
```
- **Use Case:** Multi-wallet management, organizing personal wallets
- **Technical Details:** Independent from contacts table, allows self-referencing

---

### 3.2 Get Contact Wallets
**Retrieve all labeled wallets created by a user.**

- **Method:** `GET`
- **Endpoint:** `/contact-wallets/<wallet_address>`
- **Response (200 OK):**
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
- **Use Case:** Displaying user's labeled wallet collection
- **Technical Details:** Sorted by creation date

---

## 4️⃣ Transactions (2 Endpoints)

### 4.1 Create Transaction
**Execute an ETH transfer on Scroll Sepolia network.**

- **Method:** `POST`
- **Endpoint:** `/transactions`
- **Request Body:**
```json
{
  "wallet_origen": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "wallet_destino": "0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199",
  "monto": "0.1",
  "clave_privada": "0xprivate_key_here"
}
```
- **Response (201 Created):**
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
- **Use Case:** Sending ETH between wallets
- **Technical Details:** 
  - Uses Web3.py for transaction signing
  - Automatic gas price estimation
  - Returns transaction hash for tracking
  - Verifiable on Scroll Sepolia explorer

---

### 4.2 Get Transaction History
**Retrieve all transactions for a wallet (sent and received).**

- **Method:** `GET`
- **Endpoint:** `/transactions/wallet/<wallet_address>`
- **Response (200 OK):**
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
- **Use Case:** Transaction history view, accounting
- **Technical Details:** Includes both incoming and outgoing transactions

---

## 5️⃣ Balance (1 Endpoint)

### 5.1 Get Wallet Balance
**Query current ETH balance from Scroll Sepolia blockchain.**

- **Method:** `GET`
- **Endpoint:** `/balance/<wallet_address>`
- **Example:**
```bash
curl http://127.0.0.1:5000/balance/0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```
- **Response (200 OK):**
```json
{
  "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "balance": "1.5",
  "balance_wei": "1500000000000000000",
  "network": "Scroll Sepolia",
  "chain_id": 534351
}
```
- **Use Case:** Displaying wallet balance, pre-transaction validation
- **Technical Details:** 
  - Direct RPC query via Web3.py
  - Returns both human-readable (ETH) and Wei formats
  - Real-time data, not cached

---

## 6️⃣ Pyth Network Pricing (2 Endpoints)

### 6.1 Get Single Cryptocurrency Price
**Fetch real-time price data from Pyth Network Hermes API.**

- **Method:** `GET`
- **Endpoint:** `/pyth/price/<symbol>`
- **Supported Symbols:** `eth`, `btc`, `usdc`, `usdt`, `bnb`, `sol`, `matic`, `avax`, `ada`, `doge`
- **Example:**
```bash
curl http://127.0.0.1:5000/pyth/price/eth
```
- **Response (200 OK):**
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
- **Use Case:** Real-time price displays, market dashboards
- **Technical Details:**
  - **Volatility Classification:**
    - Very Low: < 0.01%
    - Low: 0.01% - 0.1%
    - Moderate: 0.1% - 0.5%
    - High: 0.5% - 1%
    - Very High: > 1%
  - Direct integration with Pyth Hermes API
  - No rate limits for reasonable usage
  - Confidence intervals indicate price reliability

---

### 6.2 Get Multiple Cryptocurrency Prices
**Fetch prices for multiple assets in a single request.**

- **Method:** `GET`
- **Endpoint:** `/pyth/prices`
- **Query Parameters:** `?symbols=eth,btc,sol` (optional, returns all 10 if omitted)
- **Example:**
```bash
curl "http://127.0.0.1:5000/pyth/prices?symbols=eth,btc,sol"
```
- **Response (200 OK):**
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
- **Use Case:** Portfolio overviews, multi-asset dashboards
- **Technical Details:** Batch fetching for efficiency, filtered results if symbols specified

---

## 7️⃣ AI Chat Assistant (1 Endpoint - 4 Actions)

### 7.1 AI-Powered Chat
**Natural language interface for crypto operations powered by DeepSeek AI.**

- **Method:** `POST`
- **Endpoint:** `/pyth/chat`
- **Base Request:**
```json
{
  "message": "Your natural language query here",
  "portfolio": [
    {
      "symbol": "ETH",
      "amount": 1.5
    }
  ]
}
```

---

#### Action 1: Get Single Price
**AI detects price query for specific cryptocurrency.**

**Example Queries:**
- "What's the price of Ethereum?"
- "How much is BTC?"
- "Current SOL price?"

**Request:**
```json
{
  "message": "What's the current price of Ethereum?"
}
```

**Response:**
```json
{
  "response": "The current price of Ethereum (ETH) is $2,045.67 USD with a confidence interval of ±$0.15 (0.007%). The volatility is classified as Very Low, indicating stable pricing. This data was published at 2025-11-23 12:05:54 UTC.",
  "action": "get_price",
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

#### Action 2: Get Multiple Prices
**AI detects comparison or multiple asset queries.**

**Example Queries:**
- "Compare ETH and BTC prices"
- "Show me prices for top 3 cryptos"
- "What are SOL and MATIC worth?"

**Request:**
```json
{
  "message": "Compare Ethereum, Bitcoin, and Solana prices"
}
```

**Response:**
```json
{
  "response": "Here are the current prices:\n\n• Ethereum (ETH): $2,045.67 (±$0.15, Very Low volatility)\n• Bitcoin (BTC): $37,234.89 (±$2.50, Low volatility)\n• Solana (SOL): $58.23 (±$0.08, Low volatility)",
  "action": "get_multiple_prices",
  "data": {
    "prices": [
      {
        "symbol": "ETH",
        "price": 2045.67,
        "volatility": "Very Low"
      },
      {
        "symbol": "BTC",
        "price": 37234.89,
        "volatility": "Low"
      }
    ]
  }
}
```

---

#### Action 3: Transfer Advice
**AI provides market-based recommendations for transfers.**

**Example Queries:**
- "Should I transfer ETH now?"
- "Is it a good time to send Bitcoin?"
- "Advise me on transferring 0.5 ETH"

**Request:**
```json
{
  "message": "Should I transfer 0.5 ETH right now?"
}
```

**Response:**
```json
{
  "response": "📊 Ethereum (ETH): $2,045.67\n🎯 Volatility: Very Low (0.007%)\n⏰ Updated: 2025-11-23 12:05:54 UTC\n\n✅ RECOMMENDATION: This is a GOOD time to transfer ETH.\n\nThe volatility is very low, indicating stable pricing with minimal risk of price fluctuation during transaction confirmation. The tight confidence interval (±$0.15) means reliable pricing.\n\n💡 Additional Tips:\n- Gas fees on Scroll Sepolia are typically low\n- Transaction confirmations take ~3-5 seconds\n- Monitor for 5-10 minutes to ensure continued stability\n\n⚠️ Always verify recipient address before sending.",
  "action": "transfer_advice",
  "data": {
    "symbol": "ETH",
    "price": 2045.67,
    "volatility": "Very Low",
    "confidence_percentage": "0.007%"
  }
}
```

---

#### Action 4: Portfolio Calculator
**AI calculates total value and provides investment analysis.**

**Example Queries:**
- "What's my portfolio worth?"
- "Calculate my holdings"
- "Analyze my portfolio"

**Request:**
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
  "response": "📊 PORTFOLIO ANALYSIS\n\nTotal Value: $6,011.48 USD\n\n💎 Asset Breakdown:\n1. Ethereum (ETH): 1.5 × $2,045.67 = $3,068.51 (51.04%)\n2. Bitcoin (BTC): 0.05 × $37,234.89 = $1,861.74 (30.97%)\n3. Solana (SOL): 10 × $58.23 = $582.30 (9.69%)\n\n📈 AI Investment Advice:\n\n✅ Strengths:\n- Well-diversified across major networks\n- Balanced risk with large-cap dominance (82% in ETH+BTC)\n- Good growth potential with SOL allocation\n\n💡 Recommendations:\n- Current volatility is Very Low to Low (optimal for rebalancing)\n- Consider taking profits on ETH (>50% concentration)\n- SOL provides Layer 1 diversification\n\n⚠️ Risk: LOW to MODERATE\nAll assets show tight confidence intervals indicating stable pricing.",
  "action": "calculate_portfolio",
  "data": {
    "portfolio_items": [
      {
        "symbol": "ETH",
        "amount": 1.5,
        "price": 2045.67,
        "value_usd": 3068.51,
        "percentage": 51.04
      }
    ],
    "total_value_usd": 6011.48
  }
}
```

**Portfolio Analysis Includes:**
- Total USD value across all holdings
- Individual asset valuations
- Percentage allocation per asset
- Diversification score
- AI-generated investment recommendations
- Risk assessment based on volatility
- Rebalancing suggestions

---

## 💱 Supported Cryptocurrencies

| Symbol | Name | Pyth Feed ID |
|--------|------|--------------|
| **ETH** | Ethereum | `0xff61491a931112ddf1bd8147cd1b641375f79f5825126d665480874634fd0ace` |
| **BTC** | Bitcoin | `0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43` |
| **USDC** | USD Coin | `0xeaa020c61cc479712813461ce153894a96a6c00b21ed0cfc2798d1f9a9e9c94a` |
| **USDT** | Tether | `0x2b89b9dc8fdf9f34709a5b106b472f0f39bb6ca9ce04b0fd7f2e971688e2e53b` |
| **BNB** | Binance Coin | `0x2f95862b045670cd22bee3114c39763a4a08beeb663b145d283c31d7d1101c4f` |
| **SOL** | Solana | `0xef0d8b6fda2ceba41da15d4095d1da392a0d2f8ed0c6c7bc0f4cfac8c280b56d` |
| **MATIC** | Polygon | `0x5de33a9112c2b700b8d30b8a3402c103578ccfa2765696471cc672bd5cf6ac52` |
| **AVAX** | Avalanche | `0x93da3352f9f1d105fdfe4971cfa80e9dd777bfc5d0f683ebb6e1294b92137bb7` |
| **ADA** | Cardano | `0x2a01deaec9e51a579277b34b122399984d0bbf57e2458a7e42fecd2829867a0d` |
| **DOGE** | Dogecoin | `0xdcef50dd0a4cd2dcc17e45df1676dcb336a11a61c69df7a0299b0150c672d25c` |

---

## 🛠️ Technologies

### Backend Framework
- **Flask 3.0.0** - Lightweight Python web framework
- **Flask-CORS** - Cross-origin resource sharing support

### Blockchain Integration
- **Web3.py 6.x** - Ethereum/Scroll blockchain interaction
- **Scroll Sepolia Testnet** - Layer 2 scaling solution
- **Pyth Network** - Decentralized oracle for price feeds

### Database
- **Supabase** - PostgreSQL cloud database
- **supabase-py** - Python client library

### AI Integration
- **DeepSeek AI** - Natural language processing
- **Model:** `deepseek-chat` with function calling

### Additional Libraries
- **requests** - HTTP client for API calls
- **python-dotenv** - Environment variable management
- **datetime** - Timestamp handling

---

## ❌ Error Handling

### HTTP Status Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| **200** | OK | Successful GET/PUT/DELETE request |
| **201** | Created | Successful POST request |
| **400** | Bad Request | Missing fields, invalid data format |
| **404** | Not Found | User/contact/transaction doesn't exist |
| **500** | Internal Server Error | Database/API/blockchain errors |

### Error Response Format
```json
{
  "error": "Error message describing the issue",
  "details": "Additional technical information (optional)"
}
```

### Example Errors

**Invalid Symbol:**
```json
{
  "error": "Símbolo no soportado. Símbolos válidos: eth, btc, usdc, usdt, bnb, sol, matic, avax, ada, doge"
}
```

**User Not Found:**
```json
{
  "error": "Usuario no encontrado"
}
```

**Pyth Network Error:**
```json
{
  "error": "Error al obtener precio de Pyth Network",
  "details": "Connection timeout"
}
```

**Insufficient Balance:**
```json
{
  "error": "Saldo insuficiente para realizar la transacción"
}
```

---

## 📚 Usage Examples

### Complete Workflow Example

#### Step 1: Create User
```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "wallet": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "nombre_usuario": "Alice",
    "clave_privada_encriptada": "encrypted_key_123"
  }'
```

#### Step 2: Check Balance
```bash
curl http://127.0.0.1:5000/balance/0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

#### Step 3: Get Real-time ETH Price
```bash
curl http://127.0.0.1:5000/pyth/price/eth
```

#### Step 4: Ask AI for Transfer Advice
```bash
curl -X POST http://127.0.0.1:5000/pyth/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Should I transfer 0.5 ETH now?"
  }'
```

#### Step 5: Execute Transfer
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

#### Step 6: Calculate Portfolio Value
```bash
curl -X POST http://127.0.0.1:5000/pyth/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Calculate my portfolio value",
    "portfolio": [
      {"symbol": "ETH", "amount": 1.5},
      {"symbol": "BTC", "amount": 0.05},
      {"symbol": "SOL", "amount": 10}
    ]
  }'
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Add unit tests for new features
- Update documentation for API changes
- Test on Scroll Sepolia before submitting

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support & Resources

### Documentation
- 📖 [Full API Documentation](API_DOCUMENTATION.md)
- 🚀 [Quick Start Guide](#installation)
- 💡 [Usage Examples](#-usage-examples)

### External Resources
- 🔗 [Scroll Documentation](https://docs.scroll.io)
- 🔗 [Scroll Sepolia Faucet](https://scroll.io/bridge) - Get test ETH
- 🔗 [Pyth Network Docs](https://docs.pyth.network)
- 🔗 [DeepSeek API](https://platform.deepseek.com/)
- 🔗 [Supabase Documentation](https://supabase.com/docs)
- 🔗 [Web3.py Documentation](https://web3py.readthedocs.io/)

### Blockchain Explorers
- 🔍 [Scroll Sepolia Explorer](https://sepolia.scrollscan.com)
- 📊 [Pyth Price Feeds](https://pyth.network/price-feeds)

---

## 🎯 Roadmap

### Current Features (v1.0)
- ✅ User & contact management
- ✅ ETH transfers on Scroll Sepolia
- ✅ Real-time price feeds (10 cryptocurrencies)
- ✅ AI chat with 4 action types
- ✅ Portfolio calculator

### Planned Features (v2.0)
- 🔜 Multi-currency conversion calculator
- 🔜 Volatility analysis dashboard
- 🔜 Price alert system with Supabase
- 🔜 Risk analysis for transfers
- 🔜 Gas fee comparator
- 🔜 Transaction history export (CSV/JSON)
- 🔜 Mainnet deployment support

---

## 👥 Team

**HappyHODLers**
- 🏗️ Built for hackathons and crypto enthusiasts
- 🌐 Repository: [github.com/HappyHODLers/Backend](https://github.com/HappyHODLers/Backend)

---

## 🙏 Acknowledgments

- **Scroll** for providing a fast and efficient Layer 2 solution
- **Pyth Network** for reliable decentralized oracle data
- **DeepSeek** for powerful AI natural language processing
- **Supabase** for seamless PostgreSQL cloud database
- **Web3.py** for robust Ethereum integration

---

## 📊 Project Stats

- **Total Endpoints:** 15
- **Supported Cryptocurrencies:** 10
- **AI Actions:** 4
- **Database Tables:** 4
- **Blockchain Network:** Scroll Sepolia (Chain ID: 534351)
- **Language:** Python 3.8+
- **Framework:** Flask 3.0.0

---

## 🔐 Security Notice

⚠️ **Important Security Reminders:**

1. **Never commit `.env` files** to version control
2. **Encrypt private keys** client-side before sending to API
3. **Use HTTPS** in production environments
4. **Rotate API keys** regularly
5. **Validate all inputs** before processing
6. **Test on testnet** before mainnet deployment
7. **Store encrypted keys** securely in production
8. **Monitor API usage** for suspicious activity

---

## 📈 Performance & Rate Limits

| Service | Rate Limit | Notes |
|---------|-----------|-------|
| **Scroll Sepolia RPC** | No strict limit | Public RPC may throttle heavy usage |
| **Pyth Hermes API** | ~100 req/min recommended | No strict enforcement |
| **DeepSeek AI** | Depends on API tier | Check your plan limits |
| **Supabase** | Free tier: 50MB database | Upgrade for production |

---

**Last Updated:** November 23, 2025  
**Version:** 1.0  
**Status:** Active Development  
**Network:** Scroll Sepolia Testnet

---

Made with ❤️ by HappyHODLers 🚀

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si deseas contribuir:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## 👤 Autor

**JHAMILCALI**

- GitHub: [@JHAMILCALI](https://github.com/JHAMILCALI)
- Repositorio: [clarity-backend](https://github.com/JHAMILCALI/clarity-backend)

---

## 🌟 Agradecimientos

- [Stacks](https://www.stacks.co/) - Blockchain para contratos inteligentes
- [DeepSeek](https://www.deepseek.com/) - IA para procesamiento de lenguaje natural
- [Flask](https://flask.palletsprojects.com/) - Framework web para Python
- [Supabase](https://supabase.com/) - Base de datos PostgreSQL en la nube

---

## 📚 Documentación Adicional

- **[SUPABASE_API.md](SUPABASE_API.md)** - Documentación completa de endpoints de Supabase
- **[AI_DATABASE_EXAMPLES.md](AI_DATABASE_EXAMPLES.md)** - Ejemplos de cómo la IA interactúa con la base de datos
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía de despliegue
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Guía de integración con frontend

---

## 🧠 Nueva Funcionalidad: IA + Base de Datos

La IA de DeepSeek ahora puede interactuar directamente con tu base de datos de Supabase usando lenguaje natural:

```bash
# Listar usuarios
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Muéstrame todos los usuarios"}'

# Crear un usuario
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Registra un usuario llamado Juan con wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"}'

# Buscar usuario
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Busca el usuario con wallet ST2PQHQ0EYR93KSP0B6AN9AHEJ1K3EBRJP02HPGK6"}'
```

**Ver más ejemplos en [AI_DATABASE_EXAMPLES.md](AI_DATABASE_EXAMPLES.md)**

---

## 📞 Soporte

Si tienes problemas o preguntas, por favor:

1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Abre un [Issue](https://github.com/JHAMILCALI/clarity-backend/issues) en GitHub
3. Consulta la [documentación de Stacks](https://docs.stacks.co/)

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

Hecho con ❤️ por JHAMILCALI

</div>
