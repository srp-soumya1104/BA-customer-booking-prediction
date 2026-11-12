-- 1. Lowest in-stock discounted offer per product (SQLite / MySQL 8+)
WITH ranked_offers AS (
    SELECT product_id, product_name, platform,
        ROUND(listed_price * (1.0 - discount_pct / 100.0), 2) AS discounted_price,
        ROW_NUMBER() OVER (PARTITION BY product_id
            ORDER BY listed_price * (1.0 - discount_pct / 100.0), platform) AS offer_rank
    FROM offers WHERE in_stock = 1
)
SELECT product_id, product_name, platform, discounted_price
FROM ranked_offers WHERE offer_rank = 1 ORDER BY product_id;

-- 2. Platform offer availability and discount overview
SELECT platform, COUNT(*) AS listed_offers,
    SUM(CASE WHEN in_stock = 1 THEN 1 ELSE 0 END) AS available_offers,
    ROUND(AVG(discount_pct), 2) AS avg_discount_pct,
    ROUND(100.0 * SUM(CASE WHEN in_stock = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS stock_rate_pct
FROM offers GROUP BY platform ORDER BY platform;

-- 3. Coupon rules: test eligibility using the final order subtotal, not unit price.
SELECT platform, coupon_code, coupon_pct, coupon_min_spend, coupon_max_discount,
    COUNT(*) AS product_count
FROM offers WHERE coupon_code IS NOT NULL AND TRIM(coupon_code) <> ''
GROUP BY platform, coupon_code, coupon_pct, coupon_min_spend, coupon_max_discount
ORDER BY platform, coupon_min_spend;
