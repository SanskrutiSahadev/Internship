import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.markdown("""
    <style>
    /* This targets the main content area */
    .block-container {
        padding-top: 1rem;    /* Reduced from default ~6rem */
        padding-bottom: 0rem;
        padding-left: 4rem;
        padding-right: 4rem;
    }
    .stApp { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00d1ff; }
    /* Force the dataframe container to have a white feel */
    .stDataFrame { background-color: white; border-radius: 5px; padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv('sales_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# --- HEADER ---
st.title("SALES ANALYSIS REPORT")
st.write(f"Last updated: {df['Date'].max().strftime('%Y-%m-%d')}")

# --- TOP ROW: KPI METRICS ---
col_name = 'Total_Sales' if 'Total_Sales' in df.columns else 'Total_Sales'

total_rev = df[col_name].sum()
total_qty = df['Quantity'].sum()
avg_order = df[col_name].mean()

col1, col2, col3 = st.columns(3)
col1.metric("TOTAL REVENUE", f"${total_rev:,.2f}", "+12%")
col2.metric("UNITS SOLD", f"{total_qty:,}", "Stable")
col3.metric("AVG ORDER VALUE", f"${avg_order:,.2f}", "-5%")

# st.divider()

# --- MIDDLE ROW: TRENDS & PRODUCT PERFORMANCE ---
left_col, right_col = st.columns([1.3, 1])

with left_col:
    st.markdown("<h4 style='text-align: center;'>Monthly Sales Trend</h4>", unsafe_allow_html=True)
    
    df_trend = df.resample('M', on='Date')[col_name].sum().reset_index()
    
    fig_trend = px.line(df_trend, x='Date', y=col_name, template="plotly_dark", markers=True)
    
    fig_trend.update_traces(
        line_color='#00d1ff', 
        line_width=3, 
        marker=dict(size=12, color='white', line=dict(width=2, color='#00d1ff')),
        text=df_trend[col_name].apply(lambda x: f'{x/1000000:.2f}M'),
        mode='lines+markers+text',
        textposition='top center', # Pushes label above the dot
        textfont=dict(size=14, color='white')
    )
    
    fig_trend.update_layout(
        margin=dict(t=50, b=0, l=0, r=0),
        yaxis=dict(showgrid=True, gridcolor='#333'),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with right_col:
    st.markdown("<h4 style='text-align: center;'>Sales by Product</h4>", unsafe_allow_html=True)
    
    product_sales = df.groupby('Product')[col_name].sum().reset_index()
    # product_sales = product_sales.sort_values(by=col_name, ascending=True)
    # Custom high-contrast blues
    fig_prod = px.bar(product_sales, x=col_name, y='Product', 
                      orientation='h', 
                      template="plotly_dark",
                      color='Product',
                      color_discrete_sequence=['#87CEEB', '#5F9EA0', '#4682B4', '#1E90FF', '#00BFFF'])
    
    fig_prod.update_traces(
        text=(product_sales[col_name] / 1000000).apply(lambda x: f'{x:.3f}M'), 
        textposition='outside', 
        textfont=dict(size=14, color='white'),
        cliponaxis=False # Prevents labels from being cut off at the edge
    )
    
    fig_prod.update_layout(
        showlegend=False, 
        margin=dict(t=30, b=0, l=0, r=50), 
        xaxis=dict(title="Total Revenue", showgrid=True, gridcolor='#333'),
        yaxis=dict(title="")
    )
    st.plotly_chart(fig_prod, use_container_width=True)
# --- BOTTOM ROW: REGION & RAW DATA ---
bot_left, bot_right = st.columns([1, 2])

with bot_left:
    st.markdown("<h3 style='text-align: center;'>Regional Distribution</h3>", unsafe_allow_html=True)
    region_colors = ['#2EC4E6', '#D97742', '#5BC98C', '#1F6F8B']
    
    fig_pie = px.pie(df, values=col_name, names='Region', hole=0.5, 
                     template="plotly_dark",
                     color_discrete_sequence=region_colors)
    
    fig_pie.update_layout(
        legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="center", x=0.5)
    )
    fig_pie.update_traces(
        texttemplate="<b>%{label}</b><br><b>%{percent:.1%}</b>",
        textposition='inside',
        textfont=dict(size=16, color='black'), # Changed to white for better contrast on dark slices
        marker=dict(line=dict(color='#0e1117', width=2))
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with bot_right:
    st.subheader("Detailed Order Log")
    # Displaying the dataframe with a white background style
    st.dataframe(
        df.head(10).style.set_properties(**{
            'background-color': 'lightgray',
            'color': 'black',
            'border-color': '#d3d3d3'
        }), 
        use_container_width=True
    )