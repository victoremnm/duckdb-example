-- Optional: Create a dummy users table for demonstration if you don't have one
-- If you have a real 'users' table, skip this block.
-- CREATE TABLE users (
--     User_ID VARCHAR,
--     Date_of_Birth DATE
-- );
-- INSERT INTO users (User_ID, Date_of_Birth) VALUES
-- ('U001', '1990-05-15'),
-- ('U002', '1985-11-22'),
-- ('U003', '2000-01-01'),
-- ('U004', '1992-07-20'),
-- ('U005', '1988-03-10');


WITH PoliciesWithFullStatus AS (
    -- Join the original policies data with the calculated fields from the view
    SELECT
        p.Policy_ID,
        p.User_ID,
        p.Created_At,
        p.Canceled_Date,
        p.Annual_Premium,
        p.State,
        p.Type,
        pws.is_new_user,
        pws.Churned_Date
    FROM policies AS p
    JOIN policies_with_churn_status AS pws
      ON p.Policy_ID = pws.Policy_ID
),
UserPolicySequence AS (
    -- Add window functions to get previous policy type for sale_type determination
    SELECT
        pfs.Policy_ID,
        pfs.User_ID,
        pfs.Created_At AS Sale_Date,
        pfs.Annual_Premium AS Sale_Amount,
        pfs.State,
        pfs.Type,
        pfs.is_new_user,
        pfs.Churned_Date,
        LAG(pfs.Type) OVER (PARTITION BY pfs.User_ID ORDER BY pfs.Created_At) AS Previous_Policy_Type,
        -- Also get the previous policy's Created_At to ensure it's a *different* policy
        LAG(pfs.Created_At) OVER (PARTITION BY pfs.User_ID ORDER BY pfs.Created_At) AS Previous_Sale_Date
    FROM PoliciesWithFullStatus AS pfs
)
SELECT
    ups.Policy_ID,
    ups.User_ID,
    ups.Sale_Date,
    ups.State,
    ups.Type,
    ups.Sale_Amount,
    -- Calculate User_age_at_purchase
    -- This requires a 'users' table with Date_of_Birth
    -- Uncomment and adjust if you have a 'users' table
    -- DATEDIFF('year', u.Date_of_Birth, ups.Sale_Date) AS User_age_at_purchase,
    NULL AS User_age_at_purchase, -- Placeholder if users table is not available

    -- Determine Sale_Type based on the defined logic
    CASE
        -- new_sale: First ever policy, or user returns after churning
        WHEN ups.is_new_user THEN 'new_sale'
        WHEN ups.Churned_Date IS NOT NULL AND ups.Sale_Date > ups.Churned_Date THEN 'new_sale'
        -- cross_sale: Active user buys a policy of a *different* type
        WHEN ups.Previous_Policy_Type IS NOT NULL
             AND ups.Type != ups.Previous_Policy_Type
             -- Ensure user was 'active' at the time of sale (i.e., not churned yet)
             AND (ups.Churned_Date IS NULL OR ups.Sale_Date < ups.Churned_Date)
             THEN 'cross_sale'
        -- up_sale: Active user buys another policy of the *same* type
        WHEN ups.Previous_Policy_Type IS NOT NULL
             AND ups.Type = ups.Previous_Policy_Type
             -- Ensure user was 'active' at the time of sale (i.e., not churned yet)
             AND (ups.Churned_Date IS NULL OR ups.Sale_Date < ups.Churned_Date)
             THEN 'up_sale'
        ELSE 'unknown_sale_type' -- Fallback for any cases not explicitly covered
    END AS Sale_Type
FROM UserPolicySequence AS ups
-- LEFT JOIN users AS u ON ups.User_ID = u.User_ID -- Uncomment if you have the users table
ORDER BY ups.Sale_Date, ups.Policy_ID;