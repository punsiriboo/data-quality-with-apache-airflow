SELECT 
    COUNT(*) AS total_pass_checks
FROM orders
WHERE price > 0 AND 
    quantity > 100 AND 
    order_date IS NOT NULL AND 
    `status` IN ('Cancelled', 'Complete', 'Processing', 'Returned', 'Shipped')