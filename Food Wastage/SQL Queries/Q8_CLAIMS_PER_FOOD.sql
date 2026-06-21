
        SELECT 
            f."Food_ID", f."Food_Name", f."Food_Type", f."Meal_Type", f."Location",
            COUNT(c."Claim_ID") as Number_of_Claims,
            f."Quantity" as Available_Quantity
        FROM Food_Listings f
        LEFT JOIN Claims c ON f."Food_ID" = c."Food_ID"
        GROUP BY f."Food_ID", f."Food_Name", f."Food_Type", f."Meal_Type", f."Location", f."Quantity"
        ORDER BY Number_of_Claims DESC;