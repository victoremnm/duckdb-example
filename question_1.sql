SELECT COUNT(DISTINCT p1.User_ID) AS users_who_re_purchased
FROM policies p1
WHERE EXTRACT(YEAR FROM p1.Canceled_Date) = 2021 -- Policies canceled in 2021
  AND EXISTS (
    SELECT 1
    FROM policies p2
    WHERE p2.User_ID = p1.User_ID -- Same user
      AND EXTRACT(YEAR FROM p2.Created_At) = 2022 -- Bought another policy in 2022
  );