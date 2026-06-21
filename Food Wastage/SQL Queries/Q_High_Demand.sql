SELECT 
        f."Location", 
        COUNT(c."Claim_ID") AS "Total_Claims",
        SUM(f."Quantity") AS "Total_Volume_Claimed"
    FROM claims c
    JOIN food_listings f ON c."Food_ID" = f."Food_ID"
    GROUP BY f."Location"
    ORDER BY "Total_Claims" DESC;