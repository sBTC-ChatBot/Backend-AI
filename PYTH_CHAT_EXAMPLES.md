# 🤖 Pyth Chat AI - Ejemplos de Uso

## Endpoint
```
POST http://localhost:5000/pyth/chat
Content-Type: application/json
```

## 📊 Ejemplos de Consultas

### 1. Consultar Precio Simple
```json
{
    "message": "What's the price of ETH?"
}
```

**Respuesta:**
```json
{
    "action": "get_price",
    "symbol": "eth",
    "message": "The current price of ETH is $2045.67 USD",
    "price_data": {
        "symbol": "ETH",
        "price": 2045.67,
        "price_usd": "$2045.67",
        "source": "Pyth Network (Hermes API)"
    }
}
```

### 2. Consultar Múltiples Precios
```json
{
    "message": "Show me BTC and ETH prices"
}
```

**Respuesta:**
```json
{
    "action": "get_multiple_prices",
    "symbols": ["btc", "eth"],
    "message": "Current prices - BTC: $37850.32, ETH: $2045.67",
    "prices": [
        {
            "symbol": "BTC",
            "price": 37850.32,
            "price_usd": "$37850.32"
        },
        {
            "symbol": "ETH",
            "price": 2045.67,
            "price_usd": "$2045.67"
        }
    ]
}
```

### 3. Pedir Consejo para Transferencia
```json
{
    "message": "Should I transfer 0.5 ETH now?"
}
```

**Respuesta:**
```json
{
    "action": "transfer_advice",
    "symbol": "eth",
    "amount": 0.5,
    "message": "Current ETH price: $2045.67 USD. Analysis complete.",
    "price_data": {
        "symbol": "ETH",
        "price": 2045.67,
        "price_usd": "$2045.67",
        "confidence": 0.85,
        "confidence_usd": "±$0.85",
        "source": "Pyth Network (Hermes API)"
    },
    "transfer_info": {
        "amount": 0.5,
        "estimated_value_usd": "$1022.84",
        "estimated_gas_fee": "$0.01 - $0.10 (Scroll Sepolia)",
        "network": "Scroll Sepolia Testnet"
    },
    "advice": "At the current ETH price of $2045.67, your 0.5 ETH transfer is worth approximately $1,022.84. The market shows stable conditions with a tight confidence interval of ±$0.85, which is favorable for transactions. Gas fees on Scroll Sepolia are minimal ($0.01-$0.10), making this a cost-effective time to transfer. Consider proceeding with your transaction if the current price aligns with your expectations."
}
```

### 4. Análisis de Mejor Momento para Transferir
```json
{
    "message": "Is it a good time to send 1 BTC?"
}
```

**Respuesta:**
```json
{
    "action": "transfer_advice",
    "symbol": "btc",
    "amount": 1,
    "message": "Current BTC price: $37850.32 USD. Analysis complete.",
    "price_data": {
        "symbol": "BTC",
        "price": 37850.32,
        "price_usd": "$37850.32",
        "confidence": 12.50,
        "confidence_usd": "±$12.50",
        "source": "Pyth Network (Hermes API)"
    },
    "transfer_info": {
        "amount": 1,
        "estimated_value_usd": "$37850.32",
        "estimated_gas_fee": "$0.01 - $0.10 (Scroll Sepolia)",
        "network": "Scroll Sepolia Testnet"
    },
    "advice": "Your 1 BTC transfer at the current price of $37,850.32 represents a significant value transaction. The confidence interval of ±$12.50 indicates relatively stable market conditions. Transaction fees on Scroll Sepolia are negligible compared to your transfer value. If you're satisfied with the current BTC price and don't anticipate immediate market volatility, this could be a suitable time to proceed with your transfer."
}
```

### 5. Comparar Precios para Decisión de Transferencia
```json
{
    "message": "Show me ETH, BTC and SOL prices for a transfer"
}
```

### 6. Consulta sobre Momento del Mercado
```json
{
    "message": "When should I transfer my ETH?"
}
```

### 7. Análisis sin Monto Específico
```json
{
    "message": "Give me advice about transferring SOL"
}
```

## 💡 Preguntas que Puedes Hacer

### Consultas de Precios
- "What's the current price of ETH?"
- "How much is Bitcoin?"
- "Show me USDC price"
- "Get me prices for ETH, BTC and SOL"

### Consejos de Transferencia
- "Should I transfer 0.5 ETH now?"
- "Is it a good time to send 2 BTC?"
- "I want to transfer 100 USDC, what do you recommend?"
- "Give me advice about transferring my SOL"

### Análisis de Mercado
- "What's the best time to transfer ETH today?"
- "Should I wait before transferring my BTC?"
- "Is the ETH price stable for a transfer?"
- "How are gas fees on Scroll Sepolia?"

## 🎯 Características del Chat AI

✅ **Precios en Tiempo Real** - Usa Pyth Network Hermes API  
✅ **Consejos Personalizados** - Basados en el monto y criptomoneda  
✅ **Análisis de Volatilidad** - Considera el intervalo de confianza  
✅ **Información de Gas Fees** - Específico para Scroll Sepolia  
✅ **Valor Estimado en USD** - Calcula el valor de tu transferencia  
✅ **Conversación Natural** - Entiende preguntas en lenguaje natural  

## 📝 Criptomonedas Soportadas

ETH, BTC, USDC, USDT, BNB, SOL, MATIC, AVAX, ADA, DOGE

## ⚠️ Notas Importantes

- Todos los precios son en USD
- La red usada es **Scroll Sepolia Testnet**
- Los gas fees son estimaciones (~$0.01-$0.10)
- Los consejos son generados por IA y no constituyen asesoría financiera
- Siempre verifica los precios antes de realizar transferencias importantes
