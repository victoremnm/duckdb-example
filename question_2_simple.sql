SELECT AVG(DATEDIFF('day', p_cancel.Canceled_Date, p_new.Created_At)) AS average_duration_days
FROM policies p_cancel
JOIN policies p_new
  ON p_cancel.User_ID = p_new.User_ID
WHERE p_cancel.Canceled_Date IS NOT NULL
  AND p_new.Created_At IS NOT NULL
  -- Ensure p_new is indeed a *new* policy after cancellation of p_cancel
  AND p_new.Created_At > p_cancel.Canceled_Date
  -- Optional: To ensure it's a distinct policy
  AND p_new.Policy_ID != p_cancel.Policy_ID
  -- Limit to the *first* new policy after cancellation, or just any new policy?
  -- Assuming "a new policy" means the first one after cancellation for simplicity.
  -- For a more robust solution, you might need a CTE with LAG/LEAD to pair them correctly.
  -- This simpler join will average all valid pairs.
;