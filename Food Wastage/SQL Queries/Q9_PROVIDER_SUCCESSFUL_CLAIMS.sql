
        SELECT 
            p."Provider_ID", p."Name", p."Type", p."City",
            COUNT(c."Claim_ID") as Successful_Claims,
            SUM(f."Quantity") as Total_Food_Distributed,
            p."Contact_Number"
        FROM Providers p
        JOIN Food_Listings f ON p."Provider_ID" = f."Provider_ID"
        JOIN Claims c ON f."Food_ID" = c."Food_ID"
        WHERE c."Status" = 'Completed'
        GROUP BY p."Provider_ID", p."Name", p."Type", p."City", p."Contact_Number"
        ORDER BY Successful_Claims DESC
        LIMIT 10;