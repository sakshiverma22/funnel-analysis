# Ecommerce Plus

Ecommerce Plus is an e-commerce funnel analytics project that shows where shoppers drop out, compares customer segments, and trains an explainable purchase-propensity model in the browser.

## What it includes

- Multi-page dashboard: Overview, Funnel, Segments, ML Model, and Data Studio
- CSV upload and pasted CSV input
- Funnel conversion and drop-off calculations
- Device, traffic-source, and regional comparisons
- Opportunity sizing against the strongest peer segment
- Browser-trained regularized logistic regression
- Holdout accuracy, balanced accuracy, ROC-AUC, and baseline comparison
- Explainable model signals showing which features push purchase likelihood up or down

## Data status

The included dashboard demo data is synthetic portfolio data. It is not real company customer data. Upload a company's own event CSV to calculate metrics and train the model on that data.

## CSV format

Required columns:

```csv
user_id,event_type
```

Recommended columns:

```csv
user_id,event_type,device_type,traffic_source,region,order_value
```

Supported events:

```text
product_view
add_to_cart
checkout_start
purchase
```

`data-template.csv` and `ecommerce-plus-ml-sample.csv` are included for testing.

## ML model

The browser model is a supervised binary classifier using regularized logistic regression. Each user becomes one labeled row. Features include funnel progress, a cart-plus-checkout interaction, and one-hot encoded device, source, and region values. The model uses a deterministic 80/20 holdout split, trains on the training set, tunes its classification threshold on training data, and reports metrics on unseen users.

The model is intended for directional prioritization. Its results are not causal claims or guaranteed sales forecasts.

## Run locally

From the `dashboard` folder:

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

Open `http://localhost:8000/index.html`.

For a static deployment, upload the dashboard folder to Netlify, Vercel, GitHub Pages, or Cloudflare Pages.
