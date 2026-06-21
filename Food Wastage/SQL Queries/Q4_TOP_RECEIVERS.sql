
        SELECT 
            r."Receiver_ID", r."Name", r."Type", r."City",
            COUNT(c."Claim_ID") as Total_Claims,
            SUM(f."Quantity") as Total_Quantity_Claimed,
            r."Contact_Number" 
        FROM Receivers r
        JOIN Claims c ON r."Receiver_ID" = c."Receiver_ID"
        JOIN Food_Listings f ON c."Food_ID" = f."Food_ID"
        WHERE c."Status" = 'Completed'
        GROUP BY r."Receiver_ID", r."Name", r."Type", r."City", r."Contact_Number"
        ORDER BY Total_Quantity_Claimed DESC
        LIMIT 10;