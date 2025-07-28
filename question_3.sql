WITH PolicyActivity AS (
    SELECT
        Policy_ID,
        User_ID,
        Created_At,
        Canceled_Date,
        -- Get the previous policy's Canceled_Date for the same user
        LAG(Canceled_Date) OVER (PARTITION BY User_ID ORDER BY Created_At) AS Previous_Canceled_Date,
        -- Get the previous policy's Created_At for the same user
        LAG(Created_At) OVER (PARTITION BY User_ID ORDER BY Created_At) AS Previous_Created_At,
        -- Get the next policy's Created_At for the same user
        LEAD(Created_At) OVER (PARTITION BY User_ID ORDER BY Created_At) AS Next_Created_At
    FROM policies
),
CalculatedFields AS (
    SELECT
        Policy_ID,
        User_ID,
        Created_At,
        Canceled_Date,
        Previous_Canceled_Date,
        Previous_Created_At,
        Next_Created_At,
        -- Logic for Is_New_User
        -- A user is "new" if they never had a policy before this one (first policy for the user)
        -- OR if their *previous* policy was canceled more than 30 days before this one was created.
        (Previous_Created_At IS NULL OR -- This is the first policy for the user
         (Previous_Canceled_Date IS NOT NULL AND DATEDIFF('day', Previous_Canceled_Date, Created_At) > 30))
        AS is_new_user,

        -- Logic for Churned_Date
        CASE
            WHEN Canceled_Date IS NULL THEN NULL -- Policy is still active, so no churn
            WHEN Next_Created_At IS NOT NULL AND DATEDIFF('day', Canceled_Date, Next_Created_At) <= 30 THEN NULL -- New policy created within 30 days (moving)
            ELSE Canceled_Date + INTERVAL '30 day' -- Policy canceled, no new policy within 30 days (churn)
        END AS Churned_Date
    FROM PolicyActivity
)
SELECT
    Policy_ID,
    is_new_user,
    Churned_Date
FROM CalculatedFields;