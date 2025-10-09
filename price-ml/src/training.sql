WITH daily_avg AS (
    SELECT
        products.external_id,
        prices.created_at::DATE AS price_date,
        AVG(prices.price) AS daily_average_price,
        subcategory_id
    FROM products
    LEFT JOIN prices ON products.id = prices.product_id
    GROUP BY
        subcategory_id,
        products.external_id,
        prices.created_at::DATE
), previous_average as (
    SELECT
        external_id,
        price_date,
        daily_average_price,
        LAG(daily_average_price, 1, NULL) OVER (PARTITION BY external_id ORDER BY price_date) AS previous_day_average_price,
        subcategory_id
    FROM daily_avg
)
SELECT *
FROM previous_average
WHERE previous_day_average_price IS NOT NULL;