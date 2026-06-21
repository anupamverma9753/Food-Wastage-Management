
        SELECT 
            f."Location" as City,
            COUNT(DISTINCT p."Provider_ID") as Total_Providers,
            COUNT(DISTINCT CASE WHEN c."Status" = 'Completed' THEN r."Receiver_ID" END) as Active_Receivers,
            COUNT(f."Food_ID") as Total_Food_Listed,
            COUNT(c."Claim_ID") as Total_Claims,
            SUM(CASE WHEN c."Status" = 'Completed' THEN 1 ELSE 0 END) as Completed_Claims,
            SUM(CASE WHEN c."Status" = 'Pending' THEN 1 ELSE 0 END) as Pending_Claims,
            ROUND(SUM(CASE WHEN c."Status" = 'Completed' THEN 1 ELSE 0 END) * 100.0 / 
                  NULLIF(COUNT(c."Claim_ID"), 0), 2) as Success_Rate
        FROM Food_Listings f
        JOIN Providers p ON f."Provider_ID" = p."Provider_ID"
        LEFT JOIN Claims c ON f."Food_ID" = c."Food_ID"
        LEFT JOIN Receivers r ON c."Receiver_ID" = r."Receiver_ID"
        GROUP BY f."Location"
        ORDER BY Total_Claims DESC;