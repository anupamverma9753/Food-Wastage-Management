
        SELECT 
            r."Receiver_ID", r."Name", r."Type", r."City",
            COUNT(c."Claim_ID") as Total_Claims,
            SUM(f."Quantity") as Total_Quantity_Claimed,
            ROUND(AVG(f."Quantity"), 2) as Average_Quantity_Per_Claim
        FROM Receivers r
        JOIN Claims c ON r."Receiver_ID" = c."Receiver_ID"
        JOIN Food_Listings f ON c."Food_ID" = f."Food_ID"
        WHERE c."Status" = 'Completed'
        GROUP BY r."Receiver_ID", r."Name", r."Type", r."City"
        ORDER BY Average_Quantity_Per_Claim DESC;