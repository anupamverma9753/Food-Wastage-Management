SELECT 
        p."Provider_ID", 
        p."Name" AS "Provider_Name", 
        COUNT(f."Food_ID") AS "Total_Donations_Count",
        SUM(f."Quantity") AS "Total_Items_Contributed"
    FROM food_listings f
    JOIN providers p ON f."Provider_ID" = p."Provider_ID"
    GROUP BY p."Provider_ID", p."Name"
    ORDER BY "Total_Items_Contributed" DESC;