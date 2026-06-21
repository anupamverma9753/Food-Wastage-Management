SELECT 
        f."Food_Type",
        COUNT(CASE WHEN f."Expiry_Date" < CURRENT_DATE THEN 1 END) AS "Expired_Count",
        COUNT(CASE WHEN c."Status" = 'Completed' THEN 1 END) AS "Successfully_Distributed",
        ROUND(100.0 * (count(f."Food_ID")-COUNT(CASE WHEN c."Status" = 'Completed' THEN 1 END)) / COUNT(f."Food_ID"), 2) AS     "Wastage_Rate_Percentage"
    FROM food_listings f
    LEFT JOIN claims c ON f."Food_ID" = c."Food_ID"
    GROUP BY f."Food_Type";