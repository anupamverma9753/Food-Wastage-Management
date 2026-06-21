
        SELECT 
            f."Meal_Type",
            COUNT(c."Claim_ID") as Number_of_Claims,
            SUM(f."Quantity") as Total_Quantity_Claimed,
            ROUND(AVG(f."Quantity"), 2) as Average_Quantity
        FROM Food_Listings f
        JOIN Claims c ON f."Food_ID" = c."Food_ID"
        WHERE c."Status" = 'Completed'
        GROUP BY f."Meal_Type"
        ORDER BY Number_of_Claims DESC;