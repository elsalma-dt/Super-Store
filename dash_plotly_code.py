import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the data
data = pd.read_csv('C:/Users/KING/Downloads/archive/Sample - Superstore.csv', encoding='windows_1252')

# Create groupings for top-selling and most profitable products
top_selling_products = data.groupby('Product Name').sum()['Sales'].sort_values(ascending=False).head(5)
top_profit_products = data.groupby('Product Name').sum()['Profit'].sort_values(ascending=False).head(5)

# Create Plotly figures for top-selling and most profitable products
fig_top_selling = px.bar(top_selling_products, x=top_selling_products.index, y='Sales', title='Top 5 Best-Selling Products')
fig_top_profit = px.bar(top_profit_products, x=top_profit_products.index, y='Profit', title='Top 5 Most Profitable Products')

# Impact of discounts on sales
fig_discount_impact = px.scatter(data, x='Discount', y='Sales', trendline="ols", title="Impact of Discounts on Sales")
fig_discount_impact.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')

# Number of customers by segment
customer_segment = data.groupby('Segment').size().reset_index(name='Count')
fig_customer_segment = px.bar(customer_segment, x='Segment', y='Count', title='Number of Customers by Segment')
fig_customer_segment.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')

# Sales and profit by product category - clearer graph
category_group = data.groupby('Category')[['Sales', 'Profit']].sum().reset_index()
fig_category_sales_profit = px.bar(category_group, x='Category', y=['Sales', 'Profit'], barmode='group', 
                                   title='Sales and Profit by Category', text_auto=True)
fig_category_sales_profit.update_traces(marker_line_width=1.5, opacity=0.8)
fig_category_sales_profit.update_layout(plot_bgcolor='white', paper_bgcolor='white', font_color='black')

# Create Dash application
app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': 'black', 'color': 'white'}, children=[
    html.H1("Superstore Dashboard", style={'textAlign': 'center', 'color': 'white'}),
    
    # Section for best-selling products
    html.Div([
        html.H2("Best-Selling Products", style={'color': 'white'}),
        dcc.Graph(
            id='top-selling-products',
            figure=fig_top_selling
        ),
    ], style={'padding': '20px'}),
    
    # Section for most profitable products
    html.Div([
        html.H2("Most Profitable Products", style={'color': 'white'}),
        dcc.Graph(
            id='top-profit-products',
            figure=fig_top_profit
        ),
    ], style={'padding': '20px'}),
    
    # Impact of discounts on sales
    html.Div([
        html.H2("Impact of Discounts on Sales", style={'color': 'white'}),
        dcc.Graph(
            id='discount-impact',
            figure=fig_discount_impact
        ),
    ], style={'padding': '20px'}),
    
    # Number of customers by segment
    html.Div([
        html.H2("Number of Customers by Segment", style={'color': 'white'}),
        dcc.Graph(
            id='customer-segment',
            figure=fig_customer_segment
        ),
    ], style={'padding': '20px'}),

    # Sales and profit by category (improved clarity)
    html.Div([
        html.H2("Sales and Profit by Category", style={'color': 'white'}),
        dcc.Graph(
            id='category-sales-profit',
            figure=fig_category_sales_profit
        ),
    ], style={'padding': '20px'}),
    
    # Dropdown for selecting a specific product
    html.Div([
        html.Label("Choose a Product:", style={'color': 'white'}),
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': i, 'value': i} for i in data['Product Name'].unique()],
            value='Canon imageCLASS 2200 Advanced Copier',
            style={'color': 'black'}
        ),
        dcc.Graph(id='sales-profit-region')
    ], style={'padding': '20px'})
])

# Callback to update sales and profit graph by region based on the selected product
@app.callback(
    Output('sales-profit-region', 'figure'),
    [Input('product-dropdown', 'value')]
)
def update_graph(selected_product):
    product_data = data[data['Product Name'] == selected_product]
    region_group = product_data.groupby('Region')[['Sales', 'Profit']].mean()
    
    fig = px.bar(region_group, barmode='group', title=f'Sales and Profit for {selected_product} by Region')
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')
    return fig

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
