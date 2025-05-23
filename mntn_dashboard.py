import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ------------------------------
# Initial Setup
st.set_page_config(page_title="MNTN Deal Dashboard", layout="wide")
st.title("📈 MNTN Deal IPO Dashboard")

# ------------------------------
# Constants
NOTE_INVESTMENT = 5_000_000
INTEREST_RATE = 0.06
YEARS_HELD = 3.25  # Feb 2022 to May 2025 approx
COVERAGE_PRICE = 22.97
SECONDARY_SHARES = 79542
SECONDARY_ENTRY_PRICE = 6.31

# ------------------------------
# IPO Price Slider
ipo_price = st.slider("📊 IPO Share Price ($)", min_value=10.0, max_value=30.0, value=16.0, step=0.25)

# ------------------------------
# Calculations
accrued_interest = NOTE_INVESTMENT * INTEREST_RATE * YEARS_HELD
note_total = NOTE_INVESTMENT + accrued_interest

# Conversion price is max of coverage price or IPO price, but sale price is always max of coverage price or IPO price
note_conversion_price = max(COVERAGE_PRICE, ipo_price)

# Number of shares converted
note_shares_converted = note_total / COVERAGE_PRICE

# Value when selling converted shares at conversion price
note_share_value = note_shares_converted * note_conversion_price

secondary_value = SECONDARY_SHARES * ipo_price
secondary_cost = SECONDARY_SHARES * SECONDARY_ENTRY_PRICE

# Returns and multiples
note_profit = note_share_value - NOTE_INVESTMENT
note_moic = note_share_value / NOTE_INVESTMENT
note_irr_approx = 0.061  # ~6.1% as given

secondary_profit = secondary_value - secondary_cost
secondary_moic = secondary_value / secondary_cost
secondary_holding_years = 2.25
secondary_irr_approx = ((secondary_moic) ** (1/secondary_holding_years)) - 1

# ------------------------------
# Layout - KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Note Investment", f"${NOTE_INVESTMENT:,.0f}")
col2.metric("Accrued Interest", f"${accrued_interest:,.0f}")
col3.metric("Note Payout Value", f"${note_share_value:,.0f}")

col4, col5, col6 = st.columns(3)
col4.metric("Secondary Shares", f"{SECONDARY_SHARES:,}")
col5.metric("Secondary Investment", f"${secondary_cost:,.0f}")
col6.metric("Secondary Value at IPO", f"${secondary_value:,.0f}")

# ------------------------------
# Waterfall Chart
fig = go.Figure(go.Waterfall(
    name = "Cash Flow",
    orientation = "v",
    measure = ["absolute", "relative", "relative"],
    x = ["Initial Investment", "Note Return", "Secondary Return"],
    textposition = "outside",
    text = [
        f"-${NOTE_INVESTMENT + secondary_cost:,.0f}",
        f"+${note_share_value:,.0f}",
        f"+${secondary_value:,.0f}"
    ],
    y = [-(NOTE_INVESTMENT + secondary_cost), note_share_value, secondary_value],
    connector = {"line":{"color":"rgb(63, 63, 63)"}}
))

fig.update_layout(
        title = "💰 MNTN Investment Cash Flow",
        waterfallgap = 0.3,
        showlegend = False
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Detailed Explanations (Expandable)
with st.expander("💸 Financial Modeling — Let’s Crunch Numbers"):
    st.markdown(f"""
**Convertible Note**

**Step 1: Calculate Accrued Interest**  
Simple interest =  
$5,000,000 × 6% × 3.25 years = **${accrued_interest:,.0f}**

**Step 2: Conversion or Sale Value**  
You sell converted shares at the greater of $22.97 or IPO price.

- IPO price chosen: **${ipo_price:.2f}**  
- Max conversion price: **${note_conversion_price:.2f}**  

Conversion value =  
$5,000,000 + ${accrued_interest:,.0f} = **${note_total:,.0f}**

Shares converted =  
${note_total:,.0f} ÷ $22.97 ≈ **{note_shares_converted:,.0f} shares**

At ${note_conversion_price:.2f} sale price, proceeds =  
{note_shares_converted:,.0f} × ${note_conversion_price:.2f} = **${note_share_value:,.0f}**

Return = **${note_profit:,.0f} profit**, or **{note_moic:.2f}x MOIC**  
Time-adjusted IRR ≈ **{note_irr_approx*100:.1f}% annually**

> ⚠️ This IRR is expected for a senior instrument with downside protection, not pure equity risk.

---

**Secondary Shareholding**

- Entry:  
79,542 shares × $6.31 = **${secondary_cost:,.0f}**

- Post-IPO Value (at ${ipo_price:.2f}):  
79,542 × ${ipo_price:.2f} = **${secondary_value:,.0f}**

- Unrealized gain = **${secondary_profit:,.0f}**  
- MOIC = **{secondary_moic:.2f}x**  
- Holding Period = ~2.25 years  
- IRR ≈ **{secondary_irr_approx*100:.1f}% annualized**

> This is the alpha-generating piece: you bought cheap, waited for liquidity, with no dilution or conversion mechanics.
""")

with st.expander("📊 Capital Allocation Strategy Review"):
    st.markdown("""
| Instrument         | Size        | Purpose                     | Risk Level | Return Potential |
|--------------------|-------------|-----------------------------|------------|------------------|
| Convertible Note   | $5M         | Structured downside protection | Low        | Low-to-mid       |
| Secondary Equity   | $502K       | High-upside illiquid bet      | Medium     | High             |

**Summary:**  
The combo gave us downside protection through the note (great in choppy markets) and asymmetric upside via the secondary share purchase.  
This is textbook secondaries strategy: structured + opportunistic equity.
""")

with st.expander("🔐 Post-IPO Lock-Up Considerations"):
    st.markdown("""
- Lock-up ends Q4 2025  
- 6 months of potential price volatility  
- **Risks:** Price drops post-IPO  
- **Mitigants:**  
  - Hedge with options (if available)  
  - Distribute shares in-kind to LPs and let them decide  
  - Structure staggered sales to minimize market impact  
""")

with st.expander("📜 Return of Capital to LPs"):
    st.markdown(f"""
**May 2025:**  
- $5M principal return  
- ~${accrued_interest:,.0f} accrued interest  
- LPs receive distributions and updated capital account statements  

**Q4 2025 (post lock-up):**  
- Potential distribution of:  
  - ~$1.19M from secondary shares  
  - ~$7.5M in new shares (issued via note conversion depending on IPO pricing)  

If shares hold in the ${ipo_price:.2f}–$23 range, we're looking at ~$9M–$10M in additional value realization in Q4 2025.
""")

# ------------------------------
# Footer
st.caption("Crafted with 💼 by BULLVC Apprentice")

